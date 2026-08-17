roll_number = 1024170013

digits = [int(digit) for digit in str(roll_number)[:8]]

A = {digit * 7 for digit in digits}
B = {digit * 9 for digit in digits}

print(A)
print(B)

print(A.union(B))

print(A.intersection(B))

print(A.difference(B))
print(B.difference(A))

print(A.symmetric_difference(B))

print(A.issubset(B))
print(B.issuperset(A))

X = int(input("Enter a value: "))

A.discard(X)

print(A)