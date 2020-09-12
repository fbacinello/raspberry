import time
import pantilthat
import time_lapse_captures as cam
# import ../camera/time_lapse_captures as cam
# https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
import threading


def mover(i):
    a = int(i)

    pantilthat.pan(a)
    pantilthat.tilt(a)
    time.sleep(0.01)


def mover_pan(i):
    a = int(i)

    pantilthat.pan(a)    
    time.sleep(0.05)


def mover_tilt(i):
    a = int(i)

    pantilthat.tilt(a)    
    time.sleep(0.05)


def cam_preview():
    cam.start_preview(0)


def cam_stop():
    cam.stop_preview() 


x = threading.Thread(target=cam_preview)
x.start()
time.sleep(0.5)

for i in range(-90, -30, 1):
    mover_tilt(i)
time.sleep(0.25)

for i in range(-90, 0, 1):
    mover_pan(i)
    POS = i
time.sleep(0.25)
        
for i in range(0, -90, -1):
    mover_pan(i)
    POS = i
time.sleep(0.25)

for i in range(-30, -90, -1):
    mover_tilt(i)
time.sleep(0.25)

cam_stop()
