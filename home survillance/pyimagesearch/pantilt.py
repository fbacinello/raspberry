import pygame
import pantilthat
import threading
from time import sleep


class PanTilt:
    def __init__(self):
        self.pos_tilt = -90
        self.pos_pan = -90
        self.bandera = True
        self.delay = 0.05
        self.last_touch = 0
        self.speed = 2

        pygame.init()
        self.white = (255, 255, 255)
        self.fps = 30
        self.fpsclock = pygame.time.Clock()
        self.sur_obj = pygame.display.set_mode((180, 180))
        pygame.display.set_caption("Keyboard_Input")
        self.p1 = 10
        self.p2 = 10
        self.step = 5

    def mover_pan(self, i):
        pantilthat.pan(int(i))

    def mover_tilt(self, i):
        pantilthat.tilt(int(i))

    def mover_horizontal(self, direccion):
        if direccion == 'right' and self.pos_pan > -90:
            self.pos_pan -= self.speed
        if direccion == 'left' and self.pos_pan < 90:
            self.pos_pan += self.speed
        self.mover_pan(self.pos_pan)

    def mover_vertical(self, direccion):
        if direccion == 'up' and self.pos_tilt > -90:
            self.pos_tilt -= self.speed
        if direccion == 'down' and self.pos_tilt < 90:
            self.pos_tilt += self.speed
        self.mover_tilt(self.pos_tilt)

    def volver_posicion(self):
        for i in range(self.pos_tilt, -90, -1):
            sleep(0.01)
            self.pos_tilt = i
            self.mover_tilt(i)

        for i in range(self.pos_pan, -90, -1):
            sleep(0.01)
            self.pos_pan = i
            self.mover_pan(i)

    def log(self):
        print('h', self.pos_pan, 'v', self.pos_tilt)

    def mover_pygame(self):
        self.sur_obj.fill(self.white)
        pygame.draw.rect(self.sur_obj, (255, 0, 0), (self.p1, self.p2, 70, 65))

        key_input = pygame.key.get_pressed()
        print(key_input)
        if key_input[pygame.K_LEFT]:
            self.p1 -= self.step
            self.mover_horizontal('left')
        if key_input[pygame.K_RIGHT]:
            self.p1 += self.step
            self.mover_horizontal('right')

        if key_input[pygame.K_UP]:
            self.p2 -= self.step
            self.mover_vertical('up')
        if key_input[pygame.K_DOWN]:
            self.p2 += self.step
            self.mover_vertical('down')

        pygame.display.update()
        self.fpsclock.tick(self.fps)
        self.log()
    
    def ciclo(self):
        while True:
            self.mover_pygame()
            sleep(0.01)

    def run(self):
        x = threading.Thread(target=self.ciclo)
        x.start()
