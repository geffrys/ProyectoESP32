import time
import urequests
from machine import Pin,SoftI2C
import BME280

# DEFINICION DE VARIABLES CORRESPONDIENTES AL SENSOR

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
bme = BME280.BME280(i2c=i2c)

# LECTURA DEL SENSOR

def read_data_from_sensor():
    global temp, pressure, humidity
    temp = pressure = humidity = 0
    temp = bme.temperature
    pressure = bme.pressure
    humidity = bme.humidity

# Configuracion de la base de datos

def send_data_to_database():
    payload = {'temperatura': temp, 'presion': pressure, 'humedad': humidity}
    print(payload)
    resp = urequests.post('http://192.168.39.113:3001/medicion', json=payload, timeout=10)
    print("response: ", resp.text)
    resp.close()
    
# CUERPO DE LA PAGINA

def web_page():
  html = """<!DOCTYPE HTML><html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
      <style>
        html {
         font-family: Arial;
         display: inline-block;
         margin: 0px auto;
         text-align: center;
        }
        h2 { font-size: 3.0rem; }
        p { font-size: 3.0rem; }
        .units { font-size: 1.2rem; }
        .dht-labels{
          font-size: 1.5rem;
          vertical-align:middle;
          padding-bottom: 15px;
        }
      </style>
    </head>
    <body>
      <h2>ESP32 </h2>
      <p>
        <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
        <span class="dht-labels">Temperatura</span>
        <span>"""+str(temp)+"""</span>
      </p>
      <p>
        <i class="fas fa-tint" style="color:#00add6;"></i> 
        <span class="dht-labels">Presion</span>
        <span>"""+str(pressure)+"""</span>
      </p>
      <p>
        <i class="fas fa-tint" style="color:#00add6;"></i> 
        <span class="dht-labels">Humedad</span>
        <span>"""+str(humidity)+"""</span>
      </p>
      <script>
          setTimeout(function() {
            location.reload();
          }, 10000);
      </script>
      
    </body>
    </html>"""
  return html

# INICIALIZACION DE LOS SOCKETS DE CONEXION

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

#

def request_handler():
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  read_data_from_sensor()
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()

# BUCLE PRINCIPAL

while True:
    request_handler()
    send_data_to_database()
    # time.sleep(60)  # Espera 60 segundos
