import sys
import os
import logging
import epd2in9_V2
import time
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import traceback


picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

epd = epd2in9_V2.EPD()
epd.init()
epd.Clear(0xFF)

plant_img = Image.open(os.path.join(picdir, 'fem.jpg'))
image = Image.new('1', (epd.height, epd.width), 0)
draw = ImageDraw.Draw(image)
image.paste(plant_img, (14, -20))
epd.display(epd.getbuffer(image))

time.sleep(2)

image2 = Image.new('1', (epd.height, epd.width), 0)
plant_img = plant_img.resize((296, 128))
draw2 = ImageDraw.Draw(image2)
image2.paste(plant_img, (0, 0))
epd.display(epd.getbuffer(image2))

time.sleep(2)

image3 = ImageEnhance.Contrast(plant_img)
image3 = image3.enhance(2)
image4 = Image.new('1', (epd.height, epd.width), 0)
image4.paste(image3, (0, 0))
epd.display(epd.getbuffer(image4))
