from PIL import Image
import random
from itertools import product
import math
import time


class PerlinNoise(object):
    def __init__(self, octaves=1, persistence=2.0, frequency_factor=1.0):
        self.gradients = dict.fromkeys(range(10))
        self.octaves = octaves
        self.persistence = persistence
        self.frequency_factor = frequency_factor
        self.point = []

    def __call__(self, point):
        self.point = point
        noise = 0
        scalar = 2**0.5
        for octave in range(self.octaves):
            noise += ((self.generate_noise() * scalar) / (self.persistence ** octave))
            self.point = [coordinate*self.frequency_factor*(1 << octave) for coordinate in point]
        noise /= 2 - 2 ** (1 - self.octaves)
        r = (noise + 1) / 2
        for _ in range(int(self.octaves / 2 + 0.5)):
            r = self.fade(r)
        noise = r * 2 - 1
        return noise

    @staticmethod
    def _generate_gradient():
        vectors = [random.gauss(0, 1) for _ in range(2)]
        modulus = (vectors[0] ** 2 + vectors[1] ** 2) ** (-0.5)
        vectors = [vectors[0] * modulus, vectors[1] * modulus]
        return vectors

    def generate_noise(self):
        grid_points = []
        for coord in self.point:
            min_coord = math.floor(coord)
            max_coord = min_coord + 1
            grid_points.append((min_coord, max_coord))
        dots = []
        for grid_point in product(*grid_points):
            if grid_point not in self.gradients:
                self.gradients[grid_point] = self._generate_gradient()
            gradient = self.gradients[grid_point]
            dot = self.dot_product(gradient,
                                   [self.point[0]-grid_point[0], self.point[1]-grid_point[1]])
            dots.append(dot)
        noise = self.find_average([self.point[0]-grid_points[0][0], self.point[1]-grid_points[1][0]], dots)
        return noise

    def find_average(self, point, dots):
        x = point[0]
        y = point[1]
        average_x = self.fade(x)
        average_y = self.fade(y)
        linear_one = self.linear(dots[0], dots[1], average_y)
        linear_two = self.linear(dots[2], dots[3], average_y)
        linear_final = self.linear(linear_one, linear_two, average_x)
        return linear_final

    @staticmethod
    def dot_product(a, b):
        influence = (a[0]*b[0])+(a[1]*b[1])
        return influence

    @staticmethod
    def fade(t):
        return (6 * (t ** 5)) - (15 * (t ** 4)) + (10 * (t ** 3))

    @staticmethod
    def linear(a, b, x):
        return a+x*(b-a)


class MapGenerator(object):
    def __init__(self, data):
        self.data = data
        self.length = len(self.data)
        self.bottom = min(self.data)
        self.top = max(self.data)
        self.scale = self.top-self.bottom
        self.snow = 0.99
        self.mountain = 0.95
        self.large_hill = 0.9
        self.hill = 0.8
        self.plain = 0.4
        self.beach = 0.3
        self.shallow_water = 0.2

    def __call__(self):
        self.generate_map()
        return self.data

    def generate_map(self):
        for i in range(0, self.length):
            if self.top >= self.data[i] > self.bottom+(self.scale*self.snow):
                self.data[i] = (240, 240, 236)
            elif self.top >= self.data[i] > self.bottom+(self.scale*self.mountain):
                self.data[i] = (134, 126, 112)
            elif self.bottom+(self.scale*self.mountain) > self.data[i] > self.bottom+(self.scale*self.large_hill):
                self.data[i] = (151, 124, 83)
            elif self.bottom+(self.scale*self.large_hill) > self.data[i] > self.bottom+(self.scale*self.hill):
                self.data[i] = (222, 165, 33)
            elif self.bottom+(self.scale*self.hill) > self.data[i] > self.bottom+(self.scale*self.plain):
                self.data[i] = (124, 252, 0)
            elif self.bottom+(self.scale*self.plain) > self.data[i] > self.bottom+(self.scale*self.beach):
                self.data[i] = (253, 223, 119)
            elif self.bottom+(self.scale*self.beach) > self.data[i] > self.bottom+(self.scale*self.shallow_water):
                self.data[i] = (144, 152, 204)
            elif self.bottom <= self.data[i] <= self.bottom+(self.scale*self.shallow_water):
                self.data[i] = (0, 0, 89)


size = 256
values = [(x/size, y/size) for x in range(0, size) for y in range(0, size)]
noise_generator = PerlinNoise(6, persistence=1.4, frequency_factor=1.6)
noise_values = list(map(noise_generator, values))
map_generator = MapGenerator(noise_values)
map_values = map_generator()
image = Image.new("RGB", (size, size))
image.putdata(map_values, 128, 128)
image.save("map.png")
