from pprint import pprint
from typing import Callable, Self

class DNumber:

    def __init__(self, digits: list, b: int, d: int = 1000):
        
        self.size = d
        self.digits = digits
        self.base = b
        self.pad()

    @classmethod
    def fromInt(cls, n: int, b: int, d: int = 1000):
        return cls(cls.convert(n, b, d), b, d)

    def __repr__(self) -> str:
        return '...' + ''.join(str(digit) for index, digit in list(zip(range(100), self.digits))[::-1])

    def __add__(self, other: Self) -> Self:
        result = []
        for left, right in zip(self.digits, other.digits):
            result += [
                left + right
            ]
        
        for index in range(len(result)):
            n, r = divmod(result[index], self.base)
            result[index] = r
            if index + 1 == len(result): pass
            else: result[index + 1] += n

        return DNumber(result, self.base, self.size)



    @staticmethod
    def convert(number: int, base: int, padding: int) -> list[int]:
        output: list[int] = []
        while number:
            number, digit = divmod(number, base)
            output += [digit]

        return output + [0] * (padding - len(output))
    
    def pad(self):
        self.digits += [0] * (self.size - len(self.digits))


def convolve(left: list, right: list, /, *, func: Callable = lambda l, r: l * r):
    # Legth of output is the sum of input lengths (counting from zero)
    result = {n:list() for n in range(len(left) + len(right) - 1)}

    # Convolution alorithm
    for row_index, row_value in enumerate(right):
        for column_index, column_value in enumerate(left):
            result[row_index + column_index].append(
                func(row_value , column_value)
            )

    return result

def combine(convolution: list):
    return [sum(entry) for entry in convolution.values()][::-1]

def distribute(number):
    c = number[::]
    for index in range(len(c)):
        n, r = divmod(c[index], 2)
        c[index] = r
        if index + 1 == len(c): c.append(0)
        c[index + 1] += n

    return c


if __name__ == '__main__':

    D = DNumber.fromInt(3, 2)
    print(f'D: {D}')
    print(f'D: {D + D}')