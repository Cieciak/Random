import socket, threading, tkinter

class Server:
    BUFFER_SIZE = 1024

    def __init__(self, address: str, port: int):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((address, port))
        
        self.commands = {}

        self.address = address
        self.running = True
        self.port = port
        print('Server is up')

    def __loop(self):
        '''Main loop of the server'''
        while self.running:
            message, address = self.socket.recvfrom(self.BUFFER_SIZE)
            #print(f'Message from [{address[0]}:{address[1]}]: {message}')

            name, body = self.parse(message)
            #print(f'Command: {name}, body: {body}')

            handle = self.commands.get(name, None)
            if handle is None: raise ValueError(f'No handler for \"{name}\" found')
            handle(self, address, body)
        
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
    
if __name__ == '__main__':

    localIP     = "127.0.0.1"
    localPort   = int(input('Enter port: '))


    SERVER = Server(localIP, localPort)

    @SERVER.command('RESPONSE')
    def response(ctx: Server, address: tuple[str, int], body: str):
        print(f'Response from [{address[0]}:{address[1]}]: {body}')

    SERVER.serve()

    while True:
        command = input('Enter command: ')
        message = input('Enter body: ')
        SERVER.send(bytes(f'{command} {message}', 'UTF-8'), localIP, 20001)