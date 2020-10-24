from MathematicalFunctions import gaussian_vector
from itertools import product


class PerlinNoise(object):
    def __init__(self):
        self.gradient_points = {}

    @staticmethod
    def dot_product(a, b):
        result = 0
        for i in range(0, len(a)):
            result += a[i]*b[i]
        return result

    @staticmethod
    def fade(t):
        return (6 * (t ** 5)) - (15 * (t ** 4)) + (10 * (t ** 3))

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
        for current_dimension in range(0, dimension):
            faded_point = point[current_dimension]-grid_points[current_dimension][0]
            interpolated_dots = []
            for i in range(0, len(dots)-1, 2):
                interpolation = self.lerp(dots[i], dots[i+1], faded_point)
                interpolated_dots.append(interpolation)
            dots = interpolated_dots
        return (dots[0]+1)/2

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
        return total/max_value
