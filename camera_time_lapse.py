from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.start_preview()
camera.resolution = (2592, 1944)
camera.capture('/home/pi/Desktop/image3.jpg')
camera.stop_preview()