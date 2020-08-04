#!/usr/bin/env python3

import time
import colorsys
import sys
import logging
import logger_csv
from datetime import datetime
from time import sleep
import threading
from random import randint
import display
import sensors

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""all-in-one.py - Displays readings from all of Enviro plus' sensors

Press Ctrl+C to exit!

""")

message = ""


# Create a values dict to store the data
variables = ["temperature",
             "pressure",
             "humidity",
             "light"]

units = ["C",
         "hPa",
         "%",
         "Lux"]

# Define your own warning limits
# The limits definition follows the order of the variables array
# Example limits explanation for temperature:
# [4,18,28,35] means
# [-273.15 .. 4] -> Dangerously Low
# (4 .. 18]      -> Low
# (18 .. 28]     -> Normal
# (28 .. 35]     -> High
# (35 .. MAX]    -> Dangerously High
# DISCLAIMER: The limits provided here are just examples and come
# with NO WARRANTY. The authors of this example code claim
# NO RESPONSIBILITY if reliance on the following values or this
# code in general leads to ANY DAMAGES or DEATH.
limits = [[4, 18, 28, 35],
          [250, 650, 1013.25, 1015],
          [20, 30, 60, 70],
          [-1, -1, 30000, 100000]]

# RGB palette for values on the combined screen
palette = [(0, 0, 255),           # Dangerously Low
           (0, 255, 255),         # Low
           (0, 255, 0),           # Normal
           (255, 255, 0),         # High
           (255, 0, 0)]           # Dangerously High

values = {}

#Logger
LOG = False

# Saves the data to be used in the graphs later and prints to the log
def save_data(idx, data):
    variable = variables[idx]
    # Maintain length of list
    values[variable] = values[variable][1:] + [data]
    unit = units[idx]
    message = "{}: {:.1f} {}".format(variable[:4], data, unit)
    # logging.info(message)

def main():
    #t_logger = threading.Thread(target=retardar_logger)
    #t_logger.start()

    sensor = Sensors()
    display = Display()


    delay = 0.5  # Debounce the proximity tap
    mode = 10     # The starting mode
    last_page = 0

    for v in variables:
        values[v] = [1] * 160

    # The main loop
    try:
        while True:
            # Everything on one screen
            raw_data= sensor.get_temperature()
            save_data(0, raw_data)
            display.display_everything(variables)
            raw_data = sensor.get_pressure()
            save_data(1, raw_data)
            display.display_everything(variables)
            # if LOG:
            #     log()
            raw_data = sensor.get_humidity()
            save_data(2, raw_data)
            if proximity < 10:
                raw_data = sensor.get_lux()
            else:
                raw_data = 1
            save_data(3, raw_data)
            display.display_everything(variables)

    # Exit cleanly
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()
