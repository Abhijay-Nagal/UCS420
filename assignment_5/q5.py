import numpy as np

ucs420_abhijay = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 15, 20, 35]).reshape(3, 4)
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
