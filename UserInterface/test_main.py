import time

import Socket


def main():
    sck = Socket.MySocket()
    # sck.connect("vlbelintrocrypto.hevs.ch", 6000)

    while True:
        before = 1000000000000000000000000000000000000000000000
        before = sck.linear_congruential_generator(before)
        print("random generated = " + str(before))
        time.sleep(2)


if __name__ == "__main__":
    main()
