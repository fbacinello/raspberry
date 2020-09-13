import time
import pantilthat
import time_lapse_captures as cam
# import ../camera/time_lapse_captures as cam
# https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
import threading
import keyboard

pos_tilt = -90
pos_pan = -90
bandera = True
speed = 0.05
last_touch = 0


def cam_preview(start=0):
    cam.start_preview(start)


def cam_stop():
    cam.stop_preview()


def mover_pan(i):
    a = int(i)

    pantilthat.pan(a)
    time.sleep(speed)


def mover_tilt(i):
    a = int(i)

    pantilthat.tilt(a)
    time.sleep(speed)


def mover_horizontal(direccion):
    global pos_pan
    if direccion == 'left' and pos_pan > -90:
        pos_pan -= 1
    if direccion == 'right' and pos_pan < 90:
        pos_pan += 1
    mover_pan(pos_pan)    


def mover_vertical(direccion):
    global pos_tilt
    if direccion == 'up' and pos_tilt > -90:
        pos_tilt -= 1        
    if direccion == 'down' and pos_tilt < 90:
        pos_tilt += 1
    mover_tilt(pos_tilt)

def volver_posicion():
    print('volverpos')
    global pos_tilt
    for i in range(pos_tilt, -90, -1):
        mover_tilt(i)
    global pos_pan
    for i in range(pos_pan, -90, -1):
        mover_pan(i)


def on_press_handler(event):
    timestamp = event.time
    global last_touch
    global speed
    if not time.time() - last_touch > speed:
        pass
    last_touch = time.time()
    print(timestamp)

    key = event.name
    print(key)

    if key in ('left', 'right'):
        mover_horizontal(key)
    if key in ('up', 'down'):
        mover_vertical(key)
    if key == 'esc':
        global bandera
        bandera = False
        print('esc')
        volver_posicion()


keyboard.on_press(on_press_handler)

x = threading.Thread(target=cam_preview, args=[15])
x.start()
time.sleep(0.5)


while bandera:
    pass

volver_posicion()

