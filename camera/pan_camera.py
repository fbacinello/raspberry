import math
import time
import pantilthat
import sys
import time_lapse_captures as cam
import threading

def mover(i):
    a = int(i)

    pantilthat.pan(a)
    pantilthat.tilt(a)
    time.sleep(0.01)

def cam_preview():
    cam.start_preview()    

x = threading.Thread(target=cam_preview)
x.start()
time.sleep(0.1)

for i in range(-90, 90, 1):
    mover(i)
    POS = i
        
for i in range(90, -90, -1):
    mover(i)
    POS = i