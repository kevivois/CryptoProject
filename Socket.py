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
        vigenered_message = ""
        for p in range(len(msg)):
            v = (int.from_bytes(bytes(msg[p], "utf-8"), "big") + ord(key[p % len(key)])).to_bytes(4, "big")
            vigenered_message += chr(int.from_bytes(bytes(msg[p], "utf-8"), "big") + ord(key[p % len(key)]))
            lgth = 4 - len(v)
            payload += b'\x00' * lgth + v
        self.sock.send(payload)
        print("vigenered message :" + vigenered_message)
        return len(payload)

    def decode_vigenere(self, msg: str, message_type: str, key: str):
        message = ""
        for p in range(len(msg)):
            v = (int.from_bytes(bytes(msg[p], "utf-8"), "big") - ord(key[p % len(key)])).to_bytes(4, "big")
            decoded_char = chr(int.from_bytes(bytes(msg[p], "utf-8"), "big") - ord(key[p % len(key)]))
            message += decoded_char
        return message

    def vigenere_analysis(self, seq: str, key_length: int):
        data = defaultdict(list)
        message = ""

        for idx, value in enumerate(seq):
            data[idx % key_length].append(value)

        for key, value in data.items():
            letter_counts = Counter(value)
            most_frequent_letter = max(letter_counts, key=letter_counts.get)
            shift = ord('E') - ord(most_frequent_letter)

            for idx, c in enumerate(value):
                value[idx] = chr((ord(c) + shift) % 128)
        doing = True
        idx=0
        while doing:
            if data[idx]:
                message += data[idx].pop(0)
                idx += 1
                if idx > key_length - 1:
                    idx = 0
            else:
                doing=False

        return message

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

    def frequenceAnalysisShift(msg: str):
        foo = 0

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
