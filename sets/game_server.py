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
        room_name, player_name, card_name = body.split(' ')

        player: game.Player = ctx.data['rooms'][room_name].players[player_name]


        for index, card in enumerate(player.cards):
            if card.name == card_name: break

        player.set = card(player.set)

        del player.cards[index]

        ctx.data['rooms'][room_name].players[player_name] = player

    @SERVER.command('RESPONSE')
    def response(ctx: nt.Server, address: nt.Address, body: str):
        print(f'Response from [{address.host}:{address.port}]: {body}')

    @SERVER.command('ECHO')
    def echo(ctx: nt.Server, address: nt.Address, body: str):
        ctx.send(bytes(f'RESPONSE {body}', "UTF-8"), address)

    SERVER.serve()
    input('Press Enter to close the server!\n')