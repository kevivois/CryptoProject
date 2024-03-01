import socket

class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))
    def send(self, msg, messageType):
        payload = bytes("ISC", 'utf-8') + bytes(messageType, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        for p in msg:
            lgth = 4 - len(bytes(p, 'utf-8'))
            payload += b'\x00' * lgth + bytes(p, 'utf-8')
        self.sock.send(payload)
        return len(payload)

    def sendshift(self, msg: str, messageType: str, amount: int):
        payload = bytes("ISC", 'utf-8') + bytes(messageType, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        shifted_message = ""
        for p in msg:
            v = (int.from_bytes(bytes(p, "utf-8")) + amount).to_bytes(4)
            shifted_message += chr(int.from_bytes(bytes(p, "utf-8")) + amount)
            lgth = 4 - len(v)
            payload += b'\x00' * lgth + v
        print("shifted message :"+ shifted_message)
        self.sock.send(payload)
        return len(payload)

    def sendxor(self, msg: str, messageType: str, amount: int):
        payload = bytes("ISC", 'utf-8') + bytes(messageType, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        for p in msg:
            v = int.from_bytes(bytes(p, "utf-8")) ^ amount
            v = v.to_bytes(4)
            lgth = 4 - len(v)
            payload += b'\x00' * lgth + v
        self.sock.send(payload)
        return len(payload)

    def decodeXorMessage(self, payload: str):
        pass

    def receive(self, typeToWait='t') -> str:
        waiting = True
        while waiting:
            data = self.sock.recv(2048)
            header = data[0:3].decode("utf-8")
            if header == "ISC" and data[3:4].decode("utf-8") == typeToWait:
                waiting = False

        header = data[0:3].decode("utf-8")
        if header == "ISC":
            mode = data[3:4].decode("utf-8")
            lgth = int.from_bytes(data[4:6], "big")
            content = data[6:len(data)].decode("utf-8")
            message = "".join(c for c in content if c != '\x00')
            return message
        return ""
