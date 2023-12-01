import socket, pprint, os, select
from socket import AddressFamily, SocketKind
import threading

class CP3Socket(socket.socket):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.currently_handled = False


def recvall(sock: CP3Socket, bufsize: int) -> bytes:
    output = b''

    # Collect packets
    while True:
        packet: bytes = sock.recv(bufsize)
        output += packet

        # Break loop on empty packet or CP3 end
        if not packet or output.endswith(b'}\01\01'): return output


##

import json 
class CPPP_JSON_Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytearray):
            return obj.decode('UTF-8')
        elif isinstance(obj, bytes):
            return obj.decode('UTF-8')
        return json.JSONEncoder.default(self, obj)

class TempParser:

    def __init__(self) -> None:
        pass

    def parse(self, raw_data: bytearray) -> tuple[dict, object]:
        parsed = json.loads(raw_data[:-2])
        return parsed['head'], bytes(parsed['body'], 'utf-8')
    
##

class Message:
    parser: TempParser = TempParser()

    def __init__(self, raw_data: bytes = None, head: dict = None, body: bytearray = None):
        self.__raw: bytes = raw_data

        if raw_data:
            self.head, self.body = self.parser.parse(raw_data)
        else:
            self.head:      dict = head
            self.body: bytearray = body

    def __repr__(self) -> str:
        return f'Header: {pprint.pformat(self.head, indent = 4)}\nBody: [\n{self.body}\n]'

    @classmethod
    def empty(cls):
        return cls(head = {'method': 'NONE'}, body = b'')

    @classmethod
    def error(cls, name: str, reason: str = None):
        message = f'Error {name}\nReason: {reason}'

        return cls(
            head = {'method': 'ERROR'},
            body = bytes(message, 'utf-8')
        )

    @classmethod
    def response(cls, payload: bytes):
        return cls(
            head = {'method': 'RESPONSE'},
            body = payload
        )

    @property
    def raw(self):
        JSON = {
            'head': self.head,
            'body': self.body,
        }

        self.__raw = bytes(
            json.dumps(
                JSON,
                cls = CPPP_JSON_Encoder,
            ),
            encoding = "utf-8"
        ) + b'\01\01'
        
        return self.__raw

    def add_header(self, header: dict):
        for key, value in header.items(): self.head[key] = value

    def add_body(self, data: bytes):
        self.body = data

class Server:
    ## Get connection -->
    ## Set socket as handled -->
    ## Create task handler -->
    ## Start task -->
    ## On finish move connection to connection pool

    MAX_BUFFER = 4096

    def __init__(self, address: str, port: int, *, path = os.getcwd()):
        # Server config
        self.address = address
        self.port = port
        self.root = path

        self.handlers = {
            '__default__': self.__default
        }

        self.connections: list[CP3Socket] = []
        self.handled: list[CP3Socket] = []
        self.server_socket = CP3Socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((address, port))
        self.server_socket.listen(10)

        self.connections += [self.server_socket]

    def __default(self, sock):
        while True:
            raw = recvall(sock, self.MAX_BUFFER)
            if not raw: continue
            print(raw)

    def __handler(self, sock: socket.socket):
        task = threading.Thread(
            group = None,
            target = self.__default,
            kwargs = {'sock': sock},
            daemon = True,
        )

        return task

    def __TLH(self, sock):
        ...

    def create_task(self, sock: CP3Socket):
        task = threading.Thread(
            group = None,
            target = self.__TLH,
            kwargs = {'sock': sock},
            daemon = True,
        )


    def serve(self):
        #TODO: Add init function
        while True:
            # Wait for read
            read, write, error = select.select(self.connections, [], [])

            for socket in read:
                # Accept connection
                if socket == self.server_socket:
                    incoming, address = self.server_socket.accept()
                    self.connections += [incoming]
                # Create handler to serve the connction
                else:
                    self.handled.append(socket)
                    self.connections.remove(socket)

                    task = self.create_task(socket)

                    task.start()

if __name__ == '__main__':
    SERVER = Server('127.0.0.1', 8000)

    SERVER.serve()