import time
import sys
import threading
import logging

def getch():
    ch = sys.stdin.read(1)
    return ch

def capturar():
    char = getch()
    logging.info(char)
    
def seguir_capturando():
    while(True):
        capturar()

thread = threading.Thread(target=seguir_capturando)
thread.start()

while(True):
    pass