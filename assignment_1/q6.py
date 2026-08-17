print("6.1")

def AddOdd(n):
    s = 0

    for i in range(1, n + 1):
        if i % 2 != 0:
            s = s + i

    return s


n = int(input("Enter n: "))

print(AddOdd(n))


print("6.2")

def IsPrime(n):
    if n < 2:
        return 0

    for i in range(2, n // 2 + 1):
        if n % i == 0:
            return 0

    return 1


def AddPrime(n):
    s = 0

    for i in range(2, n + 1):
        if IsPrime(i):
            s = s + i

    return s


n = int(input("Enter n: "))

print(AddPrime(n))