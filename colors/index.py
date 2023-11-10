import tkinter as tk
import colorsys, random
from typing import Self

class HSV:

    def __init__(self, hue: float, saturation: float, value: float):
        self.saturation = saturation
        self.value      = value
        self.hue        = hue

    @staticmethod
    def avg(c1: Self, c2: Self):

        diff = c1.hue - c2.hue
        if abs(diff) < .5:
            hue = (c1.hue + c2.hue) * .5
        else:
            hue = (c1.hue + c2.hue) * .5 + .5

        return HSV(hue, (c1.saturation + c2.saturation) * .5, (c1.value + c2.value) * .5)

class RGB:


    def __init__(self, red: float, green: float, blue: float):
        self.green = green
        self.blue  = blue
        self.red   = red

    @classmethod
    def fromHSV(cls, hsv: HSV):
        R, G, B = colorsys.hsv_to_rgb(hsv.hue, hsv.saturation, hsv.value)

        return cls(R, G, B)

    def hex(self, *, scale = 255) -> str:
        return f'#{int(self.red * scale):02x}{int(self.green * scale):02x}{int(self.blue * scale):02x}'



class Canvas:

    def __init__(self, width: int, height: int, *, grid_size: int = 100):

        self.height = height
        self.width  = width

        self.grid_size = grid_size

        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width = self.width * self.grid_size, height = self.height * self.grid_size)
        self.canvas.grid()

    @staticmethod
    def color(color: HSV) -> str: return RGB.fromHSV(color).hex()

    def tile(self, x: int, y: int, color: HSV):
        
        x_top = x * self.grid_size
        y_top = y * self.grid_size

        x_bot = x_top + self.grid_size
        y_bot = y_top + self.grid_size

        self.canvas.create_rectangle(x_top, y_top, x_bot, y_bot, fill = Canvas.color(color), outline = Canvas.color(color))

if __name__ == '__main__':

    c = Canvas(15, 15, grid_size=50)

    for i in range(15):
        color1 = HSV(random.random(), random.random(), random.random())
        color2 = HSV(random.random(), random.random(), random.random())

        color3 = HSV.avg(color1, color2)

        c.tile(0, i, color1)
        c.tile(1, i, color2)
        c.tile(2, i, color3)

    c.root.mainloop()