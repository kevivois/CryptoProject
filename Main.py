import time
from threading import Thread

import Socket

b = Socket.MySocket()

b.connect("vlbelintrocrypto.hevs.ch", 6000)
#lgth = b.sendshift("quoicoõubeh !", 't')

while True:
    cmd = input("Write your command ")
    shift = input("Do you want to encode the message ? [no|yes]")
    messageType = input("Specify your message type [t:@everyone|s:server only]")
    encodeMessage = True if "yes" in shift else False
    messageType = "t" if "t" in messageType else "s"
    if encodeMessage:
        typeEncoding = 1 if "shift" in cmd.split(" ")[1] else 2
        typeEncoding = int(typeEncoding)
        b.send(cmd,messageType)
        msg = b.receive('s')
        encodeLength = int(msg.split(" ")[-1])
        msgToEncode = b.receive('s')
        if typeEncoding == 1:
            b.sendshift(msgToEncode,messageType,encodeLength)
        elif typeEncoding == 2:
            b.sendxor(msgToEncode,messageType,encodeLength)
        response = b.receive('s')
        print(response)
    else:
        b.send(cmd,messageType)
        response = b.receive(messageType)
        print(response)
