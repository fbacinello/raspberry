import time
import pantilthat
import time_lapse_captures as cam
# import ../camera/time_lapse_captures as cam
# https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
import threading
import keyboard
import sys
import time_lapse_captures as cam

FOLDER = "/root/Desktop/New"

pos_tilt = -90
pos_pan = -90
bandera = True
delay = 0.1
last_touch = 0
speed = 4

def mover_pan(i):
    pantilthat.pan(int(i))


def mover_tilt(i):
    pantilthat.tilt(int(i))


def mover_horizontal(direccion):
    global speed
    global pos_pan
    if direccion == 'right' and pos_pan > -90:
        pos_pan -= speed
    if direccion == 'left' and pos_pan < 90:
        pos_pan += speed
    mover_pan(pos_pan)


def mover_vertical(direccion):
    global speed
    global pos_tilt
    if direccion == 'up' and pos_tilt > -90:
        pos_tilt -= speed
    if direccion == 'down' and pos_tilt < 90:
        pos_tilt += speed
    mover_tilt(pos_tilt)


def volver_posicion():
    global pos_tilt
    for i in range(pos_tilt, -90, -1):
        time.sleep(0.01)
        pos_tilt = i
        mover_tilt(i)
    global pos_pan
    for i in range(pos_pan, -90, -1):
        time.sleep(0.01)
        pos_pan = i
        mover_pan(i)


def log():
    global pos_tilt
    global pos_pan
    print('h', pos_pan, 'v', pos_tilt)


def on_press_handler(event):
    timestamp = event.time
    global last_touch
    global delay
    if not timestamp - last_touch > delay:
        print('muy rapido')
        pass
    else:
        last_touch = timestamp

        key = event.name
        if key in ('left', 'right'):
            mover_horizontal(key)
        if key in ('up', 'down'):
            mover_vertical(key)
        if key == 'esc':
            global bandera
            bandera = False
            volver_posicion()
            sys.exit()
        if key == 'enter':
            cam.capture_pic(FOLDER)
        print(key)
        log()


keyboard.on_press(on_press_handler)

while bandera:
    pass



