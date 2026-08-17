print("4.1")

for i in range(1, 11):
    print(7, "*", i, "=", 7 * i)

for i in range(1, 11):
    print(9, "*", i, "=", 9 * i)


print("4.2")

n = int(input("Enter a number: "))

for i in range(1, 11):
    print(n, "*", i, "=", n * i)


print("4.3")

n = int(input("Enter n: "))

s = 0

for i in range(1, n + 1):
    s = s + i

print(s)