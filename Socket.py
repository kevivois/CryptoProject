import array
import base64
import codecs
import math
import random
import socket
import struct
from collections import defaultdict, Counter
from typing import List

import conversion
from UserInterface.Message import Message
from math import sqrt


class RandomGenerator:
    current_value: int

    def __init__(self, seed: int = 0) -> None:
        self.current_value = seed

    def random(self):
        a = 1664525
        b = 1013904223
        n = 1 << 32
        rand = (self.current_value * a + b) % n
        self.current_value = rand
        return rand


class MySocket:

    # *setup

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(True)
        self.__sending = False
        self.host = None
        self.port = None
        self.__available = False
        self.__abortingReceived = False
        self.messages = []
        self.random_generator = RandomGenerator(314)
        self.current_rsa_key_encode_pair = (None, None)
        self.current_rsa_key_decode_pair = (None, None)

    def connect(self, host, port):
        self.host = host
        self.port = port
        self.sock.connect((host, port))
        self.__available = True

    def stop(self):
        self.sock.close()

    def abort_actual_receiving(self):
        self.__abortingReceived = True

    def send(self, msg, message_type):
        payload = bytes("ISC", 'utf-8') + bytes(message_type, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        for p in msg:
            payload += p.to_bytes(4, "big")
        self.send_payload(payload)
        return len(payload)

    def send_payload(self, payload):
        try:
            self.sock.send(payload)
        except socket.error as e:
            print(e)
            self.reconnect()
        except Exception as e:
            print(e)

    def reconnect(self):
        self.__sending = False
        self.abort_actual_receiving()
        try:
            self.sock.close()
        except socket.error as e:
            pass
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(self.host, self.port)

    def isSending(self):
        return self.__sending

    @staticmethod
    def is_prime(n: int):
        if n <= 1:
            return False
        for i in range(2, int(sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def coprime(a: int, b: int):
        mn = min(a, b)
        for i in range(2, mn):
            if a % i == 0 and b % i == 0:
                return False
        return True

    def key_rand_prime(self):
        res = 0
        numb = self.random_generator.random() % 669  # to change (random always the same ? )
        with open("prime.txt") as pf:
            res = int(pf.read().splitlines()[numb])
        return res


    def diffieHellman(self, p: int):
        q: int = int(p) - 1
        liste = []
        for i in range(2, q - 1):
            if self.is_prime(i):
                liste.append(i)
        for g in range(2, int(q)):
            is_generator = True
            for j in liste:
                if pow(g, q // j, int(p)) == 1:
                    is_generator = False
                    break
            if is_generator:
                return g
        raise ValueError("diffieHellman didnt returned generator value")

    def generate_rsa_p_q(self):
        p: int = self.key_rand_prime()
        q: int = self.key_rand_prime()
        while not (self.is_prime(q) and self.is_prime(p) and p != q):
            p: int = self.key_rand_prime()
            q: int = self.key_rand_prime()
        return p, q

    def generate_rsa_keypair(self, p: int, q: int):
        def modular_inverse(a, b):
            """Calcule l'inverse multiplicatif de e modulo phi"""
            def extended_gcd(a, b):
                if a == 0:
                    return b, 0, 1
                else:
                    g, x, y = extended_gcd(b % a, a)
                    return g, y - (b // a) * x, x

            g, x, _ = extended_gcd(a, b)
            if g == 1:
                return x % b
            else:
                raise ValueError("L'inverse multiplicatif n'existe pas.")
        if self.is_prime(p) and self.is_prime(q) or p == q:
            n = q * p
            k = (p - 1) * (q - 1)
            while True:
                e = random.randint(2, k)
                is_co_prime = self.coprime(e, k)
                if e < k and is_co_prime:
                    break
            d = modular_inverse(e,k) #aaa1
            return e, d, n
        else:
            raise ValueError("p et q ne doivent pas être premiers et ne doivent pas être égaux")

    def modular_pow(self, b, e, m):
        r = 1
        if 1 & e:
            r = b
        while e:
            e >>= 1
            b = (b * b) % m
            if e & 1: r = (r * b) % m
        return r

    def send_RSA(self, msg, message_type: str, n: int, e: int):
        payload = bytes("ISC", 'utf-8') + bytes(message_type, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        msg_array = []
        for p in msg:
            valeur = self.modular_pow(p, e, n)
            msg_array.append(valeur)
            payload += valeur.to_bytes(4, "big")
        self.send_payload(payload)
        return msg_array

    def decode_RSA(self, msg, n: int, d: int):
        decoded_array = []
        for c in msg:
            valeur = self.modular_pow(c, d, n)
            decoded_array.append(valeur)
        return decoded_array

    def send_vigenere(self, msg, message_type: str, key: str):
        payload = bytes("ISC", 'utf-8') + bytes(message_type, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        arr = []
        for idx, int_value in enumerate(msg):
            normal_value = int_value + ord(key[idx % len(key)])
            payload += normal_value.to_bytes(4, 'big')
            arr.append(normal_value)
        self.send_payload(payload)
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
        message = []
        for p in msg:
            payload += (p + amount).to_bytes(4, "big")
            message.append(p + amount)
        self.send_payload(payload)
        return message

    def decode_shift(self, msg, amount: int):
        arr = []
        for p in msg:
            arr.append(p - amount)
        return arr

    def send_xor(self, msg, message_type: str, amount: int):
        payload = bytes("ISC", 'utf-8') + bytes(message_type, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        for p in msg:
            v = (p ^ amount).to_bytes(4)
            payload += v
        self.send_payload(payload)
        return len(payload)

    def receive_all(self):
        try:
            return self.__receive_all()
        except Exception as e:
            print("error while receiving : ", e)
        return "", []

    def start_shift_encode_test(self, value: int):
        self.remove_all_admin_messages()
        cmd_text = "task shift encode " + str(value if value <= 10000 else 10000)
        self.send(conversion.str_to_intarray(cmd_text), "s")
        msg: Message = self.get_last_private_message()
        encode_data = msg.get_string_message().split(" ")[-1]
        msg_to_encode: Message = self.get_last_private_message()
        msg_encoded = self.send_shift(msg_to_encode.get_int_message(), "s", int(encode_data))
        result_message: Message = self.get_last_private_message()
        return [Message("s", conversion.str_to_intarray(cmd_text), False).toString(), msg.toString(),
                msg_to_encode.toString(), Message("t", msg_encoded, False).toString(), result_message.toString()]

    def start_rsa_encode_test(self, value: int):
        self.remove_all_admin_messages()
        cmd_text = "task RSA encode " + str(value if value <= 10000 else 10000)
        self.send(conversion.str_to_intarray(cmd_text), "s")
        msg: Message = self.get_last_private_message()
        n = msg.get_string_message().split("=")[1].split(",")[0]
        e = msg.get_string_message().split("=")[-1]
        msg_to_encode: Message = self.get_last_private_message()
        msg_encoded = self.send_RSA(msg_to_encode.get_int_message(), "s", int(n), int(e))
        result_message: Message = self.get_last_private_message()
        return [Message("s", conversion.str_to_intarray(cmd_text), False).toString(), msg.toString(),
                msg_to_encode.toString(), Message("t", msg_encoded, False).toString(), result_message.toString()]

    def start_vigenere_encode_test(self, value: int):
        self.remove_all_admin_messages()
        cmd_text = "task vigenere encode " + str(value)
        self.send(conversion.str_to_intarray(cmd_text), "s")
        msg: Message = self.get_last_private_message()
        key = msg.get_string_message().split(" ")[-1]
        msg_to_encode: Message = self.get_last_private_message()
        msg_encoded = self.send_vigenere(msg_to_encode.get_int_message(), "s", key)
        result_message: Message = self.get_last_private_message()

        return [Message("s", conversion.str_to_intarray(cmd_text), False).toString(), msg.toString(),
                msg_to_encode.toString(), Message("t", msg_encoded, False).toString(), result_message.toString()]

    def start_diffie_encode_test(self):
        self.remove_all_admin_messages()
        cmd_text = "task DifHel"
        self.send(conversion.str_to_intarray(cmd_text), "s")
        msg: Message = self.get_last_private_message()
        p = self.key_rand_prime()
        g = self.diffieHellman(p)
        keys_data = str(p) + "," + str(g)
        keys_data_message = Message("s", conversion.str_to_intarray(keys_data))
        self.send(keys_data_message.get_int_message(), "s")
        halfkey = self.random_generator.random()
        publicKey = self.modular_pow(g, halfkey, p)
        server_key_info: Message = self.get_last_private_message()
        self.send(conversion.str_to_intarray(str(publicKey)), "s")
        server_key_message: Message = self.get_last_private_message()
        print(server_key_message.get_string_message())
        shared_key = self.modular_pow(int(server_key_message.get_string_message()), halfkey, p)
        self.send(conversion.str_to_intarray(str(shared_key)), "s")
        shared_key_info = self.get_last_private_message()
        self.send(conversion.str_to_intarray(str(shared_key)), "s")
        result:Message = self.get_last_private_message()
        return [Message("s", conversion.str_to_intarray(cmd_text), False).toString(), msg.toString(),
                keys_data_message.toString(), Message("t", conversion.str_to_intarray(str(publicKey)), False).toString(),
                server_key_message.toString(), result.toString()]

    def __receive_all(self):
        waiting = True
        arr = []
        data = None
        while waiting and not self.__abortingReceived:
            data = self.sock.recv(6)
            header = data[0:3].decode("utf-8")
            if header == "ISC":
                waiting = False
        if self.__abortingReceived:
            self.__abortingReceived = False
            return "", []
        header = data[0:3].decode("utf-8")
        if header == "ISC":
            mode = data[3:4].decode("utf-8")
            lgth = int.from_bytes(data[4:6], "big")
            content = self.sock.recv(lgth * 4)
            while len(content) < lgth * 4:
                content += self.sock.recv((lgth * 4) - len(content))
            for i in range(0, lgth * 4, 4):
                try:
                    arr.append(int.from_bytes(content[i:i + 4], "big"))
                except:
                    pass
            msg = Message(mode, arr, True)
            self.messages.append(msg)
            return mode, arr
        return "", []

    def get_last_public_message(self, block=False):
        msg = None
        while not msg:
            for message in self.messages.copy():
                if message.mode == "t":
                    msg = message
                    self.messages.remove(message)
                    return msg
            if not block:
                break
            return None

    def get_last_private_message(self, block=True):
        msg = None
        while not msg:
            for message in self.messages.copy():
                if message.mode == "s":
                    self.messages.remove(message)
                    msg = message
                    return msg
            if not block:
                break
        return None

    def remove_all_admin_messages(self):
        for message in self.messages.copy():
            if message.mode == "s":
                self.messages.remove(message)

    def receive(self, typeToWait='t'):
        try:
            return self.__receive(typeToWait)
        except Exception as e:
            print("error while receiving : ", e)
        return None

    def __receive(self, typeToWait='t'):
        waiting = True
        arr = []
        data = None
        while waiting and not self.__abortingReceived:
            data = self.sock.recv(6)
            header = data[0:3].decode("utf-8")
            if header == "ISC" and data[3:4].decode("utf-8") == typeToWait:
                waiting = False
        if self.__abortingReceived:
            self.__abortingReceived = False
            return []
        header = data[0:3].decode("utf-8")
        if header == "ISC":
            mode = data[3:4].decode("utf-8")
            lgth = int.from_bytes(data[4:6], "big")
            content = self.sock.recv(lgth * 4)
            while len(content) < (lgth * 4):
                content += self.sock.recv(lgth - len(content))
            for i in range(0, lgth * 4, 4):
                try:
                    arr.append(int.from_bytes(content[i:i + 4], "big"))
                except Exception as e:
                    print(e)
            return arr
        return []
