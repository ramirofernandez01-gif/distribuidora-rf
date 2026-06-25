from flask import Flask, request, redirect, url_for, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy

from app.models import database, bcrypt

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    
    bcrypt.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'

    @app.context_processor
    def inject_user():
        from flask_login import current_user
        return {'current_user': current_user}

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pruebabbdd.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
    database.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            from app.models import Usuario
            return Usuario.query.get(int(user_id))
        except Exception as e:
            print(f"Error en user_loader: {e}")
            return None
    
    with app.app_context():
        try:
            from app.models import Usuario, Categoria, Producto, Carrito, Carrito_detalle, cargarAdmin, cargarTipoUsuario, cargarCliente, cargarCategoriaProductos, cargarProductos
            
            database.create_all()
            
            cargarTipoUsuario()
            cargarCategoriaProductos()
            cargarProductos()
            cargarAdmin()
            cargarCliente()

        except Exception as e:
            print(f"Error al crear las tablas o cargar usuarios: {e}")
    
    from .blueprints import ALL_BLUEPRINTS
    
    for blueprint in ALL_BLUEPRINTS:
        app.register_blueprint(blueprint)
    
    @app.errorhandler(404)
    def not_found(error):
        return "Página no encontrada - Distribuidora RF", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return "Error interno del servidor - Distribuidora RF", 500
    
    return app
