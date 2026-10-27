import numpy as np

# Q1
arr = np.array([10, 20, 30, 40, 50])
print("Q1:")
print(arr + 2)
print(arr * 3)
print(arr / 2)

# Q2
arr2 = np.array([1, 2, 3, 6, 4, 5])
print("\nQ2:")
print(arr2[::-1])

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

# Q3
arr3 = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])
print("\nQ3:")
print(arr3[0, 1])
print(arr3[2, 0])

# Q4
abhijay = np.linspace(10, 100, 25)
print("\nQ4:")
print(abhijay)
print(abhijay.ndim)
print(abhijay.shape)
print(abhijay.size)
print(abhijay.dtype)
print(abhijay.nbytes)
print(abhijay.reshape(-1, 1))
print(abhijay.T)

# Q5
ucs420_abhijay = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 15, 20, 35]).reshape(3, 4)
print("\nQ5:")
print(ucs420_abhijay)
print(np.mean(ucs420_abhijay))
print(np.median(ucs420_abhijay))
print(np.max(ucs420_abhijay))
print(np.min(ucs420_abhijay))
print(np.unique(ucs420_abhijay))
reshaped_ucs420_abhijay = ucs420_abhijay.reshape(4, 3)
print(reshaped_ucs420_abhijay)
resized_ucs420_abhijay = np.resize(ucs420_abhijay, (2, 3))
print(resized_ucs420_abhijay)
