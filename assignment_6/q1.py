import numpy as np

temperature = np.array([25, 28, 31, 35, 38, 27, 33, 40])

# a
temp_adjusted = temperature + 2
print(temp_adjusted)

# b
fahrenheit = (9 / 5) * temperature + 32
print(fahrenheit)

# c
greater_than_32 = temperature[temperature > 32]
print(greater_than_32)

# d
count = np.sum(temperature > 32)
print(count)
