from .player import Player
from .cards import Card, CARDS

class Room:

    def __init__(self, name: str):
        self.players: dict[str, Player] = dict()
        self.lock: bool = False
        self.name: str = name

    def __repr__(self) -> str:
        return f'{self.name}: {self.players}'
        
    def add_player(self, p: Player):
        if self.lock: return
        else: self.players[p.name] = p

    def start(self):
        for name, player in self.players.items():
            player.deal_cards(CARDS)
            player.generate_set()