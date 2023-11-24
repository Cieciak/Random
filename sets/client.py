import socket
import threading

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# 1st send, 2nd recv
class Client:

    def __init__(self, addr: str, port: int):
        self.addr = addr
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.addr, self.port))

    def __handle_incoming(self):
        data = ''
        while True:
            try:data = self.socket.recv(1024)
            except OSError: pass
            if data == b'END': break
            print(data)

    def listen(self):
        self.__listening_thread = threading.Thread(
            target = self.__handle_incoming,
        )
        self.__listening_thread.start()

    def send(self, data):
        self.socket.send(data)

# Create a TCP socket
client = Client(SERVER_HOST, SERVER_PORT)
client.listen()

client.connect()
while True: client.send(bytes(input('Send: '), 'utf-8'))
