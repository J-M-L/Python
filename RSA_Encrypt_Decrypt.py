import random

_mrpt_num_trials = 5  # number of bases to test

# Miller-Rabin
def is_probable_prime(n):
    assert n >= 2
    # special case 2
    if n == 2:
        return True
    # ensure n is odd
    if n % 2 == 0:
        return False
    # write n-1 as 2**s * d
    # repeatedly try to divide n-1 by 2
    s = 0
    d = n - 1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert (2 ** s * d == n - 1)

    # test the base a to see whether it is a witness for the compositeness of n
    def try_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True  # n is definitely composite

    for i in range(_mrpt_num_trials):
        a = random.randrange(2, n)
        if try_composite(a):
            return False

    return True  # no base tested showed n as composite

#Return one prime number, 8 bytes long
def getPrimeNumber():
    while 1:
        num = random.getrandbits(64)

        if is_probable_prime(num):
            return num

#Greatest common divisor
def greatest_common_divisor(a, b):
    while b != 0:
        a, b = b, a % b
    return a

#Extended Greatest common divisor
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

#Modular inverse
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

def main():
    #Public e
    e = 65537

    #Get p that doesn't have Common Divisor with e
    p = getPrimeNumber()
    #GCD fix to p
    while 1:
        p_e_GCD = greatest_common_divisor(p-1, e)
        if p_e_GCD != 1:
            p = getPrimeNumber()
        else:
            break

    # Get q that doesn't have Common Divisor with e
    q = getPrimeNumber()
    # GCD fix to q
    while 1:
        q_e_GCD = greatest_common_divisor(q-1, e)
        if q_e_GCD != 1:
            q = getPrimeNumber()
        else:
            break


    # Public key N
    N = p* q


    # Private key d
    phi = (p-1) * (q-1)
    d = modinv(e, phi)

    #Print everything
    print("p = ", p)
    print("q = ", q)
    print("N = ", N)
    print("D = ", d)
    print()

    #Test the keys
    #Get random 120bit string and print it
    k = random.getrandbits(120)

    print("K = ", k)

    #Encrypt it with public e and N, print the result
    k2 = pow(k,e, N)

    print()
    print("K encrypted = ", k2)

    #Decrypt k2 with private key and print it.
    k3 = pow(k2,d,N)

    print("K decrypted = ", k3)

    print()

    #check the result
    if k3 == k:
        print("Encryption & Decryption successful")


main()

