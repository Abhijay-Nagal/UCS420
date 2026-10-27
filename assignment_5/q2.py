import numpy as np

arr = np.array([1, 2, 3, 6, 4, 5])
reversed_arr = arr[::-1]
print(reversed_arr)

x = np.array([1, 2, 3, 4, 5, 1, 2, 1, 1, 1])
vals, counts = np.unique(x, return_counts=True)
most_freq_x = vals[counts == max(counts)]
print(most_freq_x)
print(np.where(x == most_freq_x[0])[0])

y = np.array([1, 1, 1, 2, 3, 4, 2, 4, 3, 3])
vals, counts = np.unique(y, return_counts=True)
most_freq_y = vals[counts == max(counts)]
print(most_freq_y)
for val in most_freq_y:
    print(np.where(y == val)[0])
