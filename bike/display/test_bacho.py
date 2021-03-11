import sys
import os
import logging
import epd2in9_V2
import time
from PIL import Image, ImageDraw, ImageFont
import traceback


picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

epd = epd2in9_V2.EPD()
epd.init()
epd.Clear(0xFF)

plant_img = Image.open(os.path.join('../pic', 'plant.jpg'))
image = Image.new('1', (epd.height, epd.width), 0)
draw = ImageDraw.Draw(image)
image.paste(plant_img, (14, -20))
epd.display(epd.getbuffer(image))

