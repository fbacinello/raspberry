from time import sleep
from picamera import PiCamera
import datetime

DEFAULT_FOLDER = "/home/pi/Desktop/"
camera = PiCamera()
camera.resolution = (2592, 1944)

def preview(folder = DEFAULT_FOLDER):   
    now = datetime.datetime.now()
    name = "preview " + str(now.strftime("%Y-%m-%d %H-%M-%S") + ".jpg")
    camera.capture(folder + name)    
    
def calcular_tiempo_time_lapse(cant_fotos, tiempo_entre_foto):
    return str(datetime.timedelta(seconds=cant_fotos*tiempo_entre_foto))

def time_lapse(cant_fotos, tiempo_entre_foto, folder = DEFAULT_FOLDER):
    image_number = 1
    while cant_fotos >= image_number:
        image_name = 'image{0:04d}.jpg'.format(image_number)
        camera.capture(folder + image_name)
        print("Foto " + str(image_number) + " de " + str(cant_fotos))
        image_number += 1
        sleep(tiempo_entre_foto)

def start_preview(time=5):
    camera.resolution = (1920, 1080)
    camera.start_preview()
    sleep(time)
    camera.stop_preview()
    
def record(time=5, folder = DEFAULT_FOLDER):
    camera.resolution = (1920, 1080)
    camera.start_preview()
    camera.start_recording('/home/pi/Desktop/video.h264')
    sleep(time)
    camera.stop_recording()
    camera.stop_preview()
    
def show_effects(time=2):
    camera.resolution = (1920, 1080)
    camera.start_preview()
    for effect in camera.IMAGE_EFFECTS:
        camera.image_effect = effect
        camera.annotate_text = "Effect: %s" % effect
        sleep(time)
    camera.stop_preview()

def show_exposure(time=2):
    camera.resolution = (1920, 1080)
    camera.start_preview()
    for exposure in camera.EXPOSURE_MODES:
        camera.exposure_mode = exposure
        camera.annotate_text = "Exposure: %s" % exposure
        sleep(time)
    camera.stop_preview()
    