import time

import conversion
from Socket import MySocket


def get_user_input(prompt):
    return input(prompt).strip()


def encode_message(b, cmd, messageType):
    possibilities = ["shift", "xor", "vigenere",'RSA']
    idxChoice = -1
    for idx, v in enumerate(possibilities):
        if str(v).lower() in cmd.split(" ")[1].lower():
            idxChoice = idx

    type_encoding = idxChoice + 1
    cmd = conversion.str_to_intarray(cmd)
    b.send(cmd, messageType)

    msg_byte = b.receive('s')
    msg = conversion.intarray_to_str(msg_byte)
    print(msg)
    encode_data = msg.split(" ")[-1]
    msg_to_encode = b.receive(messageType)
    print(conversion.intarray_to_str(msg_to_encode))

    if type_encoding == 1:
        b.send_shift(msg_to_encode, messageType, int(encode_data))
    elif type_encoding == 2:
        b.send_xor(msg_to_encode, messageType, int(encode_data))
    elif type_encoding == 3:
        coded_message = b.send_vigenere(msg_to_encode, messageType, encode_data)
        decoded_message = conversion.intarray_to_str(b.decode_vigenere(coded_message,encode_data))
        print("decoded message:" + decoded_message)
    elif type_encoding == 4:
        n = msg.split("=")[1].split(",")[0]
        e = msg.split("=")[-1]
        coded_message = b.send_better_RSA(msg_to_encode, messageType, int(n),int(e))

    response = conversion.intarray_to_str(b.receive(messageType))
    print(response,'r')


def main():
    b = MySocket()
    b.connect("vlbelintrocrypto.hevs.ch", 6000)
    while True:
        cmd = get_user_input("Write your command: ")
        shift = get_user_input("Do you want to encode the message? [no|yes]: ")
        message_type = get_user_input("Specify your message type [t:@everyone|s:server only]: ")

        encode_message_flag = "yes" in shift
        message_type = "t" if "t" in message_type else "s"
        if encode_message_flag:
            encode_message(b, cmd, message_type)
        else:
            cmd = conversion.str_to_intarray(cmd)
            b.send(cmd, message_type)
            response = b.receive(message_type)
            print(response)


if __name__ == "__main__":
    main()
