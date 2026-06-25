from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Producto, Categoria
from app import database

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/')
def list_products():
    try:
        productos = Producto.query.all()
        categorias = {cat.id: cat.nombre for cat in Categoria.query.all()}
        
        return render_template('productos.html', 
                             productos=productos, 
                             categorias=categorias)
    except Exception as e:
        return render_template('productos.html', 
                             productos=[], 
                             categorias={})

@products_bp.route('/panel')
def panel():
    try:
        productos = Producto.query.all()
        categorias_list = Categoria.query.all()
        categorias = {cat.id: cat.nombre for cat in categorias_list}
        
        total_stock = sum(producto.stock for producto in productos)
        valor_inventario = sum(producto.precio * producto.stock for producto in productos)
        precio_promedio = sum(producto.precio for producto in productos) / len(productos) if productos else 0
        
        return render_template('panel_productos.html', 
                             productos=productos,
                             categorias=categorias,
                             total_stock=total_stock,
                             valor_inventario=valor_inventario,
                             precio_promedio=precio_promedio)
    except Exception as e:
        return render_template('panel_productos.html', 
                             productos=[],
                             categorias={},
                             total_stock=0,
                             valor_inventario=0,
                             precio_promedio=0)


@products_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()
            precio = request.form.get('precio')
            stock = request.form.get('stock')
            fk_categoria = request.form.get('fk_categoria', 1)
            peligroso = bool(request.form.get('peligroso'))
            imagen = request.files.get('imagen')
            
            if not nombre:
                flash('El nombre del producto es obligatorio', 'error')
                return redirect(url_for('products.panel'))
            
            if not precio or float(precio) <= 0:
                flash('El precio debe ser mayor a 0', 'error')
                return redirect(url_for('products.panel'))
                
            if not stock or int(stock) < 0:
                flash('El stock no puede ser negativo', 'error')
                return redirect(url_for('products.panel'))
            
            imagen_url = None
            if imagen and imagen.filename:
                import os
                import uuid
                from werkzeug.utils import secure_filename
                
                upload_folder = os.path.join('app', 'static', 'img', 'products')
                os.makedirs(upload_folder, exist_ok=True)
                
                ext = imagen.filename.rsplit('.', 1)[1].lower() if '.' in imagen.filename else 'jpg'
                filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")
                filepath = os.path.join(upload_folder, filename)
                
                imagen.save(filepath)
                imagen_url = f"img/products/{filename}"

            nuevo_producto = Producto(
                nombre=nombre,
                precio=float(precio),
                stock=int(stock),
                fk_categoria=int(fk_categoria),
                peligroso=peligroso,
                imagen_url=imagen_url
            )
            
            database.session.add(nuevo_producto)
            database.session.commit()
            
            flash(f'Producto "{nombre}" agregado exitosamente!', 'success')
            
            return redirect(url_for('products.panel'))
            
        except ValueError as e:
            database.session.rollback()
            flash('Error en los datos ingresados. Verifica precio y stock.', 'error')
            return redirect(url_for('products.panel'))
            
        except Exception as e:
            database.session.rollback()
            flash('Error interno del servidor. Intenta nuevamente.', 'error')
            return redirect(url_for('products.panel'))
    
    categorias = Categoria.query.all()
    return render_template('panel_productos.html', categorias=categorias)


@products_bp.route('/edit/<int:producto_id>', methods=['GET', 'POST'])
def edit_product(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    
    if request.method == 'POST':
        try:
            producto.nombre = request.form.get('nombre', '').strip()
            producto.precio = float(request.form.get('precio', 0))
            producto.stock = int(request.form.get('stock', 0))
            producto.fk_categoria = int(request.form.get('fk_categoria', 1))
            producto.peligroso = bool(request.form.get('peligroso'))
            
            imagen = request.files.get('imagen')
            if imagen and imagen.filename:
                import os
                import uuid
                from werkzeug.utils import secure_filename
                
                upload_folder = os.path.join('app', 'static', 'img', 'products')
                os.makedirs(upload_folder, exist_ok=True)
                
                ext = imagen.filename.rsplit('.', 1)[1].lower() if '.' in imagen.filename else 'jpg'
                filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")
                filepath = os.path.join(upload_folder, filename)
                
                imagen.save(filepath)
                producto.imagen_url = f"img/products/{filename}"
            
            database.session.commit()
            flash(f'Producto "{producto.nombre}" actualizado exitosamente!', 'success')
            
            return redirect(url_for('products.panel'))
            
        except Exception as e:
            database.session.rollback()
            flash('Error al actualizar producto. Intenta nuevamente.', 'error')
            return redirect(url_for('products.panel'))
    
    categorias = Categoria.query.all()
    return render_template('panel_productos.html', producto=producto, categorias=categorias)


@products_bp.route('/delete/<int:producto_id>', methods=['POST'])
def delete_product(producto_id):
    try:
        producto = Producto.query.get_or_404(producto_id)
        nombre_producto = producto.nombre
        
        database.session.delete(producto)
        database.session.commit()
        
        flash(f'Producto "{nombre_producto}" eliminado exitosamente!', 'success')
        
    except Exception as e:
        database.session.rollback()
        flash('Error al eliminar producto. Intenta nuevamente.', 'error')
    
    return redirect(url_for('products.panel'))


@products_bp.route('/api/categorias')
def get_categorias():
    try:
        categorias = Categoria.query.all()
        categorias_json = [{'id': cat.id, 'nombre': cat.nombre} for cat in categorias]
        return jsonify(categorias_json)
    except Exception as e:
        return jsonify([]), 500