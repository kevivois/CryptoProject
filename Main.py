import time
from threading import Thread

import Socket

b = Socket.MySocket()

b.connect("vlbelintrocrypto.hevs.ch", 6000)
lgth = b.send("quoicoõubeh !", 't')

while True:
    msg = b.receive()
    print("received " + msg)
