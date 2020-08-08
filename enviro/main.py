#!/usr/bin/env python3

import sys
import logging
import logger_csv
from datetime import datetime
from time import sleep
import display as disp
import sensors
import threading

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

noise = [[0, 0, 0, 0]]

values = {}

# Logger
LOG = False


def log():
    global LOG
    logger = logger_csv.Logger()
    while LOG:
        dic_enviro = {'time': datetime.now(),
                      'temp': values['temperature'][-1],
                      'humi': values['humidity'][-1]}
        logger.collect_data('enviro_not_suav', dic_enviro)

        dic_enviro_suav = {'time': datetime.now(),
                           'temp': values['temperature'][-60:].mean(),
                           'humi': values['humidity'][-60:].mean()}
        logger.collect_data('dic_enviro_suav', dic_enviro_suav)

        # dic_noise = {'time': datetime.now(), '100-200': noise[0], '500-600': noise[1],
        #             '1000-1200': noise[2], '2000-3000': noise[3]}
        # logger.collect_data('noise', dic_noise)

        logger.log_data()
        print("Logging")
        sleep(60)


def retardar_logger():
    global LOG
    print("-" * 100)
    print("A MIMIRRRRRRRRRRRRRRRRRRR")
    print("-" * 100)
    #sleep(30)
    LOG = True
    t_logger = threading.Thread(target=log)
    t_logger.start()


# Saves the data to be used in the graphs later and prints to the log
def save_data(idx, data):
    variable = variables[idx]
    # Maintain length of list
    values[variable] = values[variable][1:] + [data]
    unit = units[idx]
    # message = "{}: {:.1f} {}".format(variable[:4], data, unit)
    # logging.info(message)


def main():
    global noise
    sensor = sensors.Sensors()
    display = disp.Display()

    t_logger = threading.Thread(target=retardar_logger)
    t_logger.start()

    for v in variables:
        values[v] = [1] * 160

    noise = noise*60

    # The main loop
    try:
        while True:
            # Everything on one screen
            raw_data = sensor.get_temperature()
            save_data(0, raw_data)

            display.display_everything(variables, values, units)
            raw_data = sensor.get_pressure()
            save_data(1, raw_data)

            display.display_everything(variables, values, units)
            raw_data = sensor.get_humidity()
            save_data(2, raw_data)

            if sensor.get_proximity() < 10:
                raw_data = sensor.get_lux()
            else:
                raw_data = 1
            save_data(3, raw_data)
            display.display_everything(variables, values, units)

            #noise = sensor.get_noise_amp()


    # Exit cleanly
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
