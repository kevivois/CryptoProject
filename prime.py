from math import sqrt
def random(x) :
        a = 1664525
        b = 1013904223
        n = pow(2, 32)
        rand = (x*a + b)%n
        return rand
def key_rand_prime( key = 0):
    #f = open("prime.txt", "r")
    res = 0
    #numb = random(key) % 669
    for count, item in enumerate(open("prime.txt")) :
        print(count, item)
        if(count == 4) : res = item
    return res

key_rand_prime()