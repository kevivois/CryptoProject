import array
import base64
import codecs
import math
import socket
import struct
from collections import defaultdict, Counter
from typing import List

import conversion


class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg, message_type):
        payload = bytes("ISC", 'utf-8') + bytes(message_type, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        for p in msg:
            payload += p.to_bytes(4,'big')
        self.sock.send(payload)
        return len(payload)

    def send_vigenere(self, msg, message_type: str, key: str):
        payload = bytes("ISC", 'utf-8') + bytes(message_type, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        arr = []
        for idx, int_value in enumerate(msg):
            normal_value = int_value + ord(key[idx % len(key)])
            payload += normal_value.to_bytes(4,'big')
            arr.append(normal_value)
        print(payload)
        self.sock.send(payload)
        return arr

    def decode_vigenere(self, coded_msg, key: str):
        arr = []
        for idx, int_value in enumerate(coded_msg):
            normal_value = int_value - ord(key[idx % len(key)])
            arr.append(normal_value)
        return arr

    def send_shift(self, msg, message_type: str, amount: int):
        payload = bytes("ISC", 'utf-8') + bytes(message_type, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        for p in msg:
            payload += (p + amount).to_bytes(4, "big")
        self.sock.send(payload)
        return len(payload)

    def send_xor(self, msg, message_type: str, amount: int):
        payload = bytes("ISC", 'utf-8') + bytes(message_type, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        for p in msg:
            v = (p ^ amount).to_bytes(4)
            payload += v
        self.sock.send(payload)
        return len(payload)

    def receive(self, typeToWait='t'):
        waiting = True
        arr = []
        data = None
        while waiting:
            data = self.sock.recv(2048)
            header = data[0:3].decode("utf-8")
            if header == "ISC" and data[3:4].decode("utf-8") == typeToWait:
                waiting = False

        header = data[0:3].decode("utf-8")
        if header == "ISC":
            mode = data[3:4].decode("utf-8")
            lgth = int.from_bytes(data[4:6], "big")
            content = data[6:]
            for i in range(0,len(content),4):
                try:
                    arr.append(int.from_bytes(content[i:i+4]))
                except:
                    pass
            return arr
        return []