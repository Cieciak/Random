import tkinter as tk
import random
from math import sin, cos, pi

def point(part: float, *, r = 50, offset = (250, 250)):
    x = r * cos(2*pi*part)
    y = r * sin(2*pi*part)

    return (x + offset[0], y + offset[1])

def avg(a, b):
    diff = a-b
    if abs(diff) < .5:
        return (a + b) * .5
    return (a+b) * .5 + .5

root = tk.Tk()

canvas = tk.Canvas(root, width = 500, height = 500)
canvas.grid()

canvas.create_oval(200, 200, 300, 300)


a = random.random()
b = random.random()
p1 = point(a)

canvas.create_oval(p1[0]-5, p1[1] - 5, p1[0]+5, p1[1]+5, outline='red')
p2 = point(b)

canvas.create_oval(p2[0]-5, p2[1] - 5, p2[0]+5, p2[1]+5, outline='blue')
c = avg(a, b)

p3 = point(c)
canvas.create_oval(p3[0]-5, p3[1] - 5, p3[0]+5, p3[1]+5)

root.mainloop()