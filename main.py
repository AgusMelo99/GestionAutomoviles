from flask import Flask, render_template, request, redirect, url_for, flash, session

from werkzeug.security import generate_password_hash, check_password_hash

from config import Config

from database import *

#instancia de la app
app = Flask(__name__, template_folder='front/html', static_folder='front/static')
 
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

    # Verifica si se han completado todos los campos del formulario
    if not email or not contrasena:
        flash('Por favor, complete todos los campos', 'error')
        return redirect(url_for('inicio'))
    
    # Consulta el usuario en la base de datos usando el email proporcionado
    usuario = db.consultar_usuario(email)
    print(f"Usuario encontrado: {usuario}")  # Debugging
    
    # Verificar la contraseña
    if usuario and check_password_hash(usuario['contrasena'], contrasena):
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
    contrasena = str(generate_password_hash(request.form['contrasena']))

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
    return render_template('misAutos.html')

@app.route('/mantenimientos')
def mantenimientos():
    return render_template('mantenimientos.html')


#ejecucion de la app
if __name__ == '__main__':
    app.run(debug=True)
