from networking import Address
import random
from .cards import Card, CARDS

class Player:

    def __init__(self, name: str, address: Address):
        self.name = name
        self.addr = address

        self.set  = set()
        self.cards = []

    def __repr__(self) -> str: return f'{self.name}[{self.set}]({self.cards})'

    def generate_set(self, limit: int = 100, count: int = 10):
        self.set = self.set.union(random.choices(range(limit), k = count))

    def deal_cards(self, cards: list[Card], count = 10):
        self.cards = random.choices(cards, k = count)