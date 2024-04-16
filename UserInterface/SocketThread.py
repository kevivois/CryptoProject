import datetime
import threading
from datetime import time
from typing import Callable
from Socket import MySocket


class SocketThread(threading.Thread):
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.socket = MySocket()
        threading.Thread.__init__(self)
        self.working = True
        self.received_message_callback = Callable[[str], None]

    def run(self):
        print("Socket Thread Started")
        self.socket.connect(self.address, self.port)
        while self.working:
            message = self.socket.receive_all()
            print(message,"message")
            if message:
                self.received_message_callback(message)

    def set_received_message_callback(self, callback):
        self.received_message_callback = callback

    def stop(self):
        self.working = False
