import RPi.GPIO as gpio 
import time as delay
from app import app
from flask import render_template

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

ledVermelho, ledVerde = 11, 12

statusVermelho = ""
statusVerde = ""

gpio.setup(ledVermelho, gpio.OUT)
gpio.setup(ledVerde, gpio.OUT)

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
        statusVerde = 'LED verde ON'
    else:
        statusVerde = 'LED verde OFF'

    return statusVerde

@app.route("/")
def index():
    templateData = {
        'ledRed': status_led_vermelho(),
        'ledGreen': status_led_verde()
    }
    return render_template('index.html', **templateData)

@app.route("/led_vermelho/<action>")
def led_vermelho(action):

    if action == 'on':
        gpio.output(ledVermelho, gpio.HIGH)
    if action == 'off':
        gpio.output(ledVermelho, gpio.LOW)
        
    templateData = {
        'ledRed': status_led_vermelho(),
        'ledGreen': status_led_verde()
    }
    return render_template('index.html', **templateData)
