from time import sleep
from picamera import PiCamera
import datetime

camera = PiCamera()
camera.resolution = (2592, 1944)

def a():
    print("yesss")
    
def preview(folder):
    camera.capture(folder + 'preview.jpg')
    
def calcular_tiempo_time_lapse(cant_fotos, tiempo_entre_foto):
    return str(datetime.timedelta(seconds=cant_fotos*tiempo_entre_foto))

def time_lapse(cant_fotos, tiempo_entre_foto, folder):
    image_number = 1
    while cant_fotos >= image_number:
        image_name = 'image{0:04d}.jpg'.format(image_number)
        camera.capture(folder + image_name)
        print("Foto " + str(image_number) + " de " + str(cant_fotos))
        image_number += 1
        sleep(tiempo_entre_foto)
    