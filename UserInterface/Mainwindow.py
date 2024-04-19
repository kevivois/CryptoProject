import typing
from datetime import datetime
from threading import Thread

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QStyle, QComboBox
from PyQt5 import uic

from SocketThread import SocketThread
from conversion import int_to_str, str_to_intarray, intarray_to_str
from Message import Message


class UI(QMainWindow):
    closed = pyqtSignal()

    def __init__(self, filename: str, socketThread: SocketThread):
        super(UI, self).__init__()
        uic.loadUi(filename, self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.socketThread = socketThread
        self.socketThread.set_received_message_callback(self._received_message_callback)
        self.qSendButton = self.findChild(QPushButton, 'pushButton_send')
        self.qDecryptButton = self.findChild(QPushButton, 'pushButton_decrypt')
        self.qMessagesSend = self.findChild(QListWidget, 'listWidget_sentMessages')
        self.qMessagesReceived = self.findChild(QListWidget, 'listWidget_receivedMessages')
        self.qEncryptCombo = self.findChild(QComboBox, 'comboBox_encryptMethod')
        self.qDecryptCombo = self.findChild(QComboBox, 'comboBox_decryptMethod')
        self.qEncryptKey = self.findChild(QLineEdit, 'lineEdit_encryptKey')
        self.qTxtSend = self.findChild(QLineEdit, 'lineEdit_message')
        self.qDecryptKey = self.findChild(QLineEdit, 'lineEdit_decryptKey')
        self.qSendButton.clicked.connect(self.send_text_callback)
        self.qDecryptButton.clicked.connect(self.decrypt_callback_button)
        self.lstMessagesReceived: typing.List[Message] = []
        self.closed.connect(self.window_closed)

        self.qBtnTestRSA = self.findChild(QPushButton, 'pushButton_RSA')
        self.qBtnTestShift = self.findChild(QPushButton, 'pushButton_shift')
        self.qBtnTestVigenere = self.findChild(QPushButton, 'pushButton_vigenere')
        self.qBtnTestDiffie = self.findChild(QPushButton, 'pushButton_diffie')

        self.qBtnTestRSA.clicked.connect(self.start_rsa_test)
        self.qBtnTestShift.clicked.connect(self.start_shift_test)
        self.qBtnTestDiffie.clicked.connect(self.start_diffie_test)
        self.qBtnTestVigenere.clicked.connect(self.start_vigenere_test)
        self.qLineEditServerKey = self.findChild(QLineEdit, 'lineEdit_OperationValue')
        self.qServerMessages = self.findChild(QListWidget, 'listWidget_serverMessages')

        self.__testing: bool = False
        self.show()

    def start_rsa_test(self):
        Thread(target=self.__start_rsa_test).start()

    def __start_rsa_test(self):
        try:
            if self.__testing:
                return
            self.__testing = True
            messages = self.socketThread.socket.start_rsa_encode_test(int(self.qLineEditServerKey.text()))
            self.qServerMessages.clear()
            for message in messages:
                self.qServerMessages.addItem(message)
            self.__testing = False
        except Exception as e:
            self.__testing = False
            print(e)

    def start_shift_test(self):
        Thread(target=self.__start_shift_test).start()

    def __start_shift_test(self):
        try:
            if self.__testing:
                return
            self.__testing = True
            messages = self.socketThread.socket.start_shift_encode_test(int(self.qLineEditServerKey.text()))
            self.qServerMessages.clear()
            for message in messages:
                self.qServerMessages.addItem(message)
            self.__testing = False
        except Exception as e:
            self.__testing = False
            print(e)

    def __start_vigenere_test(self):
        try:
            if self.__testing:
                return
            self.__testing = True
            messages = self.socketThread.socket.start_vigenere_encode_test(int(self.qLineEditServerKey.text()))
            self.qServerMessages.clear()
            for message in messages:
                self.qServerMessages.addItem(message)
            self.__testing = False
        except Exception as e:
            self.__testing = False
            print(e)

    def start_vigenere_test(self):
        Thread(target=self.__start_vigenere_test).start()

    def start_diffie_test(self):
        if self.__testing:
            return
        self.__testing = True

        self.__testing = False
        pass

    def closeEvent(self, event):
        self.closed.emit()
        QMainWindow.closeEvent(self, event)
        self.socketThread.stop()

    def decrypt_callback_button(self):
        try:
            self.__decrypt_callback_button()
        except Exception as e:
            print(e)

    def __decrypt_callback_button(self):
        decrypt_method = self.qDecryptCombo.currentText()
        decrypt_key = self.qDecryptKey.text()
        message = self.__get_selected_received_message()
        if not message:
            raise ValueError("You must select a message")
        if decrypt_method == "RSA":
            pass
        if decrypt_method == "Vigenère":
            decrypted_message = self.socketThread.socket.decode_vigenere(message.get_int_message(), decrypt_key)
            message = Message("t", decrypted_message)
            self.lstMessagesReceived[self.__get_selected_received_message_index()] = message
            self.qMessagesReceived.selectedItems()[0].setText(message.get_string_message())
        if decrypt_method == "Shift":
            decrypted_message = self.socketThread.socket.decode_shift(message.get_int_message(), int(decrypt_key))
            message = Message("t", decrypted_message)
            self.lstMessagesReceived[self.__get_selected_received_message_index()] = message
            self.qMessagesReceived.selectedItems()[0].setText(message.get_string_message())
        if decrypt_method == "Diffie-Hellman":
            pass

    def window_closed(self):
        self.socketThread.stop()

    def __get_selected_received_message(self):
        try:
            return self.lstMessagesReceived[self.qMessagesReceived.selectedIndexes()[0].row()]
        except:
            return None

    def __get_selected_received_message_index(self):
        try:
            return self.qMessagesReceived.selectedIndexes()[0].row()
        except:
            return None

    def send_text_callback(self):
        try:
            self.__send_text_callback()
        except Exception as e:
            raise e

    def _received_message_callback(self, msg):
        try:
            self.lstMessagesReceived.append(msg)
            self.qMessagesReceived.addItem(msg.get_string_message())
        except Exception as e:
            print(e)

    def __send_text_callback(self):
        if self.qTxtSend.text() != '':
            message = str_to_intarray(self.qTxtSend.text())
            # self.txtSend.clear()
            messageType = 't'
            encryptKey = self.qEncryptKey.text()
            encryptMethod = self.qEncryptCombo.currentText()
            if encryptMethod in ["RSA", "Vigenère", "Shift", "Diffie-Hellman", "None"]:
                if encryptKey == '' and encryptMethod in ["RSA", "Vigenère", "Shift", "Diffie-Hellman"]:
                    print("encrypt key is invalid")
                else:
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
                if encryptMethod == "None":
                    self.socketThread.socket.send(message, messageType)
                self.qMessagesSend.addItem(intarray_to_str(message))
