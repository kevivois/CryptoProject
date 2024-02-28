import socket


class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))
        print("is connected")

    def send(self, msg, messageType):
        payload = bytes("ISC", 'utf-8') + bytes(messageType, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        for p in msg:
            lgth = 4 - len(bytes(p,'utf-8'))
            payload += b'\x00' * lgth + bytes(p,'utf-8')
        self.sock.send(payload)
        return len(payload)

    def receive(self) -> str:
        data = self.sock.recv(1024)
        header = data[0:3].decode("utf-8")
        if header == "ISC":
            mode = data[3:4].decode("utf-8")
            lgth = int.from_bytes(data[4:6],"big")
            content = data[6:len(data)].decode("utf-8")
            message = ""
            cn=0
            for c in content.replace('\x00',''):
                if cn <= lgth:
                    message+=c
                cn += 1
            return message
        return ""
