import time
import urequests
from machine import Pin,SoftI2C
import BME280
import ujson

# CONSTANTES

IPAPI = "http://192.168.39.113:3001"


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
    resp = urequests.post(IPAPI + '/medicion', json=payload, timeout=10)
    print("response: ", resp.text)
    resp.close()
    
# CUERPO DE LA PAGINA

def web_page(v):
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
      """
  if v:
      html = html + """
      <div>
        <p>Alerta los caracteres han variado</p>
        <p>""" + str(promediopresion) + """</p>
        <p>""" + str(promediotemp) +"""</p>
        <p>""" + str(promediohumedad) +"""</p>
    </div>
      
    """
  html = html + """      
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


# DESVIACIONES ESTANDAR
DESVIACIONTEMP = 2.0
DESVIACIONPRES = 2.0

# OBTENER EL PROMEDIO

def getProm():
    global promediopresion, promediotemp, promediohumedad
    promediopresion=promediotemp=promediohumedad=0
    promedio = 0.0
    response = urequests.get("" + str(IPAPI) + "/ultima-medicion")
    data = ujson.loads(response.content)
    print(data)
    promediopresion = data[0]['presion']
    promediotemp = data[0]['temperatura']
    promediohumedad = data[0]['humedad']
    print(promediopresion,promediotemp, promediohumedad)
    response.close()

def isVariacion():
    bandera = False
    promedioestandarpresion = promediopresion
    promedioestandartemp = promediotemp
    promedioestandarhumedad = promediohumedad
    valorPresion = float(pressure[0:len(pressure)-3])
    valorTemperatura = float(temp[0:len(temp)-1])
    valorHumedad = float(humidity[0:len(humidity)-1])
    print("promedio estandar PRESION antes de resta: ",promediopresion,"+",DESVIACIONPRES,"=",promedioestandarpresion)
    print("promedio estandar PRESION despues de resta: ",valorPresion,"-",promedioestandarpresion,"=", promedioestandarpresion - valorPresion)
    promedioestandarpresion =promedioestandarpresion - valorPresion
    print("promedio estandar PRESION despues de resta: ",valorTemperatura,"-",promedioestandartemp,"=", promedioestandartemp - valorTemperatura)
    promedioestandartemp = promedioestandartemp - valorTemperatura 
    print("promedio estandar PRESION despues de resta: ",valorHumedad,"-",promedioestandarhumedad,"=", promedioestandarhumedad - valorHumedad)
    promedioestandarhumedad = promedioestandarhumedad - valorHumedad
    resultado_presion = promedioestandarpresion > DESVIACIONPRES or promedioestandarpresion < (-1*(DESVIACIONPRES))
    resultado_temp = promedioestandartemp > DESVIACIONTEMP or promedioestandartemp < (-1*(DESVIACIONTEMP))
    resultado_humedad = promedioestandarhumedad > 0 or promedioestandarhumedad < 0
    if resultado_presion:
        bandera = True
    elif resultado_temp:
        bandera = True
    elif resultado_humedad:
        bandera = True
    return bandera

# PETICIONES GET A LA PAGINA

def request_handler(v):
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  # verificamos 
  response = web_page(v)
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()

# BUCLE PRINCIPAL

while True:
    read_data_from_sensor()
    getProm()
    isVarying = isVariacion()
    print('is varying: ',isVarying)
    request_handler(isVarying)
    send_data_to_database()
    # time.sleep(60)  # Espera 60 segundos
