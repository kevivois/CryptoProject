from math import sqrt

def prime( n: int):
    if n <= 1 :
        return False
    for i in range(2, int(sqrt(n)) + 1):
        if (n % i == 0):
            return False
    return True

with open('CryptoProject/prime.txt', 'w') as f:
    for x in range(100000000000):
        if prime(x):
            f.write(str(x))
            f.write('\n')
            print(x)
    f.close