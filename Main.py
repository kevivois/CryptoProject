import Socket

b = Socket.MySocket()

b.connect("vlbelintrocrypto.hevs.ch", 6000)
msg = "hello"
lgth = b.send(msg,"t")

b.receive(lgth)




