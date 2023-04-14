#!/usr/bin/python
import RPi.GPIO as GPIO
import time

import logger_csv

# Create a values dict to store the data
variables = ["distance"]
values_dic = {}


# Saves the data into an array
def save_data(idx, data):
    variable = variables[idx]
    # Maintain length of list and add the new value
    values_dic[variable] = np.append(values_dic[variable][1:], [data])


def save_all_data(distance):
    save_data(0, distance)

def log():
    logger = logger_csv.Logger()
    
    dic_log = {'time': datetime.now(),
               'distance': values_dic['distance'][-1]}
    logger.collect_data('water_level', dic_log)
    logger.log_data()

def inicializar_variables_data():
    for v in variables:
        values_dic[v] = np.ones(160)



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
      
      save_all_data(distance)

finally:
      GPIO.cleanup()