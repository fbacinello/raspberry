import ST7735
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from fonts.ttf import RobotoMedium as UserFont

class Display:
    # Create ST7735 LCD display class
    st7735 = ST7735.ST7735(
        port=0,
        cs=1,
        dc=9,
        backlight=12,
        rotation=90,
        spi_speed_hz=10000000
    )

    def __init__(self, rotation = 90):
        st7735.rotation = rotation
        # Initialize display
        st7735.begin()

    WIDTH = st7735.width
    HEIGHT = st7735.height

    # Set up canvas and font
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_size_small = 10
    font_size_large = 15
    font = ImageFont.truetype(UserFont, font_size_large)
    smallfont = ImageFont.truetype(UserFont, font_size_small)
    x_offset = 1
    y_offset = 1

    # The position of the top bar
    top_pos = 25

    def random_pixel(self):
        global img
        global WIDTH
        global HEIGHT
        img.putpixel((randint(0, WIDTH -1),randint(0,HEIGHT -1)), (randint(0,255),randint(0,255),randint(0,255)))
        img.putpixel((randint(0, WIDTH -1),randint(0,HEIGHT -1)), (randint(0,255),randint(0,255),randint(0,255)))
        img.putpixel((randint(0, WIDTH -1),randint(0,HEIGHT -1)), (randint(0,255),randint(0,255),randint(0,255)))

    r = 8
    creciendo = False
    def circle(self):
        global r
        global creciendo
        if creciendo:
            r = r + 1
        else:
            r = r - 1

        draw.rectangle((140, 0, 160, 20), (0, 0, 0))
        leftUpPoint = (150-r, 10-r)
        rightDownPoint = (150+r, 10+r)
        twoPointList = [leftUpPoint, rightDownPoint]
        draw.ellipse(twoPointList, fill=(255,0,0,255))

        if r == 0:
            creciendo = True
        if r == 8:
            creciendo = False

    # Displays data and text on the 0.96" LCD
    def display_text(self, variable, data, unit):
        # Maintain length of list
        values[variable] = values[variable][1:] + [data]
        # Scale the values for the variable between 0 and 1
        vmin = min(values[variable])
        vmax = max(values[variable])
        colours = [(v - vmin + 1) / (vmax - vmin + 1) for v in values[variable]]
        # Format the variable name and value
        message = "{}: {:.1f} {}".format(variable[:4], data, unit)
        logging.info(message)
        draw.rectangle((0, 0, WIDTH, HEIGHT), (255, 255, 255))
        for i in range(len(colours)):
            # Convert the values to colours from red to blue
            colour = (1.0 - colours[i]) * 0.6
            r, g, b = [int(x * 255.0) for x in colorsys.hsv_to_rgb(colour, 1.0, 1.0)]
            # Draw a 1-pixel wide rectangle of colour
            draw.rectangle((i, top_pos, i + 1, HEIGHT), (r, g, b))
            # Draw a line graph in black
            line_y = HEIGHT - (top_pos + (colours[i] * (HEIGHT - top_pos))) + top_pos
            draw.rectangle((i, line_y, i + 1, line_y + 1), (0, 0, 0))
        # Write the text at the top in black
        draw.text((0, 0), message, font=font, fill=(0, 0, 0))
        st7735.display(img)

    # Displays all the text on the 0.96" LCD
    def display_everything(self, variables):
        draw.rectangle((0, 0, WIDTH, HEIGHT), (0, 0, 0))
        #random_pixel()
        circle()
        column_count = 1
        row_count = (len(variables) / column_count)
        for i in range(len(variables)):
            variable = variables[i]
            data_value = values[variable][-1]
            unit = units[i]
            x = 0
            y = y_offset + ((HEIGHT / row_count) * (i % row_count))
            message = "{}: {:.1f} {}".format(variable[:4], data_value, unit)
            lim = limits[i]
            rgb = palette[0]
            for j in range(len(lim)):
                if data_value > lim[j]:
                    rgb = palette[j + 1]
            draw.text((x, y), message, font=font, fill=rgb)
        st7735.display(img)
