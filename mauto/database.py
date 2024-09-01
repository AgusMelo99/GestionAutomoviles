from flask_mysqldb import MySQL

mysql = MySQL()


"""
    Configura y conecta la aplicación Flask con la base de datos MySQL. 
    :param app: La instancia de la aplicación Flask.
"""
def init_app(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_PORT'] = 3306
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'admin'
    app.config['MYSQL_DB'] = 'mauto'
    mysql.init_app(app)




"""
    Inserta un nuevo usuario en la base de datos MySQL.
    :param nombre: Nombre del usuario.
    :param apellido: Apellido del usuario.
    :param email: Correo electrónico del usuario.
    :param contrasena_hash: Contraseña encriptada del usuario.
"""
def crear_usuario(nombre, apellido, email, contrasena_hash):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios(nombre, apellido, email, contrasena) VALUES (%s, %s, %s, %s)", 
                (nombre, apellido, email, contrasena_hash))
    mysql.connection.commit()
    cur.close()