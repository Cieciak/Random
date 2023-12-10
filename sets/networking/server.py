import socket, threading
from dataclasses import dataclass

from typing import Callable

@dataclass
class Address:
    host: str
    port: int


class Server:
    # Maximum size of the buffer
    BUFFER_SIZE = 1024

    def __init__(self, address: Address):
        # Make serve socket
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((address.host, address.port))

        # Server variables
        self.address = address
        self.running = True
        self.data = {}

        # Commands handlers
        self.commands: dict[str, Callable] = {}

    def __loop(self):
        '''Main loop of the server'''
        while self.running:
            # Get message
            message, address = self.socket.recvfrom(self.BUFFER_SIZE)
            address = Address(host = address[0], port = address[1])
            print(f'Message from [{address.host}:{address.port}]: {message}')

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
        '''Create thread for hanling incoming requests'''
        __thread = threading.Thread(
            target = self.__loop,
            daemon = True,
            group  = None,
            name   = f'Mainloop of {self.address.host}:{self.address.port}',
        )
        __thread.start()

    def send(self, buffer: bytes, address: Address):
        self.socket.sendto(buffer, (address.host, address.port))

    def command(self, name: str):
        def decorator(function: Callable):
            self.commands[name] = function
        
        return decorator
    
    @staticmethod
    def parse(buffer: bytes) -> tuple[str, str]:
        raw = buffer.decode('UTF-8')
        command, body = raw.split(' ', 1)

        return command, body