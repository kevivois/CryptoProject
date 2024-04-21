import typing
from datetime import datetime
from threading import Thread

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QStyle, QComboBox, \
    QDialog, \
    QDialogButtonBox
from PyQt5 import QtGui
from PyQt5 import uic

from SocketThread import SocketThread
from conversion import int_to_str, str_to_intarray, intarray_to_str
from Message import Message


class PopupRSA(QDialog):
    closed = pyqtSignal()

    def __init__(self, socketThread: SocketThread):
        super(PopupRSA, self).__init__()
        uic.loadUi("RSA_generator.ui", self)
        self.__is_closed = True
        self.socketThread = socketThread
        self.qLineEdit_n = self.findChild(QLineEdit, "lineEdit_n")
        self.qLineEdit_e = self.findChild(QLineEdit, "lineEdit_e")
        self.qLineEdit_d = self.findChild(QLineEdit, "lineEdit_d")
        self.QLineEdit_customKey = self.findChild(QLineEdit, "lineEdit_customKey")
        self.btnGenerate = self.findChild(QPushButton, "btnGenerate")
        self.qDialogWindow = self.findChild(QDialogButtonBox, "buttonBox")
        self.qDialogWindow.accepted.connect(self.window_closed)
        self.qDialogWindow.rejected.connect(self.window_closed)
        self.btnGenerate.clicked.connect(self.generate)

    def generate(self):
        pass
        try:
            p, q = self.socketThread.socket.generate_rsa_p_q()
            n, e, d = self.socketThread.socket.generate_rsa_keypair(p, q)
            self.qLineEdit_n.setText(str(n))
            self.qLineEdit_e.setText(str(e))
            self.qLineEdit_d.setText(str(d))
        except Exception as e:
            raise e

    def get_data(self):
        return int(self.qLineEdit_n.text()), int(self.qLineEdit_e.text()), int(self.qLineEdit_d.text())

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.window_closed()

    def open(self):
        self.__is_closed = False
        self.show()

    def is_closed(self):
        return self.__is_closed

    def window_closed(self):
        self.__is_closed = True
        self.closed.emit()
