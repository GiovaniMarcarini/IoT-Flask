import RPi.GPIO as gpio
import time as delay
import Adafruit_DHT as dht
from flask import render_template
from app import app

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

ledVermelho, ledVerde = 11, 12

pin_t, pin_e = 15, 16

#tamanho da lixeira
lixeira = 20

#pinos do sensor DHT
pin_dht = 4
dht_sensor = dht.DHT11

statusVermelho = ''
statusVerde = ''

gpio.setup(ledVermelho, gpio.OUT)
gpio.setup(ledVerde, gpio.OUT)
gpio.setup(pin_t, gpio.OUT)
gpio.setup(pin_e, gpio.IN)

gpio.output(ledVermelho, gpio.LOW)
gpio.output(ledVerde, gpio.LOW)

def status_led_vermelho():
    if gpio.input(ledVermelho) == 1:
        statusVermelho = 'LED vermelho ON'
    else:
        statusVermelho = 'LED vermelho OFF'
    
    return statusVermelho

def status_led_verde():
    if gpio.input(ledVerde) == 1:
        statusVerde= 'LED verde ON'
    else:
        statusVerde = 'LED verde OFF'
    
    return statusVerde

def umid_temp():
    umid, temp = dht.read(dht_sensor, pin_dht)
    if umid is not None:
        umidade = ('{0:0.0f}%'.format(umid))
    else:
        umidade = 'Erro ao ler sensor'

    if temp is not None:
        temperatura = ('{0:0.0f}*C'.format(temp))
    else:
        temperatura = 'Erro ao ler sensor'

    return umidade, temperatura

def ocupacao_lixeira():
    gpio.output(pin_t, True)
    delay.sleep(0.000001)
    gpio.output(pin_t, False)
    tempo_i = delay.time()
    tempo_f = delay.time()

    while gpio.input(pin_e) == False:
        tempo_i = delay.time()
    while gpio.input(pin_e) == True:
        tempo_f = delay.time()
    
    tempo_d = tempo_f - tempo_i
    distancia = (tempo_d * 34300)/2
    ocupacao_l = (distancia/lixeira)*100

    if ocupacao_l < 0:
        ocupacao_l = 0
    ocupacao_f = 100 - ocupacao_l

    ocupacao_lixeira = ('{0:0.0f}%'.format(ocupacao_f))

    return ocupacao_lixeira

@app.route("/")
def index():
    templateData = {
        'ledRed' : status_led_vermelho(),
        'ledGreen': status_led_verde(),
        'umid' : umid_temp()[0],
        'temp': umid_temp()[1],
        'ocup_lixeira' : ocupacao_lixeira()
    }
    return render_template('index.html', **templateData)

@app.route("/led_vermelho/<action>")
def led_vermelho(action):
    if action == 'on':
        gpio.output(ledVermelho, gpio.HIGH)
    if action == 'off':
        gpio.output(ledVermelho, gpio.LOW)
    
    templateData = {
        'ledRed' : status_led_vermelho(),
        'ledGreen': status_led_verde(),
        'umid' : umid_temp()[0],
        'temp': umid_temp()[1],
        'ocup_lixeira' : ocupacao_lixeira()
    }
    return render_template('index.html', **templateData)

@app.route("/led_verde/<action>")
def led_verde(action):
    if action == 'on':
        gpio.output(ledVerde, gpio.HIGH)
    if action == 'off':
        gpio.output(ledVerde, gpio.LOW)
    
    templateData = {
        'ledRed' : status_led_vermelho(),
        'ledGreen': status_led_verde(),
        'umid' : umid_temp()[0],
        'temp': umid_temp()[1],
        'ocup_lixeira' : ocupacao_lixeira()
    }
    return render_template('index.html', **templateData)
