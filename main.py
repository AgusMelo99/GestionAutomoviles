from flask import Flask, render_template, request, redirect, url_for, flash

from werkzeug.security import generate_password_hash

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

    #falta la logica para autenticar

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

#ejecucion de la app
if __name__ == '__main__':
    app.run(debug=True)
