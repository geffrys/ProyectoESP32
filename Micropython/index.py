import time
import urequests
import ujson
import machine

BMP280_ADDRESS = 0x76

t_fine = 0

scl_pin = machine.Pin(22)
sda_pin = machine.Pin(21)

# Crea una instancia del objeto I2C
i2c = machine.SoftI2C(scl=scl_pin, sda=sda_pin)

# Leer valores de compensación del sensor BMP280
def read_calibration():
    calibration = bytearray(24)
    i2c.readfrom_mem_into(BMP280_ADDRESS, 0x88, calibration)
    return calibration


def read_temperature(calibration):
    raw_data = i2c.readfrom_mem(BMP280_ADDRESS, 0xFA, 3)
    adc_T = (raw_data[0] << 16) | (raw_data[1] << 8) | raw_data[2]
    var1 = ((((adc_T >> 3) - (calibration[0] << 8))) * (calibration[1])) >> 11
    var2 = (
        (
            (((adc_T >> 4) - (calibration[0] << 8)))
            * ((adc_T >> 4) - (calibration[0] << 8))
        )
        >> 12
    ) * (calibration[2]) >> 14
    t_fine = var1 + var2
    temperature = (t_fine * 5 + 128) >> 8
    return temperature / 100.0


def read_pressure(calibration, t_fine):
    #raw_data = i2c.readfrom_mem(BMP280_ADDRESS, 0xF7, 3)
    #adc_P = (raw_data[0] << 16) | (raw_data[1] << 8) | raw_data[2]
    var1 = t_fine - 128000
    var2 = var1 * var1 * calibration[5]
    var2 = var2 + ((var1 * calibration[4]) << 17)
    var2 = var2 + ((calibration[3] * 131072) >> 1)
    var1 = ((var1 * var1 * calibration[2]) >> 15) * 2
    var1 = (var1 >> 2) + ((calibration[1] << 16) + (calibration[0] << 9))
    pressure = (((var1 + var2) >> 12) * 100) >> 8
    return pressure


# Leer los valores de compensación
calibration = read_calibration()

# Configuracion de la base de datos

import urequests
import ujson

def send_data_to_database(temperature, presion, humedad):

    payload = {'temperatura': temperature, 'presion': presion, 'humedad': humedad}
    print(payload)
    json_data = ujson.dumps(payload)
    print(json_data)
    resp = urequests.post('http://localhost:3000/medicion', json=json_data, timeout=10, data=json_data)
    print("response: ", resp.text)
    resp.close()

while True:

    temperatura = read_temperature(calibration)
    presion = read_pressure(calibration, t_fine)
    humedad = 0
    send_data_to_database(temperatura, presion, humedad)
    time.sleep(60)  # Espera 60 segundos
