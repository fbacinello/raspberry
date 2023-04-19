#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import numpy as np
from datetime import datetime

import logger_csv


# -------  LOGGER METHODS -------

# Create a values dict to store the data
variables = ["distance", "litros"]
values_dic = {}

# Saves the data into an array
def save_data(idx, data):
    variable = variables[idx]
    # Maintain length of list and add the new value
    values_dic[variable] = np.append(values_dic[variable][1:], [data])

def save_all_data(distance, litros):
    save_data(0, distance)
    save_data(1, litros)

def log():
    logger = logger_csv.Logger()
    
    dic_log = {'time': datetime.now(),
               'distance': values_dic['distance'][-1],
               'litros': values_dic['litros'][-1]}
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

    return cant_litros

try:
      inicializar_variables_data()
      
      GPIO.setmode(GPIO.BOARD)

      PIN_TRIGGER = 7
      PIN_ECHO = 11

      GPIO.setup(PIN_TRIGGER, GPIO.OUT)
      GPIO.setup(PIN_ECHO, GPIO.IN)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      print ('Waiting for sensor to settle')

      time.sleep(2)

      print ('Calculating distance')

      GPIO.output(PIN_TRIGGER, GPIO.HIGH)

      time.sleep(0.00001)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
      while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

      pulse_duration = pulse_end_time - pulse_start_time
      distance = round(pulse_duration * 17150, 2)
      print ('Distance:',distance,'cm')

      litros = calcular_litros_agua(distance)
      print ('Cant litros: ', litros, ' litros')
      
      save_all_data(distance, litros)
      log()

finally:
      GPIO.cleanup()