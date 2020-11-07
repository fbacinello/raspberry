from time import sleep
import board
import neopixel
import threading

# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.D18

# On a Raspberry pi, use this instead, not all pins are supported
# pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 100

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
)


def latir():
    while True:
        for i in range(1, 10, 1):
            pixels.brightness = i/10
            sleep(0.1)

        for i in range(10, 1, -1):
            pixels.brightness = i/10
            sleep(0.1)


def apagar():
    pixels.fill((0, 0, 0))
    pixels.show()


t_latir = threading.Thread(target=latir)
t_latir.start()

# pixels = neopixel.NeoPixel(board.D18, 300, brightness=1)
pixels.fill((0, 255, 0))
sleep(2)
pixels.show()

for i in range(num_pixels):
    print(i)
    pixels[i] = (255, 0, 0)
    pixels.show()
    sleep(0.05)

for i in range(num_pixels -1, 0, -1):
    print(i)
    pixels[i] = (0, 255, 0)
    pixels.show()
    sleep(0.05)

apagar()
