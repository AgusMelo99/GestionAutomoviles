from flask import Flask, render_template, request, redirect, url_for, flash

from database import crear_usuario, init_app

from werkzeug.security import generate_password_hash

from config import Config

app = Flask(__name__, template_folder='front/html', static_folder='front/static')
app.config.from_object(Config)
 
# Inicialización de la base de datos MySQL
init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']
        #lógica de autenticación
        #se guardan las variables mail y contrasena asi las usamos en la DB
        return redirect(url_for('index'))
    return render_template('inicio.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        contrasena = generate_password_hash(request.form['contrasena'])
        #lógica de registro
        #lo mismo que en def inicio pero con registro

        crear_usuario(nombre, apellido, email, contrasena)
        flash('Usuario registrado exitosamente', 'success')

        return redirect(url_for('index'))
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)
