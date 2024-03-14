import socket
from collections import defaultdict, Counter


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
            lgth = 4 - len(bytes(p, 'utf-8'))
            payload += b'\x00' * lgth + bytes(p, 'utf-8')
        self.sock.send(payload)
        return len(payload)

    def send_vigenere(self, msg: str, message_type: str, key: str):
        payload = bytes("ISC", 'utf-8') + bytes(message_type, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        coded_msg = ""
        for p in range(len(msg)):
            single_value = (ord(msg[p]) + ord(key[p % len(key)]))
            bytes_value = single_value.to_bytes(4, "big")
            coded_msg += chr(single_value % 1114112)
            lgth = 4 - len(bytes_value)
            payload += b'\x00' * lgth + bytes_value
        self.sock.send(payload)
        return coded_msg

    def decode_vigenere(self, coded_msg: str, key: str) -> str:
        decoded_msg = ""
        for i in range(len(coded_msg)):
            single_value = (ord(coded_msg[i]) - ord(key[i % len(key)])) % 1114112
            decoded_char = chr(single_value)
            decoded_msg += decoded_char
        return decoded_msg

    """
    Essai non concluant mdr
    """

    def vigenere_analysis(self, seq: str, key_length: int):
        data = defaultdict(list)
        message = ""

        for idx, value in enumerate(seq):
            data[idx % key_length].append(value)

        for key, value in data.items():
            letter_counts = Counter(value)
            most_frequent_letter = max(letter_counts, key=letter_counts.get)
            shift_start = ord('E')
            if str(most_frequent_letter).islower():
                shift_start = ord('e')

            shift = (shift_start - ord(most_frequent_letter)) % 26

            for idx, c in enumerate(value):
                value[idx] = self.shift_max(c, shift)

        doing = True
        idx = 0
        while doing:
            if data[idx]:
                message += data[idx].pop(0)
                idx += 1
                if idx > key_length - 1:
                    idx = 0
            else:
                doing = False
        return message

    def shift_max(self, c: str, cnt: int) -> str:
        if c.isupper():
            mnV = ord('A')
            mxV = ord('Z')
            v = ord(c) + cnt
            result = chr((v - mnV) % 26 + mnV)
            return result
        elif c.islower():
            mnV = ord('a')
            mxV = ord('z')
            v = ord(c) + cnt
            result = chr((v - mnV) % 26 + mnV)
            return result
        else:
            return c

    def send_shift(self, msg: str, message_type: str, amount: int):
        payload = bytes("ISC", 'utf-8') + bytes(message_type, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        shifted_message = ""
        for p in msg:
            v = (int.from_bytes(bytes(p, "utf-8"), "big") + amount).to_bytes(4, "big")
            shifted_message += chr(int.from_bytes(bytes(p, "utf-8"), "big") + amount)
            lgth = 4 - len(v)
            payload += b'\x00' * lgth + v
        print("shifted message :" + shifted_message)
        self.sock.send(payload)
        return len(payload)

    def send_xor(self, msg: str, message_type: str, amount: int):
        payload = bytes("ISC", 'utf-8') + bytes(message_type, 'utf-8')
        payload += len(msg).to_bytes(2, byteorder='big')
        for p in msg:
            v = int.from_bytes(bytes(p, "utf-8")) ^ amount
            v = v.to_bytes(4)
            lgth = 4 - len(v)
            payload += b'\x00' * lgth + v
        self.sock.send(payload)
        return len(payload)

    def receive(self, typeToWait='t') -> str:
        waiting = True
        while waiting:
            data = self.sock.recv(2048)
            header = data[0:3].decode("utf-8")
            if header == "ISC" and data[3:4].decode("utf-8") == typeToWait:
                waiting = False

        header = data[0:3].decode("utf-8")
        if header == "ISC":
            mode = data[3:4].decode("utf-8")
            lgth = int.from_bytes(data[4:6], "big")
            content = data[6:len(data)].decode("utf-8")
            message = "".join(c for c in content if c != '\x00')
            return message
        return ""
