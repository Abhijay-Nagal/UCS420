import numpy as np

# a
original = np.array([1, 2, 3, 4, 5, 6])

# b
subset = original[1:5]

# c
subset[0] = 999
print(original)
print(subset)

# d
copied = original[1:5].copy()
copied[0] = 500
print(original)
print(copied)

# e
mat = np.arange(1, 13).reshape(3, 4)
print(mat)

# f
print(mat[0, :])
print(mat[-1, :])
print(mat[:, 1])
print(mat[1:3, 2:4])

# g
r = mat.ravel()
f = mat.flatten()

# h
r[0] = 777
print(mat)

# i
f[1] = 888
print(mat)

# j
print(mat.shape)
print(mat.ndim)
print(mat.size)
print(mat.dtype)
