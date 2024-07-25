#!/usr/bin/python
import RPi.GPIO as GPIO
import numpy as np
from datetime import datetime

import sys
import os


import epd2in9_V2
import time
import logging

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

logging.basicConfig(level=logging.DEBUG)

import logger_csv

PANTALLA = False
if PANTALLA:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# -------  LOGGER METHODS -------

# Create a values dict to store the data
variables = ["distance", "litros", "litrosTotales"]
values_dic = {}


# Saves the data into an array
def save_data(idx, data):
    variable = variables[idx]
    # Maintain length of list and add the new value
    values_dic[variable] = np.append(values_dic[variable][1:], [data])


def save_all_data(distance, litros, litrosTotales):
    save_data(0, distance)
    save_data(1, litros)
    save_data(1, litrosTotales)


def log():
    logger = logger_csv.Logger()
    
    dic_log = {'time': datetime.now(),
               'distance': values_dic['distance'][-1],
               'litros': values_dic['litros'][-1],
               'litrosTotales': values_dic['litrosTotales'][-1]}
    
    logging.info(dic_log)
    print(dic_log)
    logger.collect_data('water_level', dic_log)
    logger.log_data()


def inicializar_variables_data():
    for v in variables:
        values_dic[v] = np.ones(160)

# ---------------------------------


def calcular_litros_agua(medicion_sensor):
    dist_sensor_tope = 15
    capacidad_tanque = 1000
    distancia_entre_100_litros = 17

    cant_litros = capacidad_tanque - (((medicion_sensor - dist_sensor_tope)/distancia_entre_100_litros)*100)
    return round(cant_litros, 0)


def medir_distancia():
    print('Calculating distance')
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    return round(pulse_duration * 17150, 2)


def mostrar_en_pantalla(text_distance, text_litros, girar_180_grados = False):
    print('Imprimiendo pantalla')
    fem_jpg = Image.open(os.path.join(picdir, 'fem.jpg'))
    image = Image.new('1', (epd.height, epd.width), 0)
    fem_jpg = fem_jpg.resize((296, 128))
    fem_jpg = ImageEnhance.Contrast(fem_jpg)
    fem_jpg = fem_jpg.enhance(2)
    image.paste(fem_jpg, (0, 0))
    # print('Imprimir solo FEM')
    # epd.display(epd.getbuffer(image))

    print('Imprimir datos')
    draw = ImageDraw.Draw(image)
    draw.text((2, 90), text_distance, font=font18, fill=1)
    draw.text((2, 108), text_litros, font=font18, fill=1)

    if girar_180_grados:
        image = image.transpose(method=Image.ROTATE_180)

    #epd.display(epd.getbuffer(image))


try:
    if PANTALLA:
        logging.info("epd2in9 V2 Demo")
        epd = epd2in9_V2.EPD()

        logging.info("epd2in9 - Init and Clear")
        epd.init()
        epd.Clear(0xFF)

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    inicializar_variables_data()
      
    GPIO.setmode(GPIO.BOARD)

    PIN_TRIGGER = 15 
    PIN_ECHO = 13 

    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    print('Waiting for sensor to settle')
    time.sleep(2)

    while True:
        distance = medir_distancia()
        text_distance = "Distancia: {} cm".format(distance)
        print(text_distance)

        litros = calcular_litros_agua(distance)
        litrosTotales = litros*6
        text_litros = "Litros: {} x barril - {} total".format(litros, litrosTotales)
        print(text_litros)

        save_all_data(distance, litros, litrosTotales)
        log()

        if PANTALLA:
            mostrar_en_pantalla(text_distance, text_litros)

        time.sleep(60)

finally:
      GPIO.cleanup()
