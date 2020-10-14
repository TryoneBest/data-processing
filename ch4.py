import random
import numpy as np
import matplotlib.pyplot as plt

# 纯Python方式实现1000步的随机漫步
position = 0
walk = [position]
steps = 1000
for i in range(steps):
    step = 1 if random.randint(0, 1) else -1
    position += step
    walk.append(position)


nsteps = 1000
draws = np.random.randint(0, 2, size=nsteps)
steps = np.where(draws > 0, 1, -1)
walk = steps.cumsum()
print(walk.min(), walk.max())
print((np.abs(walk) >= 10).argmax())

# 5000
nwalks = 5000
nsteps = 1000
draws = np.random.randint(0, 2, size=(nwalks, nsteps)) # 0 or 1
steps = np.where(draws > 0, 1, -1)
walks = steps.cumsum(1)
print(walks, walks.max(), walks.min())
hits30 = (np.abs(walks) >= 30).any(1)
print(hits30)
print(hits30.sum()) # 到达30或-30的数量
crossing_times = (np.abs(walks[hits30]) >= 30).argmax(1)
print(crossing_times.mean())
