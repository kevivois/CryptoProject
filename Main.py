import time
from Socket import MySocket


def get_user_input(prompt):
    return input(prompt).strip()


def encode_message(b, cmd, messageType):
    type_encoding = 1 if "shift" in cmd.split(" ")[1] else 2
    type_encoding = int(type_encoding)
    b.send(cmd, messageType)

    msg = b.receive('s')
    encode_length = int(msg.split(" ")[-1])
    msg_to_encode = b.receive(messageType)

    if type_encoding == 1:
        b.sendshift(msg_to_encode, messageType, encode_length)
    elif type_encoding == 2:
        b.sendxor(msg_to_encode, messageType, encode_length)

    response = b.receive(messageType)
    print(response)


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
            b.send(cmd, message_type)
            response = b.receive(message_type)
            print(response)


if __name__ == "__main__":
    main()
