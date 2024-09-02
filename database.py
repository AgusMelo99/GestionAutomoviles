import mysql.connector as db
import mysql.connector.errorcode

class ConexionBD:

    def __init__(self, host, port, user, password, database):
        self.mydb = db.connect(host= host, port= port, user= user, password= password)

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

    #metodos CREATE
    def crear_usuario(self, nombre, apellido, email, contrasena):
        self.cur.execute("INSERT INTO usuarios(nombre, apellido, email, contrasena) VALUES (%s, %s, %s, %s)", 
            (nombre, apellido, email, contrasena))
        self.mydb.commit()

    def cargar_auto(self, modelo, patente, usuario):
        self.cur.execute("INSERT INNTO automoviles(modelo, patente, usuario) VALUES (%s, %s, %s)",
            (modelo, patente, usuario))
        self.mydb.commit()

    def cargar_mantenimiento(self, control, fecha, prox_control, auto):
        self.cur.execute("INSERT INNTO mantenimientos(control, fecha, prox_control, auto) VALUES (%s, %s, %s, %s)",
            (control, fecha, prox_control, auto))
        self.mydb.commit()

    #metodos READ
    def consultar_usuario(self, email):
        self.cur.execute(f'SELECT * FROM usuarios WHERE email = {email}')
        return self.cur.fetchone

    def consultar_autos(self, usuario):
        self.cur.execute(f'SELECT * FROM autos WHERE dueno = {usuario}')
        return self.cur.fetchall
    
    def consultar_controles(self, auto):
        self.cur.execute(f'SELECT * FROM mantenimientos WHERE auto = {auto}')
        return self.cur.fetchall
    
    #metodos UPDATE
    
