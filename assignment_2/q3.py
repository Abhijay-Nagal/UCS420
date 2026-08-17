import random

random.seed(1024170013)

numbers = [random.randint(100, 900) for _ in range(100)]

print(numbers)

odd_numbers = [x for x in numbers if x % 2 != 0]
print(odd_numbers)
print(len(odd_numbers))

even_numbers = [x for x in numbers if x % 2 == 0]
print(even_numbers)
print(len(even_numbers))


def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


prime_numbers = [x for x in numbers if is_prime(x)]

print(prime_numbers)
print(len(prime_numbers))

frequency = {}

for number in numbers:
    if number in frequency:
        frequency[number] += 1
    else:
        frequency[number] = 1

most_frequent = max(frequency, key=frequency.get)

print(most_frequent)
print(frequency[most_frequent])