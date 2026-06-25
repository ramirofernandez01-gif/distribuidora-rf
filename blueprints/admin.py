from flask import Blueprint, render_template
from app.models import Producto, Usuario, Carrito, Carrito_detalle
from datetime import date, datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@admin_bp.route('/dashboard')
def index():
    from app.models import database

    total_productos = Producto.query.count()
    total_usuarios = Usuario.query.filter_by(fk_tipousuario=2).count()

    hoy = date.today()
    primer_dia_mes = date(hoy.year, hoy.month, 1)

    if hoy.month == 1:
        primer_dia_mes_anterior = date(hoy.year - 1, 12, 1)
        ultimo_dia_mes_anterior = date(hoy.year, 1, 1)
    else:
        primer_dia_mes_anterior = date(hoy.year, hoy.month - 1, 1)
        ultimo_dia_mes_anterior = date(hoy.year, hoy.month, 1)

    carritos_mes = Carrito.query.filter(
        Carrito.fecha >= primer_dia_mes,
        Carrito.estado != 'Cancelado'
    ).all()

    ventas_mes_actual = sum(c.total for c in carritos_mes)

    detalles_mes = []
    for c in carritos_mes:
        detalles = Carrito_detalle.query.filter_by(fk_carrito=c.id).all()
        detalles_mes.extend(detalles)
    productos_vendidos_mes = sum(d.cantidad for d in detalles_mes)

    ventas_mes_anterior = 100000.0

    if ventas_mes_anterior > 0:
        crecimiento = ((ventas_mes_actual - ventas_mes_anterior) / ventas_mes_anterior) * 100
    else:
        crecimiento = 0

    nombre_mes = [
        '', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ][hoy.month]

    mes_anterior_nombre = [
        '', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ][primer_dia_mes_anterior.month]

    return render_template(
        'pandel_admin.html',
        total_productos=total_productos,
        total_usuarios=total_usuarios,
        ventas_mes_actual=ventas_mes_actual,
        ventas_mes_anterior=ventas_mes_anterior,
        productos_vendidos_mes=productos_vendidos_mes,
        crecimiento=crecimiento,
        nombre_mes=nombre_mes,
        mes_anterior_nombre=mes_anterior_nombre
    )


@admin_bp.route('/stats')
def stats():
    return "Estadísticas del negocio (por implementar)"


@admin_bp.route('/reports')
def reports():
    return "Reportes administrativos (por implementar)"


@admin_bp.route('/settings')
def settings():
    return "Configuraciones del sistema (por implementar)"