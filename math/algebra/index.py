from pprint import pprint
from typing import Callable, Self

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
