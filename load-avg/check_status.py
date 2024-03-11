import subprocess
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Función para enviar un correo electrónico
def send_email(subject, body):
    sender_email = "Un nombre cualquiera <unemail@blaster.com.ar>"
    receiver_email = "unemail@blaster.com.ar"

    # Configuración del servidor SMTP de Amazon SES
    smtp_server = "smtp.algo.com"
    smtp_port = 587
    smtp_username = "unusuario"
    smtp_password = "unpassowrd"

    # Crear el objeto del mensaje
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Agregar el cuerpo del mensaje
    message.attach(MIMEText(body, "plain"))

    # Iniciar la conexión con el servidor SMTP y enviar el correo electrónico
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Función para obtener la carga del sistema
def get_system_load():
    try:
        # Ejecutar el comando uptime y capturar la salida
        result = subprocess.run(["uptime"], capture_output=True, text=True, check=True)
        output_lines = result.stdout.splitlines()

        # Obtener los valores de carga desde la salida del comando
        load_values = [float(value) for value in output_lines[0].split(":")[-1].strip().split(",")]

        return load_values

    except subprocess.CalledProcessError as e:
        print(f"Error al obtener la carga del sistema: {e}")
        return None

# Obtener la dirección IP local
def get_local_ip():
    try:
        # Crear un socket y obtener la dirección IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error as e:
        print(f"Error al obtener la dirección IP local: {e}")
        return None

# Obtener el nombre del hostname local
def get_hostname():
    try:
        # Obtener el nombre del hostname local
        hostname = socket.gethostname()
        return hostname
    except socket.error as e:
        print(f"Error al obtener el nombre del hostname local: {e}")
        return None

# Umbral de carga para generar una alerta
umbral_carga = 5.0

# Obtener la carga del sistema
load_average = get_system_load()

# Obtener la dirección IP local
local_ip = get_local_ip()

# Obtener el nombre del hostname local
hostname = get_hostname()

reporte = f"Maximo {umbral_carga}. Load average: {', '.join(map(str, load_average))}\nDirección IP local: {local_ip}\nHostname local: {hostname}"

print(reporte)

if load_average is not None and any(value > umbral_carga for value in load_average):
    # Enviar una alerta por correo electrónico
    subject = "Alerta de carga del sistema"
    body = f"La carga del sistema ha superado el umbral establecido de {umbral_carga}. Load average: {', '.join(map(str, load_average))}\nDirección IP local: {local_ip}\nHostname local: {hostname}"
    send_email(subject, body)
    print(body)
