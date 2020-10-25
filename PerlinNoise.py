from MathematicalFunctions import gaussian_vector
from itertools import product
from MapRendering import MapGenerator
from PIL import Image


class PerlinNoise(object):
    def __init__(self, dimension):
        self.gradient_points = {}
        self.dimension = dimension
        self.scale_factor = 2 * dimension ** -0.5

    @staticmethod
    def dot_product(a, b):
        result = 0
        for i in range(0, len(a)):
            result += a[i]*b[i]
        return result

    @staticmethod
    def fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    @staticmethod
    def lerp(a, b, t):
        return a + t * (b - a)

    def generate_noise_point(self, point):
        grid_points = []
        dimension = len(point)
        for coordinate in point:
            min_coordinate = int(coordinate//1)
            max_coordinate = min_coordinate+1
            grid_points.append((min_coordinate, max_coordinate))
        dots = []
        for grid_point in product(*grid_points):
            if grid_point not in self.gradient_points:
                self.gradient_points[grid_point] = gaussian_vector(dimension)
            position = [point[i] - grid_point[i] for i in range(0, dimension)]
            gradient = self.gradient_points[grid_point]
            dot_product = self.dot_product(gradient, position)
            dots.append(dot_product)
        dimension = self.dimension
        while len(dots) > 1:
            dimension -= 1
            faded_point = self.fade(point[dimension] - grid_points[dimension][0])
            interpolated_dots = []
            while dots:
                interpolation = self.lerp(faded_point, dots.pop(0), dots.pop(0))
                interpolated_dots.append(interpolation)
            dots = interpolated_dots
        return dots[0]*self.scale_factor

    def octave_perlin(self, point, octaves=1, persistence=0.5, lacunarity=2):
        total = 0
        frequency = 1
        amplitude = 1
        max_value = 0
        for _ in range(0, octaves):
            total += self.generate_noise_point([coordinate*frequency for coordinate in point]) * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= lacunarity
        total /= 2 - 2 ** (1 - octaves)
        return total / max_value


size = 256
noise = size*size*[None]
noise_generator = PerlinNoise(2)
for y in range(0, size):
    for x in range(0, size):
        noise[y*size+x] = (noise_generator.octave_perlin((x/size, y/size), 6)+1)/4
print(min(noise), max(noise))
map_generator = MapGenerator(noise)
map_data = map_generator.generate_map()
img = Image.new('RGB', (size, size))
img.putdata(noise)
img.show()
