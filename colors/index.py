import tkinter as tk
import colorsys

class Canvas:

    def __init__(self, width: int, height: int, *, grid_size: int = 100):

        self.height = height
        self.width  = width

        self.grid_size = grid_size

        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width = self.width * self.grid_size, height = self.height * self.grid_size)
        self.canvas.grid()

    @staticmethod
    def color(color: tuple[int, int, int], *, scale = 255) -> str: return f'#{int(color[0] * scale):02x}{int(color[1] * scale):02x}{int(color[2] * scale):02x}'


    def tile(self, x: int, y: int, color: tuple[int, int, int]):
        
        x_top = x * self.grid_size
        y_top = y * self.grid_size

        x_bot = x_top + self.grid_size
        y_bot = y_top + self.grid_size

        self.canvas.create_rectangle(x_top, y_top, x_bot, y_bot, fill = Canvas.color(color), outline = Canvas.color(color))

if __name__ == '__main__':

    c = Canvas(15, 1, grid_size=100)

    for i in range(15):
        color = colorsys.hsv_to_rgb(i/15, 1, 1)
        c.tile(i, 0, color)

    c.root.mainloop()