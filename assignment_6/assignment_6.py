import numpy as np

# Q1
temperature = np.array([25, 28, 31, 35, 38, 27, 33, 40])
print("Q1:")
print(temperature + 2)
print((9 / 5) * temperature + 32)
print(temperature[temperature > 32])
print(np.sum(temperature > 32))

# Q2
steps = np.array([
    [5000, 6200, 7100],
    [8000, 7500, 9000],
    [4500, 5100, 4800],
    [9000, 8500, 9500]
])
print("\nQ2:")
print(np.sum(steps))
print(np.mean(steps))
print(np.max(steps), np.min(steps))
print(np.sum(steps, axis=0))
print(np.sum(steps, axis=1))
max_pos = np.argmax(steps)
print(np.unravel_index(max_pos, steps.shape))

# Q3
print("\nQ3:")
original = np.array([1, 2, 3, 4, 5, 6])
subset = original[1:5]
subset[0] = 999
print(original, subset)

copied = original[1:5].copy()
copied[0] = 500
print(original, copied)

mat = np.arange(1, 13).reshape(3, 4)
print(mat)
print(mat[0, :])
print(mat[-1, :])
print(mat[:, 1])
print(mat[1:3, 2:4])

r = mat.ravel()
f = mat.flatten()
r[0] = 777
print(mat)
f[1] = 888
print(mat)
print(mat.shape, mat.ndim, mat.size, mat.dtype)

# Q4
print("\nQ4:")
X = np.array([
    [6, 70, 3],
    [5, 50, 6],
    [8, 80, 2],
    [4, 30, 8]
])
y = np.array([40, 65, 30, 85])

print(X.shape, X.ndim)
Xt = X.T
print(Xt)
XtX = Xt @ X
print(XtX)
inv_XtX = np.linalg.inv(XtX)
print(inv_XtX)
beta = inv_XtX @ Xt @ y
print(beta)

new_user = np.array([5, 40, 7])
print(new_user @ beta)
