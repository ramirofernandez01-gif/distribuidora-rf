document.addEventListener("DOMContentLoaded", function() {
    console.log("🎯 Panel Admin JavaScript cargado correctamente");

    let tareas = [];
    const tareaInput = document.getElementById("tareaInput");
    const agregarBtn = document.getElementById("agregarBtn");
    const listaTareas = document.getElementById("listaTareas");
    const contadorTareas = document.getElementById("contadorTareas");
    const micButton = document.getElementById("micButton");

    function guardarTareas() {
        try {
            localStorage.setItem('cleansa-admin-tareas', JSON.stringify(tareas));
            console.log('✅ Tareas guardadas en localStorage');
        } catch (error) {
            console.error('❌ Error al guardar tareas:', error);
        }
    }

    function cargarTareas() {
        try {
            const tareasGuardadas = localStorage.getItem('cleansa-admin-tareas');
            if (tareasGuardadas) {
                tareas = JSON.parse(tareasGuardadas);
                console.log(`📂 ${tareas.length} tareas cargadas desde localStorage`);
            }
        } catch (error) {
            console.error('❌ Error al cargar tareas:', error);
            tareas = [];
        }
    }

    function agregarTarea() {
        const texto = tareaInput.value.trim();
        if (texto) {
            const nuevaTarea = {
                id: Date.now(),
                texto: texto,
                completada: false,
                fechaCreacion: new Date().toISOString()
            };
            tareas.push(nuevaTarea);
            tareaInput.value = "";
            mostrarTareas();
            guardarTareas();
            console.log(`✅ Tarea agregada: "${texto}"`);
        }
    }

    function eliminarTarea(id) {
        const index = tareas.findIndex(tarea => tarea.id === id);
        if (index !== -1) {
            const tareaEliminada = tareas[index];
            tareas.splice(index, 1);
            mostrarTareas();
            guardarTareas();
            console.log(`🗑️ Tarea eliminada: "${tareaEliminada.texto}"`);
        }
    }

    function alternarTarea(id) {
        const tarea = tareas.find(t => t.id === id);
        if (tarea) {
            tarea.completada = !tarea.completada;
            mostrarTareas();
            guardarTareas();
            console.log(`🔄 Tarea ${tarea.completada ? 'completada' : 'pendiente'}: "${tarea.texto}"`);
        }
    }

    function marcarTodasCompletadas() {
        tareas.forEach(tarea => tarea.completada = true);
        mostrarTareas();
        guardarTareas();
        console.log("✅ Todas las tareas marcadas como completadas");
    }

    function desmarcarTodas() {
        tareas.forEach(tarea => tarea.completada = false);
        mostrarTareas();
        guardarTareas();
        console.log("🔄 Todas las tareas desmarcadas");
    }

    function eliminarCompletadas() {
        const tareasAntesCount = tareas.length;
        tareas.splice(0, tareas.length, ...tareas.filter(tarea => !tarea.completada));
        const tareasEliminadas = tareasAntesCount - tareas.length;
        
        if (tareasEliminadas > 0) {
            console.log(`🗑️ ${tareasEliminadas} tarea(s) completada(s) eliminada(s)`);
            mostrarTareas();
            guardarTareas();
        }
    }

    function mostrarTareas() {
        if (!listaTareas) {
            console.warn("⚠️ Elemento listaTareas no encontrado");
            return;
        }
        
        listaTareas.innerHTML = "";
        
        if (tareas.length === 0) {
            listaTareas.innerHTML = `
                <li class="text-center py-12">
                    <div class="bg-gradient-to-br from-smoke-white/10 to-pro-blue/5 rounded-2xl p-8 border border-light-blue/20">
                        <svg class="w-16 h-16 mx-auto mb-4 text-light-blue/50" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                        </svg>
                        <p class="text-lg font-medium text-pro-blue mb-2">No hay tareas pendientes</p>
                        <p class="text-sm text-soft-gray">¡Organiza tu día agregando tu primera tarea!</p>
                        <div class="mt-4 flex justify-center">
                            <div class="flex items-center space-x-2 text-xs text-light-teal/70">
                                <span>💡</span>
                                <span>Tip: Usa el micrófono para agregar tareas por voz</span>
                            </div>
                        </div>
                    </div>
                </li>
            `;
        } else {
            tareas.forEach(function(tarea, index) {
                const li = document.createElement("li");
                li.className = `task-item group relative flex items-center p-4 rounded-xl transition-all duration-300 cursor-move transform hover:scale-[1.02] ${
                    tarea.completada 
                        ? 'bg-gradient-to-r from-warm-green/20 to-warm-green/10 border border-warm-green/30 shadow-lg shadow-warm-green/10' 
                        : 'bg-gradient-to-r from-smoke-white to-smoke-white/95 border border-light-blue/30 shadow-lg shadow-pro-blue/10 hover:border-pro-blue/50 hover:shadow-pro-blue/20'
                }`;
                
                li.draggable = true;
                li.dataset.index = index;
                
                const mainContainer = document.createElement("div");
                mainContainer.className = "flex items-center w-full space-x-4";
                
                const dragIcon = document.createElement("div");
                dragIcon.innerHTML = `
                    <svg class="w-5 h-5 text-soft-gray group-hover:text-pro-blue transition-colors duration-200" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M9 6a2 2 0 11-4 0 2 2 0 014 0zM9 12a2 2 0 11-4 0 2 2 0 014 0zM9 18a2 2 0 11-4 0 2 2 0 014 0zM19 6a2 2 0 11-4 0 2 2 0 014 0zM19 12a2 2 0 11-4 0 2 2 0 014 0zM19 18a2 2 0 11-4 0 2 2 0 014 0z"/>
                    </svg>
                `;
                dragIcon.className = "cursor-move flex-shrink-0 opacity-60 group-hover:opacity-100 transition-opacity duration-200";
                
                const checkboxContainer = document.createElement("div");
                checkboxContainer.className = "relative flex-shrink-0";
                
                const checkbox = document.createElement("input");
                checkbox.type = "checkbox";
                checkbox.checked = tarea.completada;
                checkbox.className = `
                    w-5 h-5 rounded-lg border-2 transition-all duration-200 cursor-pointer
                    ${tarea.completada 
                        ? 'bg-warm-green border-warm-green text-white' 
                        : 'bg-transparent border-pro-blue hover:border-light-blue focus:ring-2 focus:ring-pro-blue/50'
                    }
                `;
                checkbox.onchange = function() {
                    tarea.completada = this.checked;
                    mostrarTareas();
                    guardarTareas();
                };
                
                checkboxContainer.appendChild(checkbox);
                
                const tareaContent = document.createElement("div");
                tareaContent.className = "flex-1 min-w-0";
                
                const tareaTexto = document.createElement("p");
                tareaTexto.textContent = tarea.texto;
                tareaTexto.className = `
                    text-base font-medium transition-all duration-200 break-words
                    ${tarea.completada 
                        ? 'text-soft-gray line-through opacity-75' 
                        : 'text-dark-teal group-hover:text-pro-blue'
                    }
                `;
                
                const metaInfo = document.createElement("p");
                const fecha = new Date(tarea.fechaCreacion || Date.now()).toLocaleDateString('es-AR', {
                    day: '2-digit',
                    month: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit'
                });
                metaInfo.textContent = fecha;
                metaInfo.className = "text-xs text-soft-gray mt-1";
                
                tareaContent.appendChild(tareaTexto);
                tareaContent.appendChild(metaInfo);
                
                const btnEliminar = document.createElement("button");
                btnEliminar.innerHTML = `
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
                    </svg>
                `;
                btnEliminar.className = `
                    flex-shrink-0 w-8 h-8 rounded-lg transition-all duration-200 
                    bg-red-500/20 hover:bg-red-500 text-red-400 hover:text-white 
                    border border-red-500/30 hover:border-red-500
                    opacity-0 group-hover:opacity-100 transform scale-90 hover:scale-100
                    flex items-center justify-center
                `;
                btnEliminar.onclick = function(e) {
                    e.stopPropagation();
                    tareas.splice(index, 1);
                    mostrarTareas();
                    guardarTareas();
                };
                
                mainContainer.appendChild(dragIcon);
                mainContainer.appendChild(checkboxContainer);
                mainContainer.appendChild(tareaContent);
                mainContainer.appendChild(btnEliminar);
                
                li.appendChild(mainContainer);
                listaTareas.appendChild(li);
            });
        }
        
        const tareasCompletadas = tareas.filter(tarea => tarea.completada).length;
        const tareasPendientes = tareas.length - tareasCompletadas;
        
        if (contadorTareas) {
            contadorTareas.textContent = `Tareas Pendientes: ${tareasPendientes}`;
        }

        agregarEventosDragAndDrop();
    }

    let arrastrandoElemento = null;
    let indiceArrastrando = null;

    function agregarEventosDragAndDrop() {
        const items = listaTareas.querySelectorAll('li[draggable="true"]');

        items.forEach(item => {
            item.addEventListener('dragstart', function(e) {
                arrastrandoElemento = this;
                indiceArrastrando = parseInt(this.dataset.index);

                console.log(`🎯 Arrastrando tarea ${indiceArrastrando}: "${tareas[indiceArrastrando].texto}"`);

                this.classList.add('dragging');

                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/html', this.outerHTML);
            });

            item.addEventListener('dragend', function(e) {
                console.log('🔄 Arrastre finalizado');

                this.classList.remove('dragging');

                arrastrandoElemento = null;
                indiceArrastrando = null;
            });

            item.addEventListener('dragover', function(e) {
                e.preventDefault();

                this.classList.add('drag-over');
            });

            item.addEventListener('dragleave', function(e) {
                this.classList.remove('drag-over');
            });

            item.addEventListener('drop', function(e) {
                e.preventDefault();

                if (arrastrandoElemento && arrastrandoElemento !== this) {
                    const targetIndex = parseInt(this.dataset.index);
                    console.log(`📍 Soltando tarea ${indiceArrastrando} sobre tarea ${targetIndex}`);

                    reordenarTareas(indiceArrastrando, targetIndex);
                }

                this.classList.remove('drag-over');
            });
        });
    }

    function reordenarTareas(fromIndex, toIndex) {
        const tareaMovida = tareas[fromIndex];
        
        tareas.splice(fromIndex, 1);
        
        tareas.splice(toIndex, 0, tareaMovida);
        
        console.log('🔄 Array reordenado:', tareas);
        
        mostrarTareas();
        guardarTareas();
    }

    function configurarReconocimientoVoz() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.lang = 'es-AR';
            recognition.continuous = false;
            recognition.interimResults = false;

            let isListening = false;

            if (micButton) {
                micButton.addEventListener('click', function() {
                    if (!isListening) {
                        micButton.classList.remove('from-gray-100', 'to-smoke-white', 'hover:from-smoke-white', 'hover:to-gray-50');
                        micButton.classList.add('from-light-teal', 'to-light-blue', 'listening-pulse', 'shadow-light-teal/50');
                        micButton.title = 'Escuchando... Habla ahora';
                        
                        recognition.start();
                        isListening = true;
                        console.log('🎙️ Iniciando reconocimiento de voz...');
                    }
                });
            }

            recognition.addEventListener('result', function(event) {
                const transcript = event.results[0][0].transcript.trim();
                console.log('🗣️ Texto reconocido:', transcript);
                
                if (tareaInput) {
                    tareaInput.value = transcript;
                    tareaInput.focus();
                }
            });

            recognition.addEventListener('end', function() {
                console.log('🔇 Reconocimiento de voz finalizado');
                
                if (micButton) {
                    micButton.classList.remove('from-light-teal', 'to-light-blue', 'listening-pulse', 'shadow-light-teal/50');
                    micButton.classList.add('from-gray-100', 'to-smoke-white', 'hover:from-smoke-white', 'hover:to-gray-50');
                    micButton.title = 'Agregar tarea por voz';
                }
                isListening = false;
            });

            recognition.addEventListener('error', function(event) {
                console.error('❌ Error en reconocimiento de voz:', event.error);
                
                if (micButton) {
                    micButton.classList.remove('from-light-teal', 'to-light-blue', 'listening-pulse', 'shadow-light-teal/50'); 
                    micButton.classList.add('from-gray-100', 'to-smoke-white', 'hover:from-smoke-white', 'hover:to-gray-50');
                    micButton.title = 'Agregar tarea por voz';
                }
                isListening = false;
            });

        } else {
            if (micButton) {
                micButton.disabled = true;
                micButton.classList.add('opacity-50', 'cursor-not-allowed');
                micButton.title = 'Web Speech API no disponible en este navegador';
                
                micButton.addEventListener('click', function() {
                    alert('El navegador no soporta reconocimiento de voz.\n\nPor favor usa Chrome, Edge o Safari para esta funcionalidad.');
                });
            }
            console.warn('⚠️ Web Speech API no disponible en este navegador');
        }
    }

    function configurarEventListeners() {
        if (agregarBtn) {
            agregarBtn.addEventListener("click", agregarTarea);
        }

        if (tareaInput) {
            tareaInput.addEventListener("keypress", function(e) {
                if (e.key === "Enter") {
                    agregarTarea();
                }
            });
        }

        console.log("✅ Event listeners configurados");
    }

    window.alternarTarea = alternarTarea;
    window.eliminarTarea = eliminarTarea;
    window.marcarTodasCompletadas = marcarTodasCompletadas;
    window.desmarcarTodas = desmarcarTodas;
    window.eliminarCompletadas = eliminarCompletadas;

    cargarTareas();
    configurarEventListeners();
    configurarReconocimientoVoz();
    mostrarTareas();

    console.log("🚀 To Do List inicializado correctamente");

});