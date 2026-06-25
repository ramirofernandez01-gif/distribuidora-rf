from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

database = SQLAlchemy()
bcrypt = Bcrypt()

class Usuario (database.Model, UserMixin):
    __tablename__ = 'usuarios'  
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), unique=True, nullable=False)
    email = database.Column(database.String(100), unique=True, nullable=False)
    nombre = database.Column(database.String(100), nullable=False)
    apellido = database.Column(database.String(100), nullable=False)
    password = database.Column(database.String(200), nullable=False)
    dni = database.Column(database.Integer, nullable=False)
    direccion = database.Column(database.String(100), nullable=False)
    fk_tipousuario = database.Column(database.Integer,database.ForeignKey('tipousuarios.id'), nullable=False)
    tipo = database.Column(database.Boolean, nullable=False)

    tipo_usuario = database.relationship('TipoUsuario', backref='usuarios')

    @property
    def es_admin(self):
        return self.fk_tipousuario == 1

    @property
    def es_cliente(self):
        return self.fk_tipousuario == 2

    @property
    def es_empresa(self):
        return self.tipo == True

    @property
    def es_particular(self):
        return self.tipo == False

    def get_id(self):
        return str(self.id)
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

    def __repr__(self):
        return f'<Usuario {self.nombre} {self.apellido}>'


class TipoUsuario (database.Model):
    __tablename__ = 'tipousuarios'  
    id = database.Column(database.Integer, primary_key=True)
    nombre = database.Column(database.String(100), nullable=False)

class Categoria (database.Model):
    __tablename__ = 'categorias'  
    id = database.Column(database.Integer, primary_key=True)
    nombre = database.Column(database.String(100), nullable=False)

class Producto (database.Model):
    __tablename__ = 'productos'  
    id = database.Column(database.Integer, primary_key=True)
    nombre = database.Column(database.String(100), nullable=False)
    precio = database.Column(database.Float, nullable=False)
    stock = database.Column(database.Integer, nullable=False)
    fk_categoria = database.Column(database.Integer,database.ForeignKey('categorias.id'), nullable=False)
    peligroso = database.Column(database.Boolean, nullable=False)
    imagen_url = database.Column(database.String(255), nullable=True)

class Carrito (database.Model):
    __tablename__ = 'carritos'  
    id = database.Column(database.Integer, primary_key=True)
    fecha = database.Column(database.Date, nullable=False)
    estado = database.Column(database.String(100), nullable=False)
    total = database.Column(database.Float, nullable=False)
    codigo_envio = database.Column(database.Integer, nullable=False)
    fk_cliente = database.Column(database.Integer,database.ForeignKey('usuarios.id'), nullable=False)


class Carrito_detalle (database.Model):
    __tablename__ = 'carrito_detalles'  
    id = database.Column(database.Integer, primary_key=True)
    fk_carrito = database.Column(database.Integer,database.ForeignKey('carritos.id'), nullable=False)
    fk_producto = database.Column(database.Integer, database.ForeignKey('productos.id'), nullable=False)
    total_producto = database.Column(database.Float,nullable=False)
    cantidad = database.Column(database.Integer,nullable=False)


class Envio (database.Model):
    __tablename__ = 'envios'  
    id = database.Column(database.Integer, primary_key=True)
    fk_carrito = database.Column(database.Integer,database.ForeignKey('carritos.id'), nullable=False)
    fecha_entrega = database.Column(database.Date, nullable=False)
    direccion = database.Column(database.String(100), nullable=False)


def cargarTipoUsuario():
    tipo_admin = TipoUsuario.query.filter_by(nombre='Administrador').first()
    if not tipo_admin:
        tipo_admin = TipoUsuario(
            nombre='Administrador'
        )
        try:
            database.session.add(tipo_admin) 
            database.session.commit()
        except Exception as e:
            database.session.rollback()
    
    tipo_cliente = TipoUsuario.query.filter_by(nombre='Cliente').first()
    if not tipo_cliente:
        tipo_cliente = TipoUsuario(
            nombre='Cliente'
        )
        try:
            database.session.add(tipo_cliente) 
            database.session.commit()
        except Exception as e:
            database.session.rollback()


def cargarAdmin():
    admin = Usuario.query.filter_by(nombre='ramiro').first()
    if not admin:
        hashed_password = Bcrypt().generate_password_hash('admin').decode('utf-8')
        admin_user = Usuario(
            username='ramiro_admin',
            email='admin@distribuidora.com',
            nombre='ramiro',
            apellido='fernandez',
            password=hashed_password,
            dni=44484315,
            direccion='Eva Peron 1071',
            fk_tipousuario=1,
            tipo=True
        )

        try:
            database.session.add(admin_user) 
            database.session.commit()
            print("✅ Usuario administrador creado: ramiro")
        except Exception as e:
            database.session.rollback()
            print(f"❌ Error creando admin: {e}")


def cargarCliente():
    cliente = Usuario.query.filter_by(nombre='mateo').first()
    if not cliente:
        hashed_password = Bcrypt().generate_password_hash('1234').decode('utf-8')
        cliente_user = Usuario(
            username='mateo_cli',
            email='mateo@cliente.com',
            nombre='mateo',
            apellido='flores',
            password=hashed_password,
            dni=45887718,
            direccion='Vera 885',
            fk_tipousuario=2,
            tipo=False
        )

        try:
            database.session.add(cliente_user) 
            database.session.commit()
            
        except Exception as e:
            database.session.rollback()


def cargarCategoriaProductos():
    categorias = [
        'Motor', 'Frenos', 'Suspensión', 'Electricidad', 
        'Filtros', 'Transmisión', 'Refrigeración', 'Encendido'
    ]
    categoria_ids = {}
    
    for cat_nombre in categorias:
        categoria = Categoria.query.filter_by(nombre=cat_nombre).first()
        if not categoria:
            categoria = Categoria(nombre=cat_nombre)
            try:
                database.session.add(categoria)
                database.session.commit()
                categoria_ids[cat_nombre] = categoria.id
            except Exception as e:
                print(f"❌ Error al crear categoría {cat_nombre}: {e}")
                database.session.rollback()
        else:
            categoria_ids[cat_nombre] = categoria.id
    
    return categoria_ids


def cargarProductos():
    motor_cat = Categoria.query.filter_by(nombre='Motor').first()
    frenos_cat = Categoria.query.filter_by(nombre='Frenos').first()
    suspension_cat = Categoria.query.filter_by(nombre='Suspensión').first()
    electricidad_cat = Categoria.query.filter_by(nombre='Electricidad').first()
    filtros_cat = Categoria.query.filter_by(nombre='Filtros').first()
    transmision_cat = Categoria.query.filter_by(nombre='Transmisión').first()
    refrigeracion_cat = Categoria.query.filter_by(nombre='Refrigeración').first()
    encendido_cat = Categoria.query.filter_by(nombre='Encendido').first()

    if not all([motor_cat, frenos_cat, suspension_cat, electricidad_cat,
                filtros_cat, transmision_cat, refrigeracion_cat, encendido_cat]):
        print("❌ Error: Las categorías deben crearse antes que los productos")
        return

    productos = [
        {'nombre': 'Junta de Culata Mahle - VW Gol 1.6', 'precio': 8500.00, 'stock': 25, 'fk_categoria': motor_cat.id, 'peligroso': False},
        {'nombre': 'Junta de Culata Mahle - Fiat Siena 1.6', 'precio': 7900.00, 'stock': 20, 'fk_categoria': motor_cat.id, 'peligroso': False},
        {'nombre': 'Kit Juntas Motor Completo - Ford Ka 1.0', 'precio': 12500.00, 'stock': 15, 'fk_categoria': motor_cat.id, 'peligroso': False},
        {'nombre': 'Kit Juntas Motor Completo - Renault Clio 1.2', 'precio': 11800.00, 'stock': 18, 'fk_categoria': motor_cat.id, 'peligroso': False},
        {'nombre': 'Seg de Émbolos STD - VW Gol 1.6 8V', 'precio': 6200.00, 'stock': 30, 'fk_categoria': motor_cat.id, 'peligroso': False},
        {'nombre': 'Seg de Émbolos 0.50 - Fiat 1.6 16V', 'precio': 6800.00, 'stock': 22, 'fk_categoria': motor_cat.id, 'peligroso': False},
        {'nombre': 'Cojinetes de Biela STD - Ford 1.6', 'precio': 3500.00, 'stock': 40, 'fk_categoria': motor_cat.id, 'peligroso': False},
        {'nombre': 'Cojinetes de Bancada STD - Renault 1.9 D', 'precio': 4200.00, 'stock': 35, 'fk_categoria': motor_cat.id, 'peligroso': False},
        {'nombre': 'Cadena de Distribución - Peugeot 207 1.4', 'precio': 9800.00, 'stock': 12, 'fk_categoria': motor_cat.id, 'peligroso': False},
        {'nombre': 'Kit de Distribución Dayco - VW Gol 1.6', 'precio': 15500.00, 'stock': 20, 'fk_categoria': motor_cat.id, 'peligroso': False},
        {'nombre': 'Kit de Distribución Gates - Fiat Siena 1.8', 'precio': 16200.00, 'stock': 18, 'fk_categoria': motor_cat.id, 'peligroso': False},
        {'nombre': 'Sello de Válvulas - Motor Renault 1.6', 'precio': 2800.00, 'stock': 50, 'fk_categoria': motor_cat.id, 'peligroso': False},
        {'nombre': 'Tapa de Distribución - Ford Mondeo 2.0', 'precio': 5500.00, 'stock': 15, 'fk_categoria': motor_cat.id, 'peligroso': False},
        {'nombre': 'Pastillas de Freno Delanteras Bosch - VW Gol', 'precio': 4500.00, 'stock': 60, 'fk_categoria': frenos_cat.id, 'peligroso': False},
        {'nombre': 'Pastillas de Freno Delanteras Bosch - Fiat Palio', 'precio': 4200.00, 'stock': 55, 'fk_categoria': frenos_cat.id, 'peligroso': False},
        {'nombre': 'Pastillas de Freno Traseras - Renault Megane', 'precio': 3800.00, 'stock': 45, 'fk_categoria': frenos_cat.id, 'peligroso': False},
        {'nombre': 'Disco de Freno Delantero EBC - Ford Focus', 'precio': 7200.00, 'stock': 30, 'fk_categoria': frenos_cat.id, 'peligroso': False},
        {'nombre': 'Disco de Freno Delantero Brembo - VW Polo', 'precio': 8500.00, 'stock': 25, 'fk_categoria': frenos_cat.id, 'peligroso': False},
        {'nombre': 'Disco de Freno Ventilado - Peugeot 308', 'precio': 9100.00, 'stock': 20, 'fk_categoria': frenos_cat.id, 'peligroso': False},
        {'nombre': 'Bomba de Freno Principal - Fiat Uno', 'precio': 6500.00, 'stock': 20, 'fk_categoria': frenos_cat.id, 'peligroso': True},
        {'nombre': 'Cilindro de Rueda Trasero - VW Gol', 'precio': 2900.00, 'stock': 40, 'fk_categoria': frenos_cat.id, 'peligroso': True},
        {'nombre': 'Flexo de Freno Traseero - Renault Clio', 'precio': 1800.00, 'stock': 60, 'fk_categoria': frenos_cat.id, 'peligroso': False},
        {'nombre': 'Zapatas de Freno - VW Gol Power', 'precio': 3200.00, 'stock': 50, 'fk_categoria': frenos_cat.id, 'peligroso': False},
        {'nombre': 'Líquido de Frenos DOT 4 - 500ml', 'precio': 1500.00, 'stock': 100, 'fk_categoria': frenos_cat.id, 'peligroso': True},
        {'nombre': 'Amortiguador Delantero Monroe - VW Gol', 'precio': 9800.00, 'stock': 20, 'fk_categoria': suspension_cat.id, 'peligroso': False},
        {'nombre': 'Amortiguador Delantero Gabriel - Ford Ka', 'precio': 8500.00, 'stock': 25, 'fk_categoria': suspension_cat.id, 'peligroso': False},
        {'nombre': 'Amortiguador Trasero Monroe - Renault Clio', 'precio': 7900.00, 'stock': 22, 'fk_categoria': suspension_cat.id, 'peligroso': False},
        {'nombre': 'Kit Buje de Rueda Delantero - Fiat Palio', 'precio': 5500.00, 'stock': 30, 'fk_categoria': suspension_cat.id, 'peligroso': False},
        {'nombre': 'Kit Buje de Rueda Trasero FAG - VW Gol', 'precio': 6200.00, 'stock': 28, 'fk_categoria': suspension_cat.id, 'peligroso': False},
        {'nombre': 'Rotula Superior Moog - Peugeot 207', 'precio': 4800.00, 'stock': 25, 'fk_categoria': suspension_cat.id, 'peligroso': False},
        {'nombre': 'Rótula Inferior - Ford Focus 2.0', 'precio': 5100.00, 'stock': 20, 'fk_categoria': suspension_cat.id, 'peligroso': False},
        {'nombre': 'Silent Block Brazo - Renault Megane II', 'precio': 2200.00, 'stock': 40, 'fk_categoria': suspension_cat.id, 'peligroso': False},
        {'nombre': 'Barra Estabilizadora - VW Polo', 'precio': 3500.00, 'stock': 30, 'fk_categoria': suspension_cat.id, 'peligroso': False},
        {'nombre': 'Kit Espiral Resorte Delantero - Fiat Siena', 'precio': 12000.00, 'stock': 15, 'fk_categoria': suspension_cat.id, 'peligroso': False},
        {'nombre': 'Bota de Dirección Interior - VW Gol', 'precio': 2800.00, 'stock': 45, 'fk_categoria': suspension_cat.id, 'peligroso': False},
        {'nombre': 'Bota de Dirección Exterior - Fiat Uno', 'precio': 2500.00, 'stock': 50, 'fk_categoria': suspension_cat.id, 'peligroso': False},
        {'nombre': 'Alternador Reconstruido - VW Gol 1.6', 'precio': 18500.00, 'stock': 10, 'fk_categoria': electricidad_cat.id, 'peligroso': True},
        {'nombre': 'Alternador Nuevo Bosch - Fiat Palio 1.4', 'precio': 24000.00, 'stock': 8, 'fk_categoria': electricidad_cat.id, 'peligroso': True},
        {'nombre': 'Motor de Arranque - Renault Clio 1.6', 'precio': 15000.00, 'stock': 12, 'fk_categoria': electricidad_cat.id, 'peligroso': True},
        {'nombre': 'Bateria 12V 60Ah Moura - Libre Mantenimiento', 'precio': 42000.00, 'stock': 30, 'fk_categoria': electricidad_cat.id, 'peligroso': True},
        {'nombre': 'Bateria 12V 75Ah Duncan - Libre Mantenimiento', 'precio': 48000.00, 'stock': 25, 'fk_categoria': electricidad_cat.id, 'peligroso': True},
        {'nombre': 'Bobina de Encendido NGK - Universal', 'precio': 6800.00, 'stock': 35, 'fk_categoria': electricidad_cat.id, 'peligroso': False},
        {'nombre': 'Sensor de Oxígeno Lambda - VW Gol', 'precio': 9500.00, 'stock': 20, 'fk_categoria': electricidad_cat.id, 'peligroso': False},
        {'nombre': 'Sensor de Temperatura Agua - Renault', 'precio': 3200.00, 'stock': 30, 'fk_categoria': electricidad_cat.id, 'peligroso': False},
        {'nombre': 'Sensor MAP - Peugeot 206 1.6', 'precio': 7800.00, 'stock': 15, 'fk_categoria': electricidad_cat.id, 'peligroso': False},
        {'nombre': 'Lámpara H4 12V 60/55W Osram - Par', 'precio': 2800.00, 'stock': 80, 'fk_categoria': electricidad_cat.id, 'peligroso': False},
        {'nombre': 'Filtro de Aceite Mann - VW Gol 1.6', 'precio': 1200.00, 'stock': 100, 'fk_categoria': filtros_cat.id, 'peligroso': False},
        {'nombre': 'Filtro de Aceite Mahle - Fiat 1.4', 'precio': 1100.00, 'stock': 90, 'fk_categoria': filtros_cat.id, 'peligroso': False},
        {'nombre': 'Filtro de Aire Mann - Renault Clio 1.2', 'precio': 1800.00, 'stock': 80, 'fk_categoria': filtros_cat.id, 'peligroso': False},
        {'nombre': 'Filtro de Aire Mahle - Ford Ka 1.0', 'precio': 1650.00, 'stock': 75, 'fk_categoria': filtros_cat.id, 'peligroso': False},
        {'nombre': 'Filtro de Combustible Bosch - VW Polo', 'precio': 2200.00, 'stock': 60, 'fk_categoria': filtros_cat.id, 'peligroso': True},
        {'nombre': 'Filtro de Combustible - Fiat Siena 1.6', 'precio': 2100.00, 'stock': 55, 'fk_categoria': filtros_cat.id, 'peligroso': True},
        {'nombre': 'Filtro de Habitaculo Mahle - Peugeot 207', 'precio': 2500.00, 'stock': 50, 'fk_categoria': filtros_cat.id, 'peligroso': False},
        {'nombre': 'Filtro de Habitaculo - VW Gol Trend', 'precio': 2300.00, 'stock': 60, 'fk_categoria': filtros_cat.id, 'peligroso': False},
        {'nombre': 'Kit Filtros Service 4 en 1 - VW Gol 1.6', 'precio': 5800.00, 'stock': 40, 'fk_categoria': filtros_cat.id, 'peligroso': False},
        {'nombre': 'Kit Filtros Service 4 en 1 - Fiat Palio 1.4', 'precio': 5500.00, 'stock': 35, 'fk_categoria': filtros_cat.id, 'peligroso': False},
        {'nombre': 'Kit Embrague Valeo - VW Gol 1.6', 'precio': 22000.00, 'stock': 15, 'fk_categoria': transmision_cat.id, 'peligroso': False},
        {'nombre': 'Kit Embrague Sachs - Fiat Palio 1.4', 'precio': 19500.00, 'stock': 12, 'fk_categoria': transmision_cat.id, 'peligroso': False},
        {'nombre': 'Kit Embrague LUK - Renault Clio 1.6', 'precio': 21000.00, 'stock': 10, 'fk_categoria': transmision_cat.id, 'peligroso': False},
        {'nombre': 'Homocinética Interior - VW Gol 1.6', 'precio': 8500.00, 'stock': 18, 'fk_categoria': transmision_cat.id, 'peligroso': False},
        {'nombre': 'Homocinética Exterior - Fiat Siena 1.6', 'precio': 9200.00, 'stock': 15, 'fk_categoria': transmision_cat.id, 'peligroso': False},
        {'nombre': 'Bota de Junta Homocinética Interior', 'precio': 2800.00, 'stock': 50, 'fk_categoria': transmision_cat.id, 'peligroso': False},
        {'nombre': 'Aceite Caja Manual 75W90 GL-4 - 1L', 'precio': 4500.00, 'stock': 60, 'fk_categoria': transmision_cat.id, 'peligroso': True},
        {'nombre': 'Bomba de Agua Dolz - VW Gol 1.6', 'precio': 5800.00, 'stock': 25, 'fk_categoria': refrigeracion_cat.id, 'peligroso': False},
        {'nombre': 'Bomba de Agua Dolz - Fiat 1.4', 'precio': 5200.00, 'stock': 22, 'fk_categoria': refrigeracion_cat.id, 'peligroso': False},
        {'nombre': 'Termostato Wahler - Renault 1.6', 'precio': 2800.00, 'stock': 40, 'fk_categoria': refrigeracion_cat.id, 'peligroso': False},
        {'nombre': 'Termostato 83° - Ford Ka 1.0 Zetec', 'precio': 2500.00, 'stock': 35, 'fk_categoria': refrigeracion_cat.id, 'peligroso': False},
        {'nombre': 'Radiador Aluminio - VW Gol 1.6 (AT/MT)', 'precio': 18500.00, 'stock': 10, 'fk_categoria': refrigeracion_cat.id, 'peligroso': False},
        {'nombre': 'Radiador Aluminio - Fiat Palio 1.4', 'precio': 16800.00, 'stock': 8, 'fk_categoria': refrigeracion_cat.id, 'peligroso': False},
        {'nombre': 'Tapa de Radiador 1.2 kg - Universal', 'precio': 1200.00, 'stock': 80, 'fk_categoria': refrigeracion_cat.id, 'peligroso': False},
        {'nombre': 'Anticongelante Orgánico Verde - 1L', 'precio': 2200.00, 'stock': 70, 'fk_categoria': refrigeracion_cat.id, 'peligroso': True},
        {'nombre': 'Manguera de Radiador Superior - VW Gol', 'precio': 1800.00, 'stock': 45, 'fk_categoria': refrigeracion_cat.id, 'peligroso': False},
        {'nombre': 'Electrovéntilador - Fiat Uno', 'precio': 9500.00, 'stock': 12, 'fk_categoria': refrigeracion_cat.id, 'peligroso': True},
        {'nombre': 'Bujías NGK BPR5ES x4 - Universal', 'precio': 3600.00, 'stock': 100, 'fk_categoria': encendido_cat.id, 'peligroso': False},
        {'nombre': 'Bujías Iridium NGK - VW Gol 1.6', 'precio': 7200.00, 'stock': 60, 'fk_categoria': encendido_cat.id, 'peligroso': False},
        {'nombre': 'Bujías Platino Bosch - Fiat 1.4 Fire', 'precio': 6500.00, 'stock': 55, 'fk_categoria': encendido_cat.id, 'peligroso': False},
        {'nombre': 'Cables de Bujías Bosch - VW Gol 1.6', 'precio': 4800.00, 'stock': 40, 'fk_categoria': encendido_cat.id, 'peligroso': False},
        {'nombre': 'Cables de Bujías NGK - Fiat Palio 1.6', 'precio': 4500.00, 'stock': 35, 'fk_categoria': encendido_cat.id, 'peligroso': False},
        {'nombre': 'Rotor de Distribuidor - Renault 1.6', 'precio': 1500.00, 'stock': 40, 'fk_categoria': encendido_cat.id, 'peligroso': False},
        {'nombre': 'Tapa de Distribuidor - Ford 1.8', 'precio': 2800.00, 'stock': 30, 'fk_categoria': encendido_cat.id, 'peligroso': False},
        {'nombre': 'Platinos de Encendido - Fiat Uno S', 'precio': 2200.00, 'stock': 25, 'fk_categoria': encendido_cat.id, 'peligroso': False},
        {'nombre': 'Inyector Limpio Bosch - Universal 250ml', 'precio': 3500.00, 'stock': 80, 'fk_categoria': encendido_cat.id, 'peligroso': True},
    ]

    for prod_info in productos:
        producto = Producto.query.filter_by(nombre=prod_info['nombre']).first()
        if not producto:
            producto = Producto(
                nombre=prod_info['nombre'],
                precio=prod_info['precio'],
                stock=prod_info['stock'],
                fk_categoria=prod_info['fk_categoria'],
                peligroso=prod_info['peligroso']
            )
            try:
                database.session.add(producto)
                database.session.commit()
            except Exception as e:
                print(f"❌ Error al crear producto {prod_info['nombre']}: {e}")
                database.session.rollback()
