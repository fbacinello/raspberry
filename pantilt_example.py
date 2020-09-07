import math
import time
import pantilthat
import sys

def mover(i):
    a = int(i)

    pantilthat.pan(a)
    pantilthat.tilt(a)
    time.sleep(0.01)
    
POS = -90

try:
    while True:
        for i in range(-90, 90, 1):
            mover(i)
            POS = i
        
        for i in range(90, -90, -1):
            mover(i)
            POS = i
            
except KeyboardInterrupt:
    sys.exit(0)
    
finally:
    for i in range(-90, POS, -1):
        mover(i)