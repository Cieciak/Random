import tkinter as tk
import random, time
from math import *

class Imaginary:

    def __init__(self, origin: complex, size: float, resolution: int):

        self.resolution = resolution
        self.origin     = origin
        self.size       = size
        self.func       = lambda x: x - (x - .25j) * (x - .5j) * (x - .75) * (x - .33) * (x + .707 - 0.2j) * (x + .345) * (x - .1j)

        # Create tkinter app
        self.root       = tk.Tk()
        self.canvas     = tk.Canvas(self.root, width = self.resolution, height = self.resolution)
        self.canvas.grid()

    def gerenerate(self, size: int, magnitude: float):
        self.points = [complex(random.random() * magnitude, random.random() * magnitude) for _ in range(size)]
        return self.points

    def apply(self):
        self.points = [self.func(p) for p in self.points]

    def plot(self):
        for p in self.points:
            self.draw_point(p)

    def clear(self):
        self.canvas.delete('all')

    def draw_point(self, point: complex):
        point = point.conjugate() - self.origin
        scale = self.resolution / self.size

        point = point * scale + complex(self.resolution, self.resolution) * .5

        self.canvas.create_oval(
            point.real - 10,
            point.imag - 10,
            point.real + 10,
            point.imag + 10,
            fill='red',
        )

    def update(self):
        self.root.update()

SIZE = 1000
ITERATIONS = 10

# root = tk.Tk()

# canvas = tk.Canvas(root, width = SIZE, height = SIZE)
# canvas.grid()

def scale(s: float):
    def decorator(func):
        def wrapper(x: float):
            return s * func(x / s)
        return wrapper
    return decorator

def draw(canvas: tk.Canvas, input: list[float], output: list[float], spacing: int, offset: tuple[int, int]):

    dx, dy = offset
    for i, o in zip(input, output):
        canvas.create_line(
            dx,
            dy + i,
            dx + spacing,
            dy + o
        )

def apply(f, array: list[float]) -> list[float]:
    return [f(x) for x in array]

# # Something happens around 4.1 -- 4.2
# @scale(45)
# def f(x: float) -> float:
#     return (x**5)/(x**3 + x + 1)


# A = [180 * x for x in range(1, 10)]
# for i in range(ITERATIONS):

#     B = apply(f, A)
#     draw(canvas, A, B, SIZE / ITERATIONS, (1 + (SIZE / ITERATIONS) * i, 10))

#     A = B

plotter = Imaginary(0, 2, 1000)

POINTS = plotter.gerenerate(100, .5)

while True:
    plotter.update()
    time.sleep(0.01)
    plotter.clear()
    plotter.apply()
    plotter.plot()


#root.mainloop()