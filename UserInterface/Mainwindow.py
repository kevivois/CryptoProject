from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class UI(QMainWindow):
    def __init__(self, filename: str):
        super(UI, self).__init__()
        uic.loadUi(filename, self)
        self.show()
