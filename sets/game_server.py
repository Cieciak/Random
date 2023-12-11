import networking as nt
import game

if __name__ == '__main__':
    ADDRESS = nt.Address('127.0.0.1', 20000)
    SERVER  = nt.Server(ADDRESS)

    SERVER.data['rooms'] = {}

    @SERVER.command('MAKE-ROOM')
    def make_room(ctx: nt.Server, address: nt.Address, body: str):
        ctx.data['rooms'][body] = game.Room(body)

    @SERVER.command('JOIN-ROOM')
    def join_room(ctx: nt.Server, address: nt.Address, body: str):
        name, room = body.split(' ')
        
        player = game.Player(name, address)

        ctx.data['rooms'][room].add_player(player)

    @SERVER.command('GET-ROOM')
    def get_room(ctx: nt.Server, address: nt.Address, body: str):
        room: game.Room = ctx.data['rooms'][body]

        ctx.send(bytes(f'CONSOLE {room}', 'UTF-8'), address)

    @SERVER.command('START-GAME')
    def start_game(ctx: nt.Server, address: nt.Address, body: str):
        ctx.data['rooms'][body].start()

    @SERVER.command('USE-CARD')
    def use_card(ctx: nt.Server, address: nt.Address, body: str):
        body, name, used = body.split(' ')

        room: game.Room = ctx.data['rooms'][body]
        for player in room.players:
            if player.name == name: break
        
        deck = player.cards
        
        for index, card in enumerate(deck):
            if card.name == used: break

        del deck[index]
        player.cards = deck
        ctx.data['rooms'][body] = room

        



    @SERVER.command('RESPONSE')
    def response(ctx: nt.Server, address: nt.Address, body: str):
        print(f'Response from [{address.host}:{address.port}]: {body}')

    @SERVER.command('ECHO')
    def echo(ctx: nt.Server, address: nt.Address, body: str):
        ctx.send(bytes(f'RESPONSE {body}', "UTF-8"), address)

    @SERVER.command('ADD')
    def add(ctx: nt.Server, address: nt.Address, body: str):
        ctx.send(bytes(f'ADD-TO-SET {body}', "UTF-8"), address)

    @SERVER.command('CADD')
    def add(ctx: nt.Server, address: nt.Address, body: str):
        ctx.send(bytes(f'ADD-CARD {body}', "UTF-8"), address)

    SERVER.serve()
    input('Press Enter to close the server!\n')