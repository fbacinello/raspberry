import time
import pantilthat
import sys
import cv2 as cv
import imutils
import pygame
import socket

pos_tilt = -90
pos_pan = -90
bandera = True
delay = 0.05
last_touch = 0
speed = 2

pygame.init()
fps = 24
fpsclock = pygame.time.Clock()
sur_obj = pygame.display.set_mode((180, 180))
pygame.display.set_caption("Keyboard_Input")
White = (255, 255, 255)
p1 = 10
p2 = 10
step = 5

client_socket = socket.socket()
client_socket.connect(('192.168.0.11', 8000))
connection = client_socket.makefile('wb')


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


def salir():
    volver_posicion()
    pygame.quit()
    cap.release()
    cv.destroyAllWindows()
    sys.exit()


def mover_pygame():
    global p1
    global p2

    sur_obj.fill(White)
    pygame.draw.rect(sur_obj, (255, 0, 0), (p1, p2, 70, 65))

    for eve in pygame.event.get():
        if eve.type == pygame.QUIT:
            salir()

    key_input = pygame.key.get_pressed()
    if key_input[pygame.K_LEFT]:
        p1 -= step
        mover_horizontal('left')
    if key_input[pygame.K_RIGHT]:
        p1 += step
        mover_horizontal('right')

    if key_input[pygame.K_UP]:
        p2 -= step
        mover_vertical('up')
    if key_input[pygame.K_DOWN]:
        p2 += step
        mover_vertical('down')

    if key_input[pygame.K_ESCAPE]:
        salir()

    pygame.display.update()
    fpsclock.tick(fps)
    log()


# -- 2. Read the video stream
cap = cv.VideoCapture(0)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break

    fps_cam = cap.get(5)
    cv.putText(frame, str(fps_cam), (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))

    frame = imutils.rotate(frame, 180 - pos_pan)
    cv.imshow('Capture - Rotate on pan', frame)

    connection.write(frame)
    if cv.waitKey(1) == ord('q'):
        break

    mover_pygame()
