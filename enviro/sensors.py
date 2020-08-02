from bme280 import BME280
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559
from subprocess import PIPE, Popen

# BME280 temperature/pressure/humidity sensor
bme280 = BME280()

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

def get_temperature():
    cpu_temp = get_cpu_temperature()
    # Smooth out with some averaging to decrease jitter
    cpu_temps = cpu_temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
    raw_temp = bme280.get_temperature()
    raw_data = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
    return raw_data

def get_pressure():
    return bme280.get_pressure()

def get_humidity():
    return bme280.get_humidity()

def get_lux():
    return ltr559.get_lux()

def get_proximity():
    return ltr559.get_proximity()
