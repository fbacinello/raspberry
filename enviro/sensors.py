from bme280 import BME280

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559

    ltr559 = LTR559()
except ImportError:
    import ltr559
from subprocess import PIPE, Popen
from enviroplus.noise import Noise


class Sensors:
    def __init__(self):
        # BME280 temperature/pressure/humidity sensor
        self.bme280 = BME280()
        # Light sensor
        self.ltr559 = LTR559()
        self.noise = Noise()

        self.cpu_temps = None
        self.factor = 2.15

    # Get the temperature of the CPU for compensation
    def get_cpu_temperature(self):
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
        output, _error = process.communicate()
        return float(output[output.index('=') + 1:output.rindex("'")])

    def get_temperature(self):
        if self.cpu_temps is None:
            self.cpu_temps = [self.get_cpu_temperature()] * 5

        cpu_temp = self.get_cpu_temperature()
        # Smooth out with some averaging to decrease jitter
        self.cpu_temps = self.cpu_temps[1:] + [cpu_temp]
        avg_cpu_temp = sum(self.cpu_temps) / float(len(self.cpu_temps))
        #print(avg_cpu_temp)
        raw_temp = self.bme280.get_temperature()
        raw_data = raw_temp - ((avg_cpu_temp - raw_temp) / self.factor)
        return raw_data

    def get_pressure(self):
        return self.bme280.get_pressure()

    def get_humidity(self):
        return self.bme280.get_humidity()

    def get_lux(self):
        return self.ltr559.get_lux()

    def get_proximity(self):
        return self.ltr559.get_proximity()

    def get_noise_amp(self):
        amps = self.noise.get_amplitudes_at_frequency_ranges([
            (100, 200),
            (500, 600),
            (1000, 1200),
            (2000, 5000)
        ])
        amps = [n * 32 for n in amps]
        return amps
