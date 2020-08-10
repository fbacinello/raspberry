import time_lapse_captures as cam

PREVIEW = True
CANT_FOTOS = 30
TIEMPO_ENTRE_FOTO = 1
FOLDER = "/home/pi/Desktop/"

if PREVIEW:
    cam.preview(FOLDER)
# cam.record()
else:
    tiempo = cam.calcular_tiempo_time_lapse(CANT_FOTOS, TIEMPO_ENTRE_FOTO)
    print("El time lapse sera de: " + tiempo)
    entrada = input("Presionar S para empezar: ")
    if entrada.upper() == "S":
        print("Arranca el show")
        cam.time_lapse(CANT_FOTOS, TIEMPO_ENTRE_FOTO, FOLDER)
        print("FINNNNNNNN")
