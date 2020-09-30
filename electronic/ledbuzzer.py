import RPi.GPIO as GPIO
import time

# Set the GPIO naming convention
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set the three GPIO pins for Output
GPIO.setup(18, GPIO.OUT) # roja
GPIO.setup(24, GPIO.OUT) # azul
GPIO.setup(22, GPIO.OUT) # parlante

luz_roja = True
for i in range(100):
    if luz_roja:
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)
    else:
        GPIO.output(24, GPIO.HIGH)
        GPIO.output(18, GPIO.LOW)
    time.sleep(0.05)    
    luz_roja = not luz_roja

GPIO.output(18, GPIO.LOW)
GPIO.output(24, GPIO.LOW)


GPIO.output(22, GPIO.HIGH)
time.sleep(0.2)
GPIO.output(22, GPIO.LOW)
GPIO.cleanup()
