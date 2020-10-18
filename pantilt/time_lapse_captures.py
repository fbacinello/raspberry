from time import sleep
from picamera import PiCamera
import datetime

DEFAULT_FOLDER = "/home/pi/Desktop/"
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.rotation = 180


def capture_pic(folder=DEFAULT_FOLDER):
    global camera
    if camera.closed:
        camera = PiCamera()
    with camera as cam:
        name = "preview " + fecha_formateada() + ".jpg"
        cam.capture(folder + name)


def calcular_tiempo_time_lapse(cant_fotos, tiempo_entre_foto):
    return str(datetime.timedelta(seconds=cant_fotos * tiempo_entre_foto))


def time_lapse(cant_fotos, tiempo_entre_foto, folder=DEFAULT_FOLDER):
    image_number = 1
    while cant_fotos >= image_number:
        image_name = 'image{0:04d}.jpg'.format(image_number)
        camera.capture(folder + image_name)
        print("Foto " + str(image_number) + " de " + str(cant_fotos))
        image_number += 1
        sleep(tiempo_entre_foto)
    camera.close()


def start_preview(time=5):
    camera.resolution = (1920, 1080)
    camera.start_preview()
    sleep(time)
    if not time == 0:
        camera.stop_preview()

def stop_preview():
    camera.stop_preview()
    camera.close()

def record(time=5, folder=DEFAULT_FOLDER):
    with camera as cam:
        cam.resolution = (1920, 1080)
        cam.start_preview()
        cam.start_recording(folder + 'video' + fecha_formateada() + '.h264')
        sleep(time)
        cam.stop_recording()
        cam.stop_preview()


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


def fecha_formateada():
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
