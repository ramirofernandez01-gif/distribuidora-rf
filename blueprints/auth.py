from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from app.models import Usuario, database, bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/')
def index():
    return render_template('login.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Usuario.query.filter_by(email=email).first()
        
        if user:
            password_check = bcrypt.check_password_hash(user.password, password)
            
            if password_check:
                login_user(user)
                return redirect(url_for('main.home'))
            else:
                return render_template('login.html', error="Contraseña incorrecta")
        else:
            return render_template('login.html', error="Usuario no encontrado")
    return render_template('login.html')


@auth_bp.route('/singin', methods=['GET', 'POST'])
def singin():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        dni = request.form.get('dni')
        direccion = request.form.get('direccion')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        terms = request.form.get('terms')
        tipo_usuario = request.form.get('tipo_usuario')
        
        if not all([username, email, nombre, apellido, dni, direccion, password, confirm_password]):
            return render_template('singin.html', error="Todos los campos son obligatorios")
        
        if password != confirm_password:
            return render_template('singin.html', error="Las contraseñas no coinciden")
        
        if not terms:
            return render_template('singin.html', error="Debes aceptar los términos y condiciones")
        
        if not tipo_usuario:
            return render_template('singin.html', error="Debes seleccionar el tipo de usuario")
        
        try:
            dni_int = int(dni)
            if dni_int < 1000000 or dni_int > 99999999:
                return render_template('singin.html', error="El DNI debe tener entre 7 y 8 dígitos")
        except ValueError:
            return render_template('singin.html', error="El DNI debe ser un número válido")
        
        existing_user = Usuario.query.filter_by(username=username).first()
        if existing_user:
            return render_template('singin.html', error="El nombre de usuario ya existe")
            
        existing_email = Usuario.query.filter_by(email=email).first()
        if existing_email:
            return render_template('singin.html', error="El correo electrónico ya está registrado")
        
        existing_dni = Usuario.query.filter_by(dni=dni_int).first()
        if existing_dni:
            return render_template('singin.html', error="Ya existe un usuario registrado con este DNI")
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        es_empresa = True if tipo_usuario == 'empresa' else False
        
        new_user = Usuario(
            username=username,
            email=email,
            nombre=nombre,
            apellido=apellido,
            password=hashed_password,
            dni=dni_int,
            direccion=direccion,
            fk_tipousuario=2,
            tipo=es_empresa
        )
        
        try:
            database.session.add(new_user)
            database.session.flush()
            database.session.commit()
            
            return render_template('login.html', success="Registro exitoso. Ya puedes iniciar sesión con tu cuenta.")
            
        except Exception as e:
            database.session.rollback()
            
            return render_template('singin.html', error="Error al registrar usuario. Inténtalo de nuevo.")
    
    return render_template('singin.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
