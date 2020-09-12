import time
import pantilthat
import time_lapse_captures as cam
# import ../camera/time_lapse_captures as cam
# https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
import threading
import keyboard


def cam_preview():
    cam.start_preview(0)


def cam_stop():
    cam.stop_preview()


def mover_pan(i):
    a = int(i)

    pantilthat.pan(a)
    time.sleep(0.05)


def mover_tilt(i):
    a = int(i)

    pantilthat.tilt(a)
    time.sleep(0.05)


def mover_horizontal(direccion):
    global pos_pan
    if direccion == 'left' and pos_pan >= -90:
        pos_pan -= 1
    if direccion == 'right' and pos_pan <= 90:
        pos_pan += 1


def mover_vertical(direccion):
    global pos_tilt
    if direccion == 'up' and pos_tilt >= -90:
        pos_tilt -= 1
    if direccion == 'down' and pos_tilt <= 90:
        pos_tilt += 1


def on_press_handler(event):
    dire = event.name
    print(event.name)
    if dire in ('left', 'right'):
        mover_horizontal(dire)
    if dire in ('up', 'down'):
        mover_vertical(dire)


for i in range(90, -90, -1):
    mover_pan(i)

for i in range(90, -90, -1):
    mover_tilt(i)

keyboard.on_press(on_press_handler)

x = threading.Thread(target=cam_preview)
x.start()
time.sleep(0.5)

pos_tilt = -90
pos_pan = -90

while True:
    pass


