import time_lapse_captures as cam

PREVIEW = False
CANT_FOTOS = 600
TIEMPO_ENTRE_FOTO = 1

if PREVIEW:   
    cam.preview()
else:
    tiempo = cam.calcular_tiempo_time_lapse(CANT_FOTOS,TIEMPO_ENTRE_FOTO)
    print("El time lapse sera de: "+ tiempo)
    entrada = input("Presionar S para empezar: ")
    if entrada.upper() == "S":
        print("Arranca el show")
        cam.a()
        image_number = 0

