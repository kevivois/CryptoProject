import socket


class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

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

            payload += bytes(str(p).zfill(4), 'utf-8')
        self.sock.send(payload)
        return len(payload)

    def receive(self, size) -> str:
        data = self.sock.recv(size)
        header = data[0:3].decode("utf-8")
        print("data:"+data.decode("utf-8") + " header :" + header)
        if header == "ISC":
            mode = data[3:4].decode("utf-8")
            lgth = int.from_bytes(data[4:6],"big")
            content = data[6:len(data)].decode("utf-8")
            message = ""
            cn=0
            for c in content.split("000"):
                if cn <= lgth:
                    message+=c
                cn += 1
            return message
        return ""
