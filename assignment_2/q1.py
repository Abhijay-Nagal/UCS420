roll_number = 1024170013

digits = [int(digit) for digit in str(roll_number)]
L = [digit * 10 for digit in digits]

print(L)

L.append(100)
print(L)

L.insert(2, 50)
print(L)

L.remove(100)
print(L)

L.pop(2)
print(L)

L.sort()
print(L)

L.sort(reverse=True)
print(L)

print(L[:3])
print(L[-3:])

average = sum(L) / len(L)
new_list = [x for x in L if x > average]

print(new_list)