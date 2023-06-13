# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import network

# IMPORTACION DEL SOCKET
try:
  import usocket as socket
except:
  import socket

#ACCESS POINT
def crearAccessPoint():
    # Configurar el nombre de la red y la contraseña del punto de acceso
    ssid = 'jerryESP32'
    passwo = 'contrasena123'
    # Configurar el modo de red en modo AP
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=passwo)
    # Obtener y mostrar la dirección IP del punto de acceso
    ip_address = ap.ifconfig()[0]
    print('Punto de acceso IP:', ip_address)


# CONEXION A WIFI
def conectarWifi():
    # Nombre de tu red Wi-Fi y contraseña
    ssid = "ATEHORTUA"
    password = "AdriLeo43594"
    # Configuración de la conexión Wi-Fi
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    # Esperar a que se establezca la conexión
    while not sta_if.isconnected():
        pass
    # Imprimir información de conexión
    print("Conexión Wi-Fi establecida")
    print("Dirección IP:", sta_if.ifconfig()[0])

conectarWifi()