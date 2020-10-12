import sched
import time
from datetime import datetime
from datetime import timedelta

s = sched.scheduler(time.time, time.sleep)


def imprimir_y_reprogramar():
    now = datetime.now()
    print('Ahora:', now)
    en_1_min = datetime.now() + timedelta(minutes=1)
    print('dentro de un min:', en_1_min)
    s.enterabs(en_1_min.timestamp(), 1, imprimir_y_reprogramar)
    print('reprogramado para dentro de un min')


imprimir_y_reprogramar()
s.run()

while True:
    a = 0
