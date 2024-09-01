from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='front/html', static_folder='front/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        #lógica de autenticación
        #se guardan las variables mail y contraseña asi las usamos en la DB
        return redirect(url_for('index'))
    return render_template('inicio.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        contraseña = request.form['contraseña']
        #lógica de registro
        #lo mismo que en def inicio pero con registro
        return redirect(url_for('index'))
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)
