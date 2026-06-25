Distribuidora RF — Documentación del Proyecto

E-commerce de repuestos y autopartes construido con Flask (Python), SQLite y Tailwind CSS.


TABLA DE CONTENIDOS

1. Estructura del Proyecto
2. Stack Tecnológico
3. Cómo Correr el Proyecto
4. Base de Datos — Modelos
5. Rutas del Servidor (Blueprints)
6. Inicialización de la Aplicación
7. Módulo de Inteligencia Artificial
8. Frontend — Plantillas y Diseño
9. Frontend — JavaScript y Lógica de Cliente
10. Usuarios del Sistema y Permisos
11. Catálogo de Productos y Carrito
12. Flujo General de Compra


1. ESTRUCTURA DEL PROYECTO

El proyecto sigue un patrón de diseño Modelo-Vista-Controlador adaptado a Flask, organizado en una carpeta principal "app":

- run.py: Punto de entrada para iniciar el servidor.
- requirements.txt: Lista de dependencias del proyecto.
- app/__init__.py: Fábrica principal de la aplicación Flask.
- app/models.py: Define la estructura de la base de datos (tablas y columnas).
- app/blueprints/: Contiene la lógica del servidor dividida en módulos (auth, admin, products, users, ia).
- app/templates/: Contiene todos los archivos visuales (HTML).
- app/static/: Contiene estilos CSS, scripts JavaScript, e imágenes.


2. STACK TECNOLÓGICO

- Backend: Python 3 con el framework Flask.
- Base de datos: SQLite manipulada a través de SQLAlchemy (ORM).
- Autenticación: Flask-Login para manejo de sesiones seguras y Flask-Bcrypt para encriptar contraseñas.
- Frontend: HTML5, CSS puro y TailwindCSS para el diseño responsivo. JavaScript nativo para animaciones e interacciones.
- Inteligencia Artificial: Modelo de clasificación de sentimientos utilizando scikit-learn.


3. CÓMO CORRER EL PROYECTO

Para poner en marcha la aplicación, se deben ejecutar los siguientes comandos en la terminal, dentro de la carpeta del proyecto:

Crear entorno virtual:
python -m venv .venv_run

Activar el entorno:
.venv_run\Scripts\activate

Instalar dependencias:
pip install -r requirements.txt

Ejecutar la aplicación:
python run.py

La aplicación estará disponible abriendo el navegador en la dirección: http://127.0.0.1:5000


4. BASE DE DATOS — MODELOS

La base de datos almacena toda la información estructural en distintas tablas conectadas entre sí:

- Usuario: Almacena los datos de los clientes y administradores. Campos principales: username (nombre de usuario único), email (correo electrónico), nombre (real), apellido, dni, direccion y password (encriptada). 
- TipoUsuario: Define los niveles de acceso (Administrador o Cliente).
- Categoria: Agrupa los productos (Motor, Frenos, Suspensión, etc.).
- Producto: Almacena el catálogo de autopartes. Incluye nombre, precio, stock, y si el producto requiere manejo especial (peligroso).
- Carrito y Envios: Tablas preparadas para almacenar el historial de compras.


5. RUTAS DEL SERVIDOR (BLUEPRINTS)

La lógica del servidor está modularizada para mantener el orden:

- Auth: Maneja el inicio de sesión (/login), el registro (/singin) y el cierre de sesión (/logout). Asegura que no haya usuarios duplicados y encripta las contraseñas antes de guardarlas.
- Products: Gestiona la vista del catálogo público y el panel interno donde el administrador puede agregar, editar (modificando incluso la imagen) o eliminar repuestos.
- Users: Gestiona la vista del carrito de compras, la pantalla de compra exitosa y el perfil del cliente.
- Admin: Proporciona el tablero principal para los dueños del negocio, incluyendo el listado y edición de todos los usuarios registrados.
- IA: Integra la interfaz de predicción de texto mediante inteligencia artificial.


6. INICIALIZACIÓN DE LA APLICACIÓN

Cuando se ejecuta el archivo run.py, ocurre lo siguiente:
- Se inicia Flask y se configura la llave secreta para proteger las sesiones.
- Se conecta SQLAlchemy con la base de datos SQLite local.
- Se crean todas las tablas si no existían previamente.
- Se inyectan datos de prueba por defecto (categorías, lista extensa de autopartes, y un administrador por defecto).


7. MÓDULO DE INTELIGENCIA ARTIFICIAL

El sistema cuenta con un modelo de Machine Learning entrenado previamente (guardado en un archivo .joblib).
Los clientes pueden ingresar texto y el modelo predecirá si el sentimiento o la necesidad planteada es Positiva o Negativa, retornando el nivel de confianza de la predicción.


8. FRONTEND — PLANTILLAS Y DISEÑO

Todo el aspecto visual está diseñado buscando una apariencia extremadamente profesional y moderna.
Se utiliza un esquema de colores basado en tonos de azul marino (dark-teal), azul brillante (pro-blue) y blanco humo.

- Interfaz Global: Una barra de navegación inteligente que cambia sus opciones dependiendo de si el usuario es un invitado, un cliente o un administrador.
- Tarjetas de Productos: Tienen un efecto 3D que gira al hacerles clic, revelando la descripción técnica de la autoparte en su reverso.
- Formularios: Los campos de ingreso (como login y registro) tienen validaciones visuales en tiempo real y bordes redondeados estilizados.
- Ventanas Emergentes (Modales): Se crearon ventanas modernas para confirmar eliminaciones, editar datos (con soporte para emails e imágenes) o procesar el pago sin necesidad de recargar la página.


9. FRONTEND — JAVASCRIPT Y LÓGICA DE CLIENTE

El comportamiento interactivo del navegador está controlado por JavaScript:

- Carrito de Compras: Utiliza el almacenamiento local (localStorage) del navegador. Esto permite que el usuario navegue por toda la página agregando repuestos sin que se pierdan, de una manera extremadamente rápida ya que no requiere consultas constantes a la base de datos hasta que se decida finalizar la compra.
- Modales: Manejo de apertura y cierre de ventanas con suaves animaciones de opacidad y escala.


10. USUARIOS DEL SISTEMA Y PERMISOS

El sistema distingue fuertemente entre dos tipos de roles:
- Administradores: Tienen un panel de control exclusivo. Pueden ver y editar información de cualquier cliente, y pueden administrar el catálogo completo de productos (subir fotos, modificar precios, agregar stock). No pueden comprar.
- Clientes (Particulares o Empresas): Tienen su propio carrito, pueden ver el catálogo, acceder a la inteligencia artificial, registrarse y realizar pagos.

Para el primer ingreso, se crea automáticamente un administrador con el correo "user1@distribuidora.com" y un cliente de prueba.


11. CATÁLOGO DE PRODUCTOS Y CARRITO

El catálogo está compuesto por repuestos automotores divididos en categorías como Motor, Suspensión, Electricidad y Encendido.
Los clientes pueden añadir estos productos a su carrito. El icono del carrito en la barra de navegación se actualiza instantáneamente con una pequeña burbuja indicando la cantidad de artículos elegidos.


12. FLUJO GENERAL DE COMPRA

El recorrido del cliente es el siguiente:
- Explora el catálogo de autopartes.
- Agrega ítems al carrito (si no tiene sesión iniciada, el sistema le pedirá que inicie sesión).
- Ingresa a la pantalla del Carrito, donde puede ajustar cantidades y ver el subtotal y los impuestos (IVA).
- Presiona "Confirmar Pedido".
- Se abre una ventana interactiva (Modal de Checkout) donde el usuario elige el Método de Pago (Efectivo o Tarjeta, obligando a llenar los datos de la tarjeta de forma validada si aplica) y el Método de Entrega (Retiro o Envío a Domicilio, exigiendo dirección en este último).
- Al confirmar el formulario validado, la compra se procesa de manera exitosa y el carrito se vacía automáticamente, llevando al cliente a una pantalla de agradecimiento.
