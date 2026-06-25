
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 Panel de Productos CleanSA iniciado');

    const modal = document.getElementById('productoModal');
    const openModalBtn = document.getElementById('openModalBtn');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const cancelModalBtn = document.getElementById('cancelModalBtn');
    const modalTitle = modal.querySelector('h3');
    const modalForm = modal.querySelector('form');

    const nombreInput = modalForm.querySelector('input[placeholder="Ej: Detergente Premium"]');
    const descripcionInput = modalForm.querySelector('textarea');
    const precioInput = modalForm.querySelector('input[type="number"][step="0.01"]');
    const stockInput = modalForm.querySelector('input[type="number"]:not([step])');
    const categoriaSelect = modalForm.querySelector('select[name="fk_categoria"]');

    if (openModalBtn) {
        openModalBtn.addEventListener('click', function() {
            openModal('add');
        });
    }

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeModal);
    }

    if (cancelModalBtn) {
        cancelModalBtn.addEventListener('click', closeModal);
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
            closeModal();
        }
    });

    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    function openModal(mode = 'add', productData = null) {
        if (mode === 'add') {
            modalTitle.textContent = 'Agregar Producto';
            modalForm.action = '/products/add';
            modalForm.method = 'POST';
            clearForm();
        } else if (mode === 'edit') {
            modalTitle.textContent = 'Editar Producto';
            modalForm.action = `/products/edit/${productData.id}`;
            modalForm.method = 'POST';
            fillForm(productData);
        }

        modal.classList.remove('hidden');

        if (nombreInput) {
            setTimeout(() => nombreInput.focus(), 100);
        }
    }

    function closeModal() {
        modal.classList.add('hidden');
        clearForm();
    }

    function clearForm() {
        modalForm.reset();
        
        const inputs = modalForm.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.classList.remove('border-red-500', 'border-green-500');
            
            const errorMsg = input.parentNode.querySelector('.error-message');
            if (errorMsg) {
                errorMsg.remove();
            }
        });
    }

    function fillForm(productData) {
        if (nombreInput) nombreInput.value = productData.nombre || '';
        if (descripcionInput) descripcionInput.value = '';
        if (precioInput) precioInput.value = productData.precio || '';
        if (stockInput) stockInput.value = productData.stock || '';
        if (categoriaSelect) categoriaSelect.value = productData.fk_categoria || '';
        
        const peligrosoCheckbox = modalForm.querySelector('input[name="peligroso"]');
        if (peligrosoCheckbox) {
            peligrosoCheckbox.checked = productData.peligroso || false;
        }
    }

    if (nombreInput) {
        nombreInput.addEventListener('input', function() {
            validateField(this, value => value.trim().length >= 3, 
                'El nombre debe tener al menos 3 caracteres');
        });
    }

    if (precioInput) {
        precioInput.addEventListener('input', function() {
            validateField(this, value => parseFloat(value) > 0, 
                'El precio debe ser mayor a 0');
        });
    }

    if (stockInput) {
        stockInput.addEventListener('input', function() {
            validateField(this, value => value !== '' && parseInt(value) >= 0, 
                'El stock no puede ser negativo');
        });
    }

    if (categoriaSelect) {
        categoriaSelect.addEventListener('change', function() {
            validateField(this, value => value !== '', 
                'Debe seleccionar una categoría');
        });
    }

    function validateField(input, validationFn, errorMessage) {
        const value = input.value;
        const isValid = validationFn(value);
        
        const existingError = input.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        if (isValid) {
            input.classList.remove('border-red-500');
            input.classList.add('border-green-500');
        } else {
            input.classList.remove('border-green-500');
            input.classList.add('border-red-500');
            
            const errorDiv = document.createElement('p');
            errorDiv.className = 'error-message text-red-600 text-xs mt-1';
            errorDiv.textContent = errorMessage;
            input.parentNode.appendChild(errorDiv);
        }

        return isValid;
    }

    modalForm.addEventListener('submit', function(e) {
        let isFormValid = true;
        
        if (nombreInput && !validateField(nombreInput, value => value.trim().length >= 3, 
            'El nombre debe tener al menos 3 caracteres')) {
            isFormValid = false;
        }
        
        if (precioInput && !validateField(precioInput, value => value !== '' && parseFloat(value) > 0, 
            'El precio debe ser mayor a 0')) {
            isFormValid = false;
        }
        
        if (stockInput && !validateField(stockInput, value => value !== '' && parseInt(value) >= 0, 
            'El stock no puede ser negativo y es requerido')) {
            isFormValid = false;
        }

        if (categoriaSelect && !validateField(categoriaSelect, value => value !== '', 
            'Debe seleccionar una categoría')) {
            isFormValid = false;
        }

        if (!isFormValid) {
            e.preventDefault();
            showNotification('Por favor corrige los errores antes de continuar', 'error');
            return;
        }

        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Guardando...';
        submitBtn.disabled = true;
    });

    document.querySelectorAll('[title="Editar"]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const row = this.closest('tr');
            const productData = extractProductDataFromRow(row);
            
            openModal('edit', productData);
        });
    });

    const deleteModal = document.getElementById('deleteProductModal');
    const deleteForm = document.getElementById('deleteProductForm');
    const deleteMessage = document.getElementById('deleteProductMessage');

    document.querySelectorAll('[title="Eliminar"]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const row = this.closest('tr');
            const productName = row.querySelector('td:nth-child(2) .text-sm.font-medium').textContent.trim();
            const productId = row.querySelector('td:first-child .text-sm').textContent.replace('#', '').trim();
            
            if (deleteModal && deleteForm && deleteMessage) {
                deleteMessage.textContent = `¿Estás seguro de que deseas eliminar "${productName}"? Esta acción no se puede deshacer.`;
                deleteForm.action = `/products/delete/${productId}`;
                
                deleteModal.classList.remove('hidden');
                setTimeout(() => {
                    deleteModal.classList.remove('opacity-0');
                    deleteModal.firstElementChild.classList.remove('scale-95');
                }, 10);
            }
        });
    });

    window.closeDeleteProductModal = function() {
        if (deleteModal) {
            deleteModal.classList.add('opacity-0');
            deleteModal.firstElementChild.classList.add('scale-95');
            setTimeout(() => {
                deleteModal.classList.add('hidden');
            }, 300);
        }
    };

    function extractProductDataFromRow(row) {
        const cells = row.querySelectorAll('td');
        
        return {
            id: cells[0].textContent.replace('#', '').trim(),
            nombre: cells[1].querySelector('.text-sm.font-medium').textContent.trim(),
            precio: cells[3].textContent.replace('$', '').replace(',', '').trim(),
            stock: cells[4].textContent.split(' ')[0].trim()
        };
    }

    function showNotification(message, type = 'info') {
        const existingNotification = document.querySelector('.custom-notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        const notification = document.createElement('div');
        notification.className = `custom-notification fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full`;
        
        switch (type) {
            case 'success':
                notification.classList.add('bg-warm-green', 'text-white');
                break;
            case 'error':
                notification.classList.add('bg-red-500', 'text-white');
                break;
            default:
                notification.classList.add('bg-pro-blue', 'text-white');
        }

        notification.innerHTML = `
            <div class="flex items-center">
                <span class="mr-3">${getIconForType(type)}</span>
                <span class="font-medium">${message}</span>
            </div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);

        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }, 4000);
    }

    function getIconForType(type) {
        switch (type) {
            case 'success':
                return '✅';
            case 'error':
                return '❌';
            default:
                return 'ℹ️';
        }
    }

    console.log('✅ Panel de Productos CleanSA completamente inicializado');
});