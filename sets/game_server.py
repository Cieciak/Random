import networking as nt

if __name__ == '__main__':
    ADDRESS = nt.Address('127.0.0.1', 20000)
    SERVER  = nt.Server(ADDRESS)

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