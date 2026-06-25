from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Usuario, database

users_bp = Blueprint('users', __name__, url_prefix='/admin/users')

@users_bp.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@users_bp.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        pass
    
    return "Formulario para agregar usuario (por implementar)"

@users_bp.route('/<int:user_id>')
def view_user(user_id):
    usuario = Usuario.query.get_or_404(user_id)
    return render_template('detalle_usuario.html', usuario=usuario)

@users_bp.route('/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    usuario = Usuario.query.get_or_404(user_id)
    
    if usuario.es_admin:
        return {"status": "error", "message": "Los administradores no pueden ser editados"}, 403

    data = request.get_json()
    if not data:
        return {"status": "error", "message": "Datos no válidos"}, 400

    try:
        usuario.username = data.get('username', usuario.username)
        usuario.email = data.get('email', usuario.email)
        usuario.nombre = data.get('nombre', usuario.nombre)
        usuario.apellido = data.get('apellido', usuario.apellido)
        usuario.dni = data.get('dni', usuario.dni)
        usuario.direccion = data.get('direccion', usuario.direccion)
        
        database.session.commit()
        return {"status": "success", "message": "Usuario actualizado correctamente"}
    except Exception as e:
        database.session.rollback()
        return {"status": "error", "message": str(e)}, 500

@users_bp.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    usuario = Usuario.query.get_or_404(user_id)
    
    if usuario.es_admin:
        return {"status": "error", "message": "Los administradores no pueden ser eliminados"}, 403
        
    try:
        database.session.delete(usuario)
        database.session.commit()
        return {"status": "success", "message": "Usuario eliminado correctamente"}
    except Exception as e:
        database.session.rollback()
        return {"status": "error", "message": str(e)}, 500

@users_bp.route('/panel')
def panel():
    usuarios = Usuario.query.all()
    return render_template('panel_usuarios.html', usuarios=usuarios)

@users_bp.route('/perfil')
def perfil():
    from flask_login import current_user
    from app.models import Carrito
    if current_user.is_authenticated:
        pedidos = Carrito.query.filter_by(fk_cliente=current_user.id).all()
    else:
        pedidos = []
    
    total_gastado = sum(p.total for p in pedidos if p.estado != 'Cancelado')
    return render_template('perfil_usuarios.html', pedidos=pedidos, total_gastado=total_gastado)


@users_bp.route('/carrito')
def carrito():
    return render_template('carrito.html')

@users_bp.route('/checkout', methods=['POST'])
def checkout():
    from flask_login import current_user
    from app.models import database, Carrito, Carrito_detalle, Producto
    from datetime import date
    import random

    if not current_user.is_authenticated:
        return {"status": "error", "message": "No autenticado"}, 401

    data = request.get_json()
    if not data or 'cart' not in data:
        return {"status": "error", "message": "Datos inválidos"}, 400

    cart_items = data['cart']
    total = float(data.get('total', 0))

    try:
        nuevo_carrito = Carrito(
            fecha=date.today(),
            estado='Completado',
            total=total,
            codigo_envio=random.randint(10000, 99999),
            fk_cliente=current_user.id
        )
        database.session.add(nuevo_carrito)
        database.session.flush()

        for item in cart_items:
            producto = Producto.query.get(item['id'])
            if producto:
                if producto.stock >= item['quantity']:
                    producto.stock -= item['quantity']
                else:
                    producto.stock = 0
                
                detalle = Carrito_detalle(
                    fk_carrito=nuevo_carrito.id,
                    fk_producto=producto.id,
                    total_producto=float(item['price']) * item['quantity'],
                    cantidad=item['quantity']
                )
                database.session.add(detalle)
        
        database.session.commit()
        return {"status": "success", "message": "Compra realizada exitosamente"}
    except Exception as e:
        database.session.rollback()
        return {"status": "error", "message": str(e)}, 500

@users_bp.route('/compra_exitosa')
def compra_exitosa():
    return render_template('compra_exitosa.html')