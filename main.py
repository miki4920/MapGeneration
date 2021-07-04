import math
import random

from itertools import product
from PIL import Image


def fade(t):
    return t * t * (3. - 2. * t)


def lerp(a, b, t):
    return a + t * (b-a)


class PerlinNoise(object):
    def __init__(self, dimension):
        self.dimension = dimension
        self.gradient = {}

    def __call__(self, point, *, octaves=1, frequency=2.0, persistence=1.0):
        total = 0
        amplitude = 1
        normalise_value = 0
        for i in range(0, octaves):
            total += self.get_noise(point) * amplitude
            normalise_value += amplitude
            amplitude *= persistence
            for coordinate in range(0, self.dimension):
                point[coordinate] *= frequency
        return total/normalise_value

    def get_gradient(self):
        random_point = [random.gauss(0, 1) for _ in range(self.dimension)]
        scale = sum(n*n for n in random_point)**-0.5
        return tuple(point*scale for point in random_point)

    def get_noise(self, point):
        grid_coordinates = []
        for coordinate in point:
            minimum_coordinate = math.floor(coordinate)
            maximum_coordinate = minimum_coordinate+1
            grid_coordinates.append((minimum_coordinate, maximum_coordinate))

        dot_products = []
        for grid_point in product(*grid_coordinates):
            if grid_point not in self.gradient:
                self.gradient[grid_point] = self.get_gradient()
            gradient = self.gradient[grid_point]
            dot_product = 0
            for i in range(0, self.dimension):
                dot_product += gradient[i] * (point[i]-grid_point[i])
            dot_products.append(dot_product)

        dimension = self.dimension
        while len(dot_products) > 1:
            dimension -= 1
            interpolation = fade(point[dimension] - grid_coordinates[dimension][0])

            future_dot_products = []
            while dot_products:
                future_dot_products.append(lerp(dot_products.pop(0), dot_products.pop(0), interpolation))
            dot_products = future_dot_products
        return (dot_products[0]+1)/2


perlin_generator = PerlinNoise(2)

terrain = [0]*10000
for y in range(0, 100):
    for x in range(0, 100):
        terrain[y*100+x] = int(perlin_generator([x/100, y/100], octaves=6, persistence=1.3, frequency=1.7)*255)

image = Image.new("L", (100, 100))
image.putdata(terrain)
image.save("terrain.png")