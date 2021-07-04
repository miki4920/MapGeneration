import math
import random
from matplotlib import pyplot as plt
gradients = [random.uniform(-1, 1) for _ in range(0, 100)]


def fade(t):
    return t * t * (3. - 2. * t)


def lerp(a, b, t):
    return a + t * (b-a)


def perlin_noise_1d(p):
    p0 = math.floor(p)
    p1 = p0+1
    return lerp(gradients[p0]*(p-p0), gradients[p1]*(p-p1), fade(p-p0))



terrain = [0]*900
for i in range(0, 900):
    terrain[i] = perlin_noise_1d(i/10) + perlin_noise_1d(i/20)*2 + perlin_noise_1d(i/40)*4 + perlin_noise_1d(i/80)*8
print(terrain)
plt.plot(terrain)
plt.show()