import numpy as np

abhijay = np.linspace(10, 100, 25)
print(abhijay)

print(abhijay.ndim)
print(abhijay.shape)
print(abhijay.size)
print(abhijay.dtype)
print(abhijay.nbytes)

transposed = abhijay.reshape(-1, 1)
print(transposed)

print(abhijay.T)
print(abhijay.T.shape)
