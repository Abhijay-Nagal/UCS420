print("5.1")

a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
c = int(input("Enter third number: "))

print(max(a, b, c))


print("5.2")

n = int(input("Enter n: "))

s = 0

for i in range(1, n + 1):
    if i % 7 == 0 and i % 9 == 0:
        s = s + i

print(s)


print("5.3")

n = int(input("Enter n: "))

s = 0

for i in range(2, n + 1):
    f = 0

    for j in range(2, i // 2 + 1):
        if i % j == 0:
            f = 1
            break

    if f == 0:
        s = s + i

print(s)