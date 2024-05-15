from typing import BinaryIO
from dataclasses import dataclass

class ColorMap:
    def __init__(self, raw: bytes):
        self.raw = raw

    def __getitem__(self, index: int):
        return self.raw[3 * index], self.raw[3 * index + 1], self.raw[3 * index + 2]

@dataclass
class ScreenDescriptor:
    width: int
    height: int
    flags: int
    background: int
    ratio: int

@dataclass
class ImageDescriptor:
    height: int
    width: int
    flags: int
    left: int
    top:  int

class GIF_Reader:

    def __init__(self, raw: BinaryIO):
        self.file = file

    def consume_header(self):
        self.header = self.file.read(6)

    def consume_screen_descriptor(self):
        width = int.from_bytes(self.file.read(2), 'little')
        he
        data = self.file.read(7)

        self.width  = data[0] + 256 * data[1]
        self.height = data[2] + 256 * data[3] 

        self.flags  = data[4]

        self.background   = data[5]
        self.aspect_ratio = data[6]

    def consume_color_map(self, size: int) -> ColorMap:
        data = self.file.read(3 * size)

        return ColorMap(data)

    def consume_extension_block(self):
        function_code = int.from_bytes(self.file.read(1), 'little')
        size          = int.from_bytes(self.file.read(1), 'little')
        data          = bytes()

        while size > 0:
            chunk = self.file.read(size)
            size  = int.from_bytes(self.file.read(1), 'little')

            data = data + chunk

        print(f'Blok data: {data}')
        return data
    
    def consume_image_descriptor(self) -> ImageDescriptor:
        left   = int.from_bytes(self.file.read(2), 'little')
        top    = int.from_bytes(self.file.read(2), 'little')
        width  = int.from_bytes(self.file.read(2), 'little')
        height = int.from_bytes(self.file.read(2), 'little')
        flags  = int.from_bytes(self.file.read(1), 'little')

        return ImageDescriptor(
            height = height,
            width = width,
            flags = flags,
            left = left,
            top = top,
        )

    # Global map
    def read(self):
        self.consume_header()
        self.consume_screen_descriptor()

        # Try to read global
        if self.flags & 0b1000_0000:
            length = 2 ** (1 + (self.flags & 0b0000_0111))
            self.global_map = self.consume_color_map(length)

        separator = self.file.read(1)

        while True:
            match separator:
                case b'!':
                    block = self.consume_extension_block()
                case b',':
                    block = self.consume_image_descriptor()
                    if block.flags & 0b1000_0000:
                        lenght = 2 ** (1 + (block.flags & 0b0000_0111))
                        local_map = self.consume_color_map(lenght)
                    print(block)
                case _:
                    print(f'Unknown separator: {separator}')
                    break

            separator = self.file.read(1)


FILE = './gif/sample.gif'

with open(FILE, 'rb') as file:
    gif = GIF_Reader(file)

    gif.read()
