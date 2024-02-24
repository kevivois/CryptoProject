import time

import Socket

b = Socket.MySocket()

b.connect("vlbelintrocrypto.hevs.ch", 6000)
msg = "bonjour monsieur !a"
time.sleep(5)
lgth = b.send(msg,"t")

msg = b.receive(lgth)
print("received "+msg)




