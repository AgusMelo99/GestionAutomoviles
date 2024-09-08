from flask import Flask, render_template, request, redirect, url_for, flash, session

from flask_bcrypt import Bcrypt

from config import Config

from database import *

from datetime import datetime

#instancia de la app
app = Flask(__name__, template_folder='front/html', static_folder='front/static')

flask_bcrypt = Bcrypt(app)

# instancia de la base de datos

db = ConexionBD(Config.MYSQL_HOST,
                Config.MYSQL_PORT,
                Config.MYSQL_USER,
                Config.MYSQL_PASSWORD,
                Config.MYSQL_DB)

# Configurar la clave secreta
app.config['SECRET_KEY'] = Config.SECRET_KEY

#ruta de pagina principal
@app.route('/')
def index():
    return render_template('index.html')

#ruta para iniciar sesion
@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    if request.method == 'GET':
        return render_template('inicio.html')
    
    email = str(request.form['email'])
    contrasena = str(request.form['contrasena'])
    
    # Consulta el usuario en la base de datos usando el email proporcionado
    usuario = db.consultar_usuario(email)

    verificacion = flask_bcrypt.check_password_hash(usuario['contrasena'], contrasena)

    # Verificar la contraseña
    if usuario and verificacion:
        # Contraseña correcta, redirigir al usuario a la página principal
        session['user_id'] = usuario['id']
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('principal'))
        
    else:
        # Autenticación fallida
        flash('Email o contraseña incorrectos', 'error')
        return redirect(url_for('inicio'))
    

#ruta para registrar cuenta
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template('registro.html')
    
    #estandarizamos los datos para usarlos
    nombre = str(request.form['nombre'])
    apellido = str(request.form['apellido'])
    email = str(request.form['email'])

    contrasena = flask_bcrypt.generate_password_hash(request.form['contrasena']).decode("utf-8")

    #logica de registro
    db.crear_usuario(nombre, apellido, email, contrasena)

    flash('Usuario registrado exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/agregarAutomovil' ,methods=['GET','POST'])
def agregarAutomovil():
    if request.method == 'POST':
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        anio = request.form.get('anio')
        vin = request.form.get('vin')
        kilometraje = request.form.get('kilometraje')
        combustible = request.form.get('combustible')

        #logica de registro
         # Obtener el ID del usuario desde la sesión
        user_id = session.get('user_id')
        
        if user_id:
            # Lógica de registro
            db.cargar_auto(modelo, vin, user_id)
            flash('Automóvil registrado exitosamente', 'success')
        else:
            flash('Debe iniciar sesión para registrar un automóvil', 'error')
            return redirect(url_for('inicio'))
        
        return redirect(url_for('principal'))
    
    return render_template('agregarAutomovil.html')

@app.route('/principal')    
def principal():
    return render_template('principal.html')

@app.route('/misAutos')
def misAutos():
    user_id = session.get('user_id')
    if user_id:
        autos = db.consultar_autos(user_id)
        return render_template('misAutos.html', autos=autos)
    else:
        flash('Debe iniciar sesión para ver sus automóviles', 'error')
        return redirect(url_for('inicio'))

@app.route('/mantenimientos/<int:auto_id>')
def mantenimientos(auto_id):
    # Conectar a la base de datos
    mantenimientos = db.consultar_mantenimientos(auto_id)
    # Renderizar la plantilla HTML y pasar los mantenimientos como contexto
    return render_template('mantenimientos.html', mantenimientos=mantenimientos, auto_id=auto_id)

@app.route('/agregarMantenimiento/<int:auto_id>', methods=['GET', 'POST'])
def agregarMantenimiento(auto_id):
    user_id = session.get('user_id')
    
    if not user_id:
        flash('Debe iniciar sesión para agregar un mantenimiento', 'error')
        return redirect(url_for('inicio'))
    
    if request.method == 'POST':
        control = request.form.get('control')
        fecha = request.form.get('fecha')
        prox_control = request.form.get('prox_control')

        try:
            if control and fecha and prox_control:
                fecha = datetime.strptime(fecha, '%Y-%m-%d')
                prox_control = datetime.strptime(prox_control, '%Y-%m-%d')
    
                if prox_control < fecha:
                    flash('La fecha del próximo control no puede ser anterior a la fecha actual', 'error')
                    return redirect(url_for('agregarMantenimiento', auto_id=auto_id))
                # Usar auto_id pasado en la URL
                db.cargar_mantenimiento(control, fecha, prox_control, auto_id)
                flash('Mantenimiento registrado exitosamente', 'success')
                return redirect(url_for('mantenimientos',auto_id=auto_id))
            else:
                flash('Todos los campos son requeridos', 'error')
                return redirect(url_for('agregarMantenimiento', auto_id=auto_id))
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('agregarMantenimiento', auto_id=auto_id))
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'error')
            return redirect(url_for('agregarMantenimiento', auto_id=auto_id))
    
    return render_template('agregarMantenimiento.html', auto_id=auto_id)

# Nueva ruta para cerrar sesión
@app.route('/logout')
def logout():
    # Eliminar la información de sesión del usuario
    session.pop('user_id', None)
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))

#ejecucion de la app
if __name__ == '__main__':
    app.run(debug=True)
