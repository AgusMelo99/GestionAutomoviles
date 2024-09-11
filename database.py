import mysql.connector as db
import mysql.connector.errorcode
import re
from datetime import datetime

class ConexionBD:

    def __init__(self, host, port, user, password, database, bcrypt):

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.bcrypt = bcrypt
        
        self.mydb = db.connect(host= self.host, port= self.port, user=self.user, password=self.password)
        self.cur = self.mydb.cursor()

        try: #seleccionamos la base de datos a usar
            self.cur.execute(f"USE {database}")
        except db.Error as err: #si no lo encuentra, lo creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cur.execute(f"CREATE DATABASE {database}")
                self.mydb.database = database
            else:
                raise err

        #creamos la tabla de usuarios
        self.cur.execute('''CREATE TABLE IF NOT EXISTS usuarios(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(30) NOT NULL,
            apellido VARCHAR(30) NOT NULL,
            email VARCHAR(50) NOT NULL,
            contrasena VARCHAR(90) NOT NULL
            )''')
        
        self.mydb.commit()

        #creamos la table de autos
        self.cur.execute('''CREATE TABLE IF NOT EXISTS automoviles(
            id_auto INT AUTO_INCREMENT PRIMARY KEY,
            modelo VARCHAR(30) NOT NULL,
            patente VARCHAR(10) NOT NULL,
            dueno INT NOT NULL,
            FOREIGN KEY (dueno) REFERENCES usuarios(id)
            )''')
        
        self.mydb.commit()

        #creamos la tabla de mantenimientos
        self.cur.execute('''CREATE TABLE IF NOT EXISTS mantenimientos(
            id_control INT AUTO_INCREMENT PRIMARY KEY,
            control VARCHAR(100) NOT NULL,
            fecha DATE NOT NULL,
            prox_control DATE,
            auto INT NOT NULL,
            FOREIGN KEY (auto) REFERENCES automoviles(id_auto)
            )''')
        
        self.mydb.commit()

        self.cur.close()
        self.cur = self.mydb.cursor(dictionary=True)
    
    def _open_connection(self):
        self.mydb = db.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cur = self.mydb.cursor(dictionary=True)

    def _close_connection(self):
        self.cur.close()
        self.mydb.close()

    #metodos CREATE
    def crear_usuario(self, nombre, apellido, email, contrasena):

        if not self.validar_nombre_apellido(nombre):
            raise ValueError("El nombre solo debe contener letras y espacios")
        
        if not self.validar_nombre_apellido(apellido):
            raise ValueError("El apellido solo debe contener letras y espacios")

        if not self.validar_email(email):
            raise ValueError("Email inválido")
        
        if not self.validar_contrasena(contrasena):
            raise ValueError("La contraseña debe tener al menos 8 caracteres, incluyendo letras y números")
        
        # Validar si el email ya está registrado
        self._open_connection()
        self.cur.execute("SELECT COUNT(*) FROM usuarios WHERE email = %s", (email,))
        resultado = self.cur.fetchone()
        if resultado['COUNT(*)'] > 0:
            self._close_connection()
            raise ValueError("El email ya está registrado")
        
        contrasena_hash = self.bcrypt.generate_password_hash(contrasena).decode('utf-8')  # Generar hash de la contraseña
        
        self.cur.execute("INSERT INTO usuarios(nombre, apellido, email, contrasena) VALUES (%s, %s, %s, %s)", 
            (nombre, apellido, email, contrasena_hash))
        self.mydb.commit()
        self._close_connection()

    def cargar_auto(self, modelo, patente, dueno):

        if not modelo or not patente or not dueno:
            raise ValueError("Todos los campos son requeridos")
        
        if not self.validar_patente(patente):
            raise ValueError("Formato de patente inválido")
        
        # Validar si la patente ya existe en la base de datos
        self._open_connection()
        self.cur.execute("SELECT COUNT(*) FROM automoviles WHERE patente = %s", (patente,))
        resultado = self.cur.fetchone()
        if resultado['COUNT(*)'] > 0:
            self._close_connection()
            raise ValueError("La patente ya está registrada")
        
        self.cur.execute("INSERT INTO automoviles(modelo, patente, dueno) VALUES (%s, %s, %s)",
            (modelo, patente, dueno))
        self.mydb.commit()
        self._close_connection()

    def auto_existe(self, auto_id):
        self._open_connection()
        self.cur.execute("SELECT COUNT(*) FROM automoviles WHERE id_auto = %s", (auto_id,))
        resultado = self.cur.fetchone()
        self._close_connection()
    
        # Verifica que el resultado no sea None y que contiene datos
        if resultado:
            existe = resultado[0] > 0
        else:
            existe = False
    
        return existe



    def cargar_mantenimiento(self, control, fecha, prox_control, auto):
        if not control or not fecha or not prox_control or not auto:
            raise ValueError("Todos los campos son requeridos")
        
        try:
            fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
            prox_control_dt = datetime.strptime(prox_control, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Formato de fecha inválido")
    
        if prox_control_dt < fecha_dt:
            raise ValueError("La fecha del próximo control no puede ser anterior a la fecha actual")
        
        self._open_connection()
        query = 'INSERT INTO mantenimientos (control, fecha, prox_control, auto) VALUES (%s, %s, %s, %s)'
        self.cur.execute(query, (control, fecha, prox_control, auto))
        self.mydb.commit()
        self._close_connection()



    #metodos READ
    def consultar_usuario(self, email):
        self._open_connection()
        self.cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        result = self.cur.fetchone()
        self._close_connection()
        return result

    def consultar_autos(self, usuario):
        self._open_connection()
        self.cur.execute('SELECT * FROM automoviles WHERE dueno = %s', (usuario,))
        result = self.cur.fetchall()
        self._close_connection()
        return result
    
    def consultar_mantenimientos(self, auto):
        self._open_connection()
        self.cur.execute('SELECT * FROM mantenimientos WHERE auto = %s', (auto,))
        result = self.cur.fetchall()
        self._close_connection()
        return result
    
    #metodos UPDATE 
    
    def validar_patente(self, patente):
        # Validar formato de patente (ejemplo: ABC123 o AB123CD)
        return re.match(r"^[A-Z]{3}[0-9]{3}$|^[A-Z]{2}[0-9]{3}[A-Z]{2}$", patente) is not None

    def validar_email(self, email):
        # Validar formato de email
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def validar_nombre_apellido(self, nombre_apellido):
        # Validar que solo contenga letras y espacios
        return re.match(r"^[a-zA-Z\s]+$", nombre_apellido) is not None

    def validar_contrasena(self, contrasena):
        # Validar que la contraseña tenga al menos 8 caracteres, incluyendo letras y números
        return re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", contrasena) is not None