from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QStyle, QComboBox
from PyQt5 import uic

from SocketThread import SocketThread
from conversion import int_to_str,str_to_intarray,intarray_to_str

class UI(QMainWindow):
    def __init__(self, filename: str, socketThread: SocketThread):
        super(UI, self).__init__()
        uic.loadUi(filename, self)
        self.socketThread = socketThread
        self.socketThread.set_received_message_callback(self._received_message_callback)
        self.sendButton = self.findChild(QPushButton, 'pushButton_send')
        self.decryptButton = self.findChild(QPushButton, 'pushButton_decrypt')
        self.lstMessagesSend = self.findChild(QListWidget, 'listWidget_sentMessages')
        self.lstMessagesReceived = self.findChild(QListWidget, 'listWidget_receivedMessages')
        self.encryptCombo = self.findChild(QComboBox, 'comboBox_encryptMethod')
        self.decryptCombo = self.findChild(QComboBox, 'comboBox_decryptMethod')
        self.messageTypeCombo = self.findChild(QComboBox, 'comboBox_messageType')
        self.encryptKey = self.findChild(QLineEdit, 'lineEdit_encryptKey')

        self.txtSend = self.findChild(QLineEdit, 'lineEdit_message')
        self.sendButton.clicked.connect(self.send_text_callback)
        self.show()

    def send_text_callback(self):
        try:
            self.__send_text_callback()
        except Exception as e:
            raise e

    def _received_message_callback(self,text):
        try:
            self.lstMessagesReceived.addItem(intarray_to_str(text))
        except Exception as e:
            print(e)
    def __send_text_callback(self):
       if self.txtSend.text() != '':
            message = str_to_intarray(self.txtSend.text())
            # self.txtSend.clear()
            messageType = self.messageTypeCombo.currentText()
            if messageType == 'private':
                messageType = 's'
            if messageType == 'public':
                messageType = 't'
            encryptKey = self.encryptKey.text()
            encryptMethod = self.encryptCombo.currentText()
            if encryptMethod in ["RSA","Vigenère","Shift","Diffie-Hellman"]:
                if encryptMethod == 'RSA':
                    pass
                    # self.socketThread.socket.sendRSA(message, encryptKey)
                if encryptMethod == "Vigenère":
                    self.socketThread.socket.send_vigenere(message, messageType, encryptKey)
                if encryptMethod == "Shift":
                    self.socketThread.socket.send_shift(message, messageType, int(encryptKey))
                if encryptMethod == "Diffie-Hellman":
                    pass
                    # self.socketThread.socket.sendDiffieHellman(message, encryptKey)
                if encryptMethod == "none":
                    self.socketThread.socket.send(message, messageType)
                print(message)
                self.lstMessagesSend.addItem(intarray_to_str(message))
