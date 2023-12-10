import tkinter as tk
import colorsys, random
from typing import Self
import cmath, math

class HSV:

    def __init__(self, hue: float, saturation: float, value: float):
        self.saturation = saturation
        self.value      = value
        self.hue        = hue

    def __add__(self, other: Self) -> Self:
        return HSV(
            self.hue + other.hue,
            self.saturation + other.saturation,
            self.value + other.value
        )

    def unpack(self) -> tuple[float, float, float]: return self.hue, self.saturation, self.value

    def scale(self, /, scale) -> Self: return HSV(self.hue * scale, self.saturation * scale, self.value * scale)

    def cap(self):
        self.hue %= 1.0
        self.value %= 1.0
        self.saturation %= 1.0

    def erf(self):
        self.hue = math.erf(2 * self.hue - 1) * .5 + .5
        self.value = math.erf(2 * self.value - 1) * .5 + .5
        self.saturation = math.erf(2 * self.value - 1) * .5 + .5

    def normalize(self) -> Self:
        L2 = (self.hue ** 2 + self.saturation ** 2 + self.value ** 2) ** .5

        return HSV(self.hue / L2, self.saturation / L2, self.value / L2)

    @staticmethod
    def avg(c1: Self, c2: Self):

        diff = c1.hue - c2.hue
        if abs(diff) < .5:
            hue = (c1.hue + c2.hue) * .5
        else:
            hue = (c1.hue + c2.hue) * .5 + .5

        return HSV(hue, (c1.saturation + c2.saturation) * .5, (c1.value + c2.value) * .5)

    @staticmethod
    def sample_simple(c1: Self, count: int, *, sigma: float = 1.0) -> list[Self]:
        H, S, V = c1.unpack()

        samples = []
        for index in range(count):
            Hp = random.gauss(mu = H, sigma = sigma) % 1.0
            Sp = random.gauss(mu = S, sigma = sigma) % 1.0
            Vp = random.gauss(mu = V, sigma = sigma) % 1.0

            samples += [HSV(Hp, Sp, Vp)]

        return samples
    
    @staticmethod
    def sample_mul(c1: Self, count: int, *, sigma: float = 1.0) -> list[Self]:
        H, S, V = c1.unpack()

        samples = []
        for index in range(count):
            Hp = H * random.gauss(mu = 1.0, sigma = sigma)
            Sp = S * random.gauss(mu = 1.0, sigma = sigma)
            Vp = V * random.gauss(mu = 1.0, sigma = sigma)

            samples += [HSV(Hp % 1.0, Sp % 1.0, Vp % 1.0)]

        return samples
    
    @staticmethod
    def sample_astral(c1: Self, count: int, *, I: Self, J: Self, radius: float = 0.1, flag: bool = False):

        # Normalize bases of local space
        I = I.normalize()
        J = J.normalize()

        # Find the n-th root of unity 
        dzeta = cmath.exp(1j * cmath.tau / count)

        constellation = []
        for index in range(count):
            z = (dzeta ** index) * radius
            i, j = z.real, z.imag

            constellation += [
                (I.scale(i), J.scale(j))
            ]

        samples = []
        for X, Y in constellation:
            s = c1 + X + Y
            if flag: s.erf()
            else: s.cap()

            samples += [s]

        return samples
            

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
    while True:

        for i in range(15):
            color1 = HSV(random.random(), random.random(), random.random())
            color2 = HSV(random.random(), random.random(), random.random())

            color3 = HSV.avg(color1, color2)

            c.tile(0, i, color1)
            c.tile(1, i, color2)
            c.tile(2, i, color3)

        color1 = HSV(random.random(), random.random(), random.random())
        c.tile(4, 0, color1)
        s = HSV.sample_simple(color1, 10, sigma = 0.1)
        for index, color in enumerate(s):
            c.tile(5, index, color)

        c.tile(7, 0, color1)
        s = HSV.sample_mul(color1, 10, sigma = 0.1)
        for index, color in enumerate(s):
            c.tile(8, index, color)

        c.tile(10, 0, color1)
        s = HSV.sample_astral(color1, 10, I = HSV(1, 0, 0), J = HSV(0, 0, 1))
        for index, color in enumerate(s):
            c.tile(11, index, color)

        c.tile(13, 0, color1)
        s = HSV.sample_astral(color1, 10, I = HSV(1, 0, 0), J = HSV(0, 0, 1), flag = True, radius = 0.3)
        for index, color in enumerate(s):
            c.tile(14, index, color)

        c.root.update()
        #input()