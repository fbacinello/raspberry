import ST7735
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from fonts.ttf import RobotoMedium as UserFont
from random import randint
import colorsys


class Display:
    def __init__(self, rotation=90):
        self.r = 8
        self.creciendo = False
        # Create ST7735 LCD display class
        self.st7735 = ST7735.ST7735(
            port=0,
            cs=1,
            dc=9,
            backlight=12,
            rotation=rotation,
            spi_speed_hz=10000000
        )

        # Initialize display
        self.st7735.begin()

        self.WIDTH = self.st7735.width
        self.HEIGHT = self.st7735.height

        # Set up canvas and font
        self.img = Image.new('RGB', (self.WIDTH, self.HEIGHT), color=(0, 0, 0))
        self.draw = ImageDraw.Draw(self.img)
        font_size_small = 10
        font_size_large = 15
        self.font = ImageFont.truetype(UserFont, font_size_large)
        self.selfsmallfont = ImageFont.truetype(UserFont, font_size_small)
        self.x_offset = 1
        self.y_offset = 1

        # Define your own warning limits
        # The limits definition follows the order of the variables array
        # Example limits explanation for temperature:
        # [4,18,28,35] means
        # [-273.15 .. 4] -> Dangerously Low
        # (4 .. 18]      -> Low
        # (18 .. 28]     -> Normal
        # (28 .. 35]     -> High
        # (35 .. MAX]    -> Dangerously High
        # DISCLAIMER: The limits provided here are just examples and come
        # with NO WARRANTY. The authors of this example code claim
        # NO RESPONSIBILITY if reliance on the following values or this
        # code in general leads to ANY DAMAGES or DEATH.
        self.limits = [[4, 18, 28, 35],
                       [250, 650, 1013.25, 1015],
                       [20, 30, 60, 70],
                       [-1, -1, 30000, 100000]]

        # RGB palette for values on the combined screen
        self.palette = [(0, 0, 255),  # Dangerously Low
                        (0, 255, 255),  # Low
                        (0, 255, 0),  # Normal
                        (255, 255, 0),  # High
                        (255, 0, 0)]  # Dangerously High

        # The position of the top bar
        self.top_pos = 25

    def random_pixel(self):
        self.img.putpixel((randint(0, self.WIDTH - 1), randint(0, self.HEIGHT - 1)),
                          (randint(0, 255), randint(0, 255), randint(0, 255)))
        self.img.putpixel((randint(0, self.WIDTH - 1), randint(0, self.HEIGHT - 1)),
                          (randint(0, 255), randint(0, 255), randint(0, 255)))
        self.img.putpixel((randint(0, self.WIDTH - 1), randint(0, self.HEIGHT - 1)),
                          (randint(0, 255), randint(0, 255), randint(0, 255)))

    def circle(self):
        if self.creciendo:
            self.r = self.r + 1
        else:
            self.r = self.r - 1

        self.draw.rectangle((140, 0, 160, 20), (0, 0, 0))
        left_up_point = (150 - self.r, 10 - self.r)
        right_down_point = (150 + self.r, 10 + self.r)
        two_point_list = [left_up_point, right_down_point]
        self.draw.ellipse(two_point_list, fill=(255, 0, 0, 255))

        if self.r == 0:
            self.creciendo = True
        if self.r == 8:
            self.creciendo = False

    # Displays data and text on the 0.96" LCD
    def display_text(self, variable, values, data, unit):
        # Maintain length of list
        values[variable] = values[variable][1:] + [data]
        # Scale the values for the variable between 0 and 1
        vmin = min(values[variable])
        vmax = max(values[variable])
        colours = [(v - vmin + 1) / (vmax - vmin + 1) for v in values[variable]]
        # Format the variable name and value
        message = "{}: {:.1f} {}".format(variable[:4], data, unit)
        # logging.info(message)
        self.draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), (255, 255, 255))
        for i in range(len(colours)):
            # Convert the values to colours from red to blue
            colour = (1.0 - colours[i]) * 0.6
            r, g, b = [int(x * 255.0) for x in colorsys.hsv_to_rgb(colour, 1.0, 1.0)]
            # Draw a 1-pixel wide rectangle of colour
            self.draw.rectangle((i, self.top_pos, i + 1, self.HEIGHT), (r, g, b))
            # Draw a line graph in black
            line_y = self.HEIGHT - (self.top_pos + (colours[i] * (self.HEIGHT - self.top_pos))) + self.top_pos
            self.draw.rectangle((i, line_y, i + 1, line_y + 1), (0, 0, 0))
        # Write the text at the top in black
        self.draw.text((0, 0), message, font=self.font, fill=(0, 0, 0))
        self.st7735.display(self.img)

    # Displays all the text on the 0.96" LCD
    def display_everything(self, variables, values, units):
        self.draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), (0, 0, 0))
        self.circle()
        column_count = 1
        row_count = (len(variables) / column_count)
        for i in range(len(variables)):
            variable = variables[i]
            data_value = values[variable][-1]
            unit = units[i]
            x = 0
            y = self.y_offset + ((self.HEIGHT / row_count) * (i % row_count))
            message = "{}: {:.1f} {}".format(variable[:4], data_value, unit)
            lim = self.limits[i]
            rgb = self.palette[0]
            for j in range(len(lim)):
                if data_value > lim[j]:
                    rgb = self.palette[j + 1]
            self.draw.text((x, y), message, font=self.font, fill=rgb)
        self.st7735.display(self.img)

    def set_backlight(self, value):
        self.st7735.set_backlight(value)

    def turn_off(self):
        self.st7735.set_backlight(0)

    def turn_on(self):
        self.st7735.set_backlight(12)
