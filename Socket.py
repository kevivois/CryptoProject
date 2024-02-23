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
        cnt=0
        payload = bytes("ISC",'utf-8') + bytes(messageType,'utf-8')
        cnt+=4
        payload+=len(msg).to_bytes(2,byteorder='big')
        cnt+=2
        for p in msg:
            payload += bytes(str(p).zfill(4),'utf-8')
            cnt+=4
        self.sock.send(payload)
        return cnt
    def receive(self, size):
        while True:
            message = str(self.sock.recv(size))
            print("received :" + message)
