import array
import base64
import codecs
import math
import socket
import struct
from collections import defaultdict, Counter
from typing import List

import conversion

from math import sqrt

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
    
    @staticmethod
    def prime(n : int):
        for i in range(2, int(sqrt(n))+1) :
            if(n % i == 0):
                return False
        return True

    @staticmethod
    def coprime(a : int, b : int):
        if(a <b) :
            for i in range(2, a) :
                if(a %i == 0 and b%i == 0):
                    return False
        return True
    
    def key_generate(self, p : int, q : int, e : int):
        if self.prime(p) and self.prime(q): 
            n = q*p
            k = (p-1)*(q-1)
            
            if e < k and self.coprime(e, k):
                d = 0
                b = 1
                res = 0
                while res != 1 :
                    res = d * e + b * k
                    b += 1
                return [n, e, d]
        else:
            return False




    def send_RSA(self, msg : str, message_type: str, n : int, e : int ):
        payload = bytes("ISC", 'utf-8') + bytes(message_type, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        encoded_msg = []
        for p in msg:
            val = pow(p, int(e))% int(n)
            v = val.to_bytes(4, "big")
            encoded_msg.append(val)
            payload += v
            encoded_msg += v.decode("utf-8", 'replace')
            lgth = 4 - len(v)
            payload += b'\x00' * lgth + v
            print(encoded_msg)
        self.sock.send(payload)
        return encoded_msg
    
    def send_better_RSA(self, msg : str, message_type: str, n : int, e : int ):
        payload = bytes("ISC", 'utf-8') + bytes(message_type, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        encoded_msg = ""
        for p in msg:
            val = int(e) % int(n)
            valeur *= (int.from_bytes(bytes(p, "utf-8"), "big"))
            valeur %= int(n)
            v = valeur.to_bytes(4, "big")
            encoded_msg += v.decode("utf-8", 'replace')
            lgth = 4 - len(v)
            payload += b'\x00' * lgth + v
            print(encoded_msg)
        self.sock.send(payload)
        return encoded_msg

    def decode_RSA(self, msg : str, n : int, d : int):
        decoded_msg = ""
        for p in range(len(msg)):
            v = (int.from_bytes(bytes(msg[p], "utf-8"), "big") ).to_bytes(4, "big")
            vigenered_message += chr(int.from_bytes(bytes(msg[p], "utf-8"), "big"))
            lgth = 4 - len(v)
            payload += b'\x00' * lgth + v
        return decoded_msg

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
