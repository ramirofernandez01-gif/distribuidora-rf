from .main import main_bp
from .admin import admin_bp
from .products import products_bp
from .employees import employees_bp
from .users import users_bp
from .auth import auth_bp
from .ia import ia_bp

ALL_BLUEPRINTS = [
    main_bp,
    admin_bp,
    products_bp,
    employees_bp,
    users_bp,
    auth_bp,
    ia_bp
]

__all__ = [
    'main_bp',
    'admin_bp', 
    'products_bp',
    'employees_bp',
    'users_bp',
    'ALL_BLUEPRINTS'
]