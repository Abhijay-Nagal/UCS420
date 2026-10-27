import numpy as np

steps = np.array([
    [5000, 6200, 7100],
    [8000, 7500, 9000],
    [4500, 5100, 4800],
    [9000, 8500, 9500]
])

# a
print(np.sum(steps))

# b
print(np.mean(steps))

# c
print(np.max(steps))
print(np.min(steps))

# d
print(np.sum(steps, axis=0))

# e
print(np.sum(steps, axis=1))

# f
max_pos = np.argmax(steps)
user, day = np.unravel_index(max_pos, steps.shape)
print(user, day)
