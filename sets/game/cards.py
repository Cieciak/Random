from typing import Callable

class Card:

    def __init__(self, name: str, function: Callable):
        self.name = name
        self.f = function

    def __repr__(self) -> str:
        return f'{self.name}'

    def __call__(self, s: set):
        return set(self.f(element) for element in s)
    
CARDS = [
    Card('ADDER', lambda x: x + 1),
    Card('SUB', lambda x: x - 1),
]