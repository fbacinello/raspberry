import RPi.GPIO as GPIO
import time
from gpiozero import CPUTemperature
import sys

cpu = CPUTemperature()

# Set the GPIO naming convention
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set a variable to hold the GPIO Pin identity
pin_sensor = 17
GPIO.setup(pin_sensor, GPIO.IN)

pin_rele = 22
GPIO.setup(pin_rele, GPIO.OUT)

print("PIR Module Test (CTRL-C to exit)")

# Variables to hold the current and last states
currentstate = 0
previousstate = 0
ultimo_movimiento = 0
duracion_fuente = 60

contador = 0
contador_prendidas = 0
contador_tiempo_total = 0
contador_tiempo = 0
rele_prendido = False


def prender_rele():
    GPIO.output(pin_rele, GPIO.HIGH)


def apagar_rele():
    GPIO.output(pin_rele, GPIO.LOW)


try:
    print("Waiting for PIR to settle ...")
    # Loop until PIR output is 0
    while GPIO.input(pin_sensor) == 1:
        currentstate = 0

    print("    Ready")
    # Loop until users quits with CTRL-C
    while True:
        # Read PIR state
        currentstate = GPIO.input(pin_sensor)

        # If the PIR is triggered
        if currentstate == 1 and previousstate == 0:
            print("    Motion detected!")
            ultimo_movimiento = time.time()
            if not rele_prendido:
                prender_rele()
                rele_prendido = True
                contador_prendidas += 1
                contador_tiempo = time.time()
                print('c', contador, '-cp', contador_prendidas)
                print('temp', cpu.temperature)
            previousstate = 1
            contador += 1

        # If the PIR has returned to ready state
        elif currentstate == 0 and previousstate == 1:
            print("    Ready")
            previousstate = 0

        if time.time() - ultimo_movimiento > duracion_fuente:
            apagar_rele()
            rele_prendido = False
            tiempo_acum = time.time() - contador_tiempo
            contador_tiempo_total += tiempo_acum
            contador_tiempo = 0
            tiempo_acum = 0
            print('tiempo total', contador_tiempo_total)

        if cpu.temperature > 70:
            apagar_rele()
            sys.exit(0)

        # Wait for 10 milliseconds
        time.sleep(0.01)

except KeyboardInterrupt:
    print("    Quit")

    # Reset GPIO settings
    GPIO.cleanup()
