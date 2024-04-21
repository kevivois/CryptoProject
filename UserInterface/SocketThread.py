from typing import Callable

from PyQt5 import QtCore

from Socket import MySocket


class SocketThread(QtCore.QThread):
    def __init__(self, address, port):
        super().__init__()
        self.address = address
        self.port = port
        self.socket = MySocket()
        self.__working = True
        self.received_message_callback = Callable[[str], None]
        self.adminMessages = []

    def run(self):
        self.socket.connect(self.address, self.port)
        while self.__working:
            if self.socket.is_ready():
                type, message = self.socket.receive_all()
                if message:
                    if type == 't':
                        self.received_message_callback(self.socket.get_last_public_message())

    def set_received_message_callback(self, callback):
        self.received_message_callback = callback

    def stop(self):
        self.__working = False
        self.socket.stop()
