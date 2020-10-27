import time_lapse_captures as cam
import time
import threading
import pygame

X = 0.0
Y = 0.0
W = 1.0
H = 1.0

pygame.init()
fps=30
fpsclock=pygame.time.Clock()
sur_obj=pygame.display.set_mode((180,180))
pygame.display.set_caption("Keyboard_Input")
White=(255,255,255)
p1=10
p2=10
step=5

def preview():
    cam.start_preview(0)    

def mover_pygame():
    global X
    global Y
    global W
    global H
    
    global p1
    global p2
    
    sur_obj.fill(White)
    pygame.draw.rect(sur_obj, (255,0,0), (p1, p2, 70, 65))
    for eve in pygame.event.get():
        if eve.type==pygame.QUIT:
            volver_posicion()            
            pygame.quit()
            sys.exit()
    key_input = pygame.key.get_pressed()
    
    if key_input[pygame.K_LEFT]:
        p1 -= step
        X += 0.1
        W = 0.5
        H = 0.5
    if key_input[pygame.K_RIGHT]:
        p1 += step
        Y += 0.1
        W = 0.5
        H = 0.5
        
    if key_input[pygame.K_UP]:
        p2 -= step
        H -= 0.1
    if key_input[pygame.K_DOWN]:
        p2 += step
        W -= 0.1
        
    pygame.display.update()
    fpsclock.tick(fps)
    cam.zoomear(X, Y, W, H)
    print((X, Y, W, H))

t = threading.Thread(target=preview)
t.start()

while True:
    mover_pygame()

# for i in range(0, 11):
#     val = i/10
#     print(val)    
#     cam.zoomear(val, val, W, H)
#     time.sleep(0.5)



# cam.zoomear(X, Y, W, H)