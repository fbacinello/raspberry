from time import sleep
from picamera import PiCamera
import datetime

camera = PiCamera()
camera.resolution = (2592, 1944)

def a():
    print("yesss")
    
def preview():
    camera.capture('/home/pi/Desktop/preview.jpg')
    
def calcular_tiempo_time_lapse(cant_fotos, tiempo_entre_foto):
    return str(datetime.timedelta(seconds=cant_fotos*tiempo_entre_foto))
    