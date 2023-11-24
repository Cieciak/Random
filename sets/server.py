import socket
import multiprocessing

from threading import Thread

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

class ClientThread:

    def __init__(self, socket: socket.socket, address: str):
        self.address = address
        self.socket = socket
        self.alive = True

        self.thread = Thread(
            target = self.loop,
            args = (),
            daemon = True
        )

    def loop(self):
        while self.alive:
            print('loop')
            data = self.socket.recv(1024)
            if data == b'END': break

            print(f'Recieved data: {data}')
        self.socket.send(b'ECHO')
        self.socket.close()

    def start(self): self.thread.start()

class Server:

    def __init__(self, addr: str, port: int):
        # Server config
        self.addr = addr
        self.port = port

        # Bind socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.addr, self.port))
        self.socket.listen()

        # Store clients
        self.client_threads: dict[str, ClientThread] = {}

    def __main_loop(self):
        while True:
            print('Main loop ready for next connection')
            client, address = self.socket.accept()
            print(f'Accepted connection from {address[0]}:{address[1]}')

            self.client_threads[address] = ClientThread(client, address)
            self.client_threads[address].start()


    def serve(self):
        self.__main_thread = Thread(
            target = self.__main_loop,
            daemon = True
        )
        self.__main_thread.start()

    def close(self):
        for client in self.client_threads.keys(): self.client_threads[client].alive = False
        self.socket.close()

server = Server('127.0.0.1', 12345)
try: server.serve()
except RuntimeError: pass

input()
server.close()