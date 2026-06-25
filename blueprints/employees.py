from flask import Blueprint, render_template

employees_bp = Blueprint('employees', __name__, url_prefix='/admin/employees')

@employees_bp.route('/')
def list_employees():
    empleados = []
    return render_template('empleados.html', empleados=empleados)
