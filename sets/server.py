import socket, threading, random
from typing import Any

class Server:
    BUFFER_SIZE = 1024

    def __init__(self, address: str, port: int):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((address, port))
        
        self.commands = {}

        self.address = address
        self.running = True
        self.port = port
        self.data = {}
        print('Server is up')

    def __loop(self):
        '''Main loop of the server'''
        while self.running:
            message, address = self.socket.recvfrom(self.BUFFER_SIZE)
            print(f'Message from [{address[0]}:{address[1]}]: {message}')

            name, body = self.parse(message)
            print(f'Command: {name}, body: {body}')

            handle = self.commands.get(name, None)
            if handle is None:
                print(f'No handler for \"{name}\" found')
                continue
            try:
                handle(self, address, body)
            except Exception as error:
                print(f'{error}')
        
    def serve(self):
        '''Create thread for handling incoming requests'''
        __thread = threading.Thread(
            target = self.__loop,
            daemon = True,
            group  = None,
            name   = f'Main loop of {self.address}:{self.port}',
        )
        __thread.start()

    def send(self, buffer: bytes, address: str, port: int):
        self.socket.sendto(buffer, (address, port))

    def command(self, name: str):
        def decorator(function):
            self.commands[name] = function

        return decorator

    @staticmethod
    def parse(buffer: bytes) -> tuple[str, str]:
        raw = buffer.decode('UTF-8')
        command, body = raw.split(' ', 1)
        
        return command, body

class Card:

    def __init__(self, name: str, f):
        self.name = name
        self.f = f

    def __repr__(self) -> str:
        return f'{self.name}'

    def __call__(self, s: set):
        return set(self.f(element) for element in s)

CARDS = [
    Card('ADDER', lambda x: x + 1),
    Card('SUB', lambda x: x - 1),
]

class Player:

    def __init__(self, name: str, _set: set):
        self.name  = name
        self.set   = _set
        self.avcards = []

    def __repr__(self) -> str:
        return f'[{self.name[0]}:{self.name[1]}]: {self.set} {self.avcards}'

    def assign(self, count: int = 10):
        for _ in range(count):
            self.set.add(random.randint(0, 100))

    def cards(self, options, count):
        for _ in range(count):
            self.avcards += random.choices(options, k = count)

class Room:

    def __init__(self, name: str):
        self.name = name
        self.agents: set[Player] = set()

        self.locked = False

    def __repr__(self) -> str: return '; '.join(f'{player}' for player in self.agents)

    def add(self, address: tuple[str, int]): 
        if not self.locked: self.agents.add(Player(address, set()))

    def remove(self, address: tuple[str, int]): 
        if not self.locked:
            player = filter(lambda p: p.name == address, self.agents)
            self.agents.remove(player)

    def lock(self): self.locked = True

    def unlock(self): self.locked = False

    def assign(self, count: int = 10):
        for player in self.agents:
            player.assign(count)

    def cards(self, options, count):
        for player in self.agents:
            player.cards(options, count)


if __name__ == '__main__':

    localIP     = "127.0.0.1"
    localPort   = 20001

    SERVER = Server(localIP, localPort)

    @SERVER.command('ECHO')
    def echo(ctx: Server, address: tuple[str, int], body: str):
        ctx.send(bytes(f'RESPONSE {body}', "UTF-8"), address[0], address[1])

    @SERVER.command('ADD-LISTING')
    def add_listing(ctx: Server, address: tuple[str, int], body: str):
        current = ctx.data.get('listing', []) + [address]
        ctx.data['listing'] = current

    @SERVER.command('GET-LISTING')
    def add_listing(ctx: Server, address: tuple[str, int], body: str):
        current = ctx.data.get('listing', [])
        text = '; '.join(f'{addr}:{port}' for addr, port in current)

        ctx.send(bytes(f'RESPONSE {text}', "UTF-8"), address[0], address[1])

    @SERVER.command('BROADCAST')
    def broadcast(ctx: Server, address: tuple[str, int], body: str):
        current = ctx.data.get('listing', [])
        for addr, port in current:
            ctx.send(bytes(f'RESPONSE {body}', "UTF-8"), addr, port)

    @SERVER.command('MAKE-ROOM')
    def make_room(ctx: Server, address: tuple[str, int], body: str):
        rooms = ctx.data.get('rooms', {})
        rooms[body] = Room(body)
        ctx.data['rooms'] = rooms
    
    @SERVER.command('JOIN-ROOM')
    def join_room(ctx: Server, address: tuple[str, int], body: str):
        room: Room = ctx.data['rooms'][body]
        room.add(address)

        ctx.data['rooms'][body] = room

    @SERVER.command('GET-ROOM')
    def get_room(ctx: Server, address: tuple[str, int], body: str):
        room: Room = ctx.data['rooms'][body]

        ctx.send(bytes(f'RESPONSE {room}', "UTF-8"), address[0], address[1])

    @SERVER.command('RBROAD')
    def rbroadcast(ctx: Server, address: tuple[str, int], body: str):
        rooms: dict[str, Room] = ctx.data['rooms']

        for key, room in rooms.items():
            if address in room.agents: break

        for addr, port in rooms[key].agents:
            ctx.send(bytes(f'RESPONSE {body}', "UTF-8"), addr, port)

    @SERVER.command('RASS')
    def rass(ctx: Server, address: tuple[str, int], body: str):
        room: Room = ctx.data['rooms'][body]
        room.assign()
        room.cards(CARDS, 3)
        ctx.data['rooms'][body] = room

    @SERVER.command('USE')
    def use(ctx: Server, address: tuple[str, int], body: str):
        rooms: dict[str, Room] = ctx.data['rooms']

        for key, room in rooms.items():
            if address in room.agents: break
        room: Room = rooms[key]

        deck = []
        for player in room.agents:
            if player.name == address:
                deck = player.avcards
                break
        
        for index, card in enumerate(deck):
            if card.name == body:
                break
        
        player.set = card(player.set)
        del player.avcards[index]
        ctx.data['rooms'][key] = room

        
                


    SERVER.serve()

    input('Press Enter to close the server!\n')