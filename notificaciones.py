import mysql.connector as db
from config import Config
from datetime import date, timedelta

import smtplib 
from email.message import EmailMessage

def mensaje(destinatario, mensaje):
    email_subject = "Mauto - Control proximo" 
    sender_email_address = "nizares97@gmail.com" 
    receiver_email_address = destinatario
    email_smtp = "smtp.gmail.com" 
    email_password = "kvyj dxvg ubnt yhda" 

    # instancia el objeto
    message = EmailMessage() 

    # configura los datos del mail
    message['Subject'] = email_subject 
    message['From'] = sender_email_address 
    message['To'] = receiver_email_address 

    # agrega el cuerpo del mensaje
    message.set_content(mensaje) 

    # habilita la conexion con el servidor smtp
    server = smtplib.SMTP(email_smtp, '587') 

    server.ehlo() 

    server.starttls() 

    # login a la cuenta a usar
    server.login(sender_email_address, email_password) 

    # envia el mail y cierra la conexion
    server.send_message(message) 

    server.quit()


hoste = Config.MYSQL_HOST
puerto = Config.MYSQL_PORT
usuario = Config.MYSQL_USER
contra = Config.MYSQL_PASSWORD
base = Config.MYSQL_DB

conexion = db.connect(host= hoste, port= puerto, user= usuario, password= contra, database= base)

cur = conexion.cursor(dictionary=True)


#levanto la info de los usuarios
cur.execute('SELECT  id, nombre, email from usuarios')
mails = cur.fetchall()


#me armo un rango de fechas los proximos 3 dias
hoy = date.today()
hasta =  hoy + timedelta(days= 3)


#levanto todos los mantenimientos y datos del auto que estan en el rango
cur.execute('''
            select a.dueno, a.modelo, a.patente, m.control, m.fecha 
            from mantenimientos m, automoviles a 
            where m.auto = a.id_auto and fecha between %s and %s 
            ''', 
            (str(hoy), str(hasta)))

pendientes = cur.fetchall()

#recorre los mantenimientos pendientes y genera los datos a enviar
for i in pendientes:
    for j in mails:
        if i['dueno'] == j['id']:
            destinatario = j['email']
            contenido = f'Le enviamos este correo para avisarle que en unos dias su  auto {i['patente']} - modelo {i['modelo']} debera hacer un control.
                        En esta ocasion debe hacer {i['control']}, para el proximo {i['fecha']}, le recomendamos hacerlo lo antes posible para asegurar que no haya imprevistos con su vehiculo.
                        No olvide anotar los resultados y asegurar un turno para el proximo control.
                        
                        Mauto'
            
            mensaje(destinatario, contenido)
            
        break


