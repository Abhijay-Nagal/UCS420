import numpy as np

X = np.array([
    [6, 70, 3],
    [5, 50, 6],
    [8, 80, 2],
    [4, 30, 8]
])
y = np.array([40, 65, 30, 85])

# a
print(X.shape)
print(X.ndim)

# b
Xt = X.T
print(Xt)

# c
XtX = Xt @ X
print(XtX)

# d
inv_XtX = np.linalg.inv(XtX)
print(inv_XtX)

# e
beta = inv_XtX @ Xt @ y
print(beta)

# g
new_user = np.array([5, 40, 7])
pred = new_user @ beta
print(pred)
