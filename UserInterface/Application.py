from typing import List

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDialog
import sys

from Mainwindow import UI

from SocketThread import SocketThread

class Application(QApplication):
    def __init__(self, argv: List[str]):
        super().__init__(argv)
        sys.excepthook = self.handle_error
        self.applicationTimer = QTimer()
        self.applicationTimer.timeout.connect(self.applicationTimer_callback)
        self.applicationTimer.start(100)
        self.socket = SocketThread("vlbelintrocrypto.hevs.ch", 6000)
        self.mainWindow = UI("gui.ui", self.socket)
        self.socket.start()
        self.mainWindow.show()


    def applicationTimer_callback(self):
        pass

    def handle_error(self, cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    application = Application(sys.argv)
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.
    sys.exit(application.exec())
