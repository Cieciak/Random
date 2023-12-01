import socket, select, os, os.path, uuid, pprint
import json 

def recvall(sock: socket.socket, bufsize: int) -> bytes:
    output = b''
    while True:
        raw_data = sock.recv(bufsize)
        output += raw_data
        if not raw_data or output.endswith(b'}\01\01'): return output

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

class Client:
    MAX_BUFFER = 4096

    def __init__(self):
        self.whoami = uuid.uuid4()
        self.sock = socket.socket()

    def request(self, address: str, port: int, message: Message) -> Message:
        sock = socket.socket()
        sock.connect((address, port))
        message.add_header({'whoami': self.whoami.bytes.hex()})
        sock.sendall(message.raw)

        response = recvall(sock, self.MAX_BUFFER)
        sock.close()

        return Message(raw_data = response)

    def connect(self, address: str, port: int):
        self.sock.connect((address, port))

    def send(self, message: Message):
        message.add_header({'whoami': self.whoami.bytes.hex()})
        self.sock.sendall(message.raw)


if __name__ == '__main__':
    CLIENT = Client()

    

    CLIENT.connect('127.0.0.1', 8000)
    while True:
        text = input('>>')
        msg = Message(body=bytearray(text, 'utf-8'), head={})
        CLIENT.send(msg)
    input()