from Socket import MySocket

def get_user_input(prompt):
    return input(prompt).strip()

def encode_message(b, cmd, messageType):
    encode = cmd.split(" ")[0]

def task_method(b, cmd, messageType):
    code = cmd.split(" ")[1]
    #récup des données
    b.send(cmd, messageType)
    msg = b.receive("s")
    print("> " + msg)
    key = msg.split(" ")[-1]
    msg_to_encode = b.receive(messageType)
    print("> " + msg_to_encode)
    if code == "shift" : 
        key = int(key) 
        b.sendshift(msg_to_encode, messageType, key)
    elif code == "vigenere" : 
        b.send_vigenere(msg_to_encode, messageType, key)
    elif code == "RSA" : 
        n = msg.split("=")[1].split(",")[0]
        e = msg.split("=")[-1]
        b.send_better_RSA(msg_to_encode, messageType, n, e)
        
    else :
        key = int(key)
        b.sendxor(msg_to_encode, messageType, key)
    print("> " + b.receive(messageType))
    b.send_RSA(msg_to_encode, messageType, n, e)
    print("> " + b.receive(messageType))
        


def main():
    b = MySocket()
    b.connect("vlbelintrocrypto.hevs.ch", 6000)

    while True:
        cmd = get_user_input("Write your command ['task'] 'shift'|'vigenere'|'xor' message:")

        if cmd.split(" ")[0] == "task" : 
            message_type = "s"
            task_method(b, cmd, message_type)
        else :
            encode_message_flag = cmd.split(" ")[0] == "shift" or "vigenere" or "xor"
            if encode_message_flag:
                encode_message(b, cmd, message_type)
            else:
                b.send(cmd, message_type)
                response = b.receive(message_type)
                print("<" + response)



if __name__ == "__main__":
    main()
