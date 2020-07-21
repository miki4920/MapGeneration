import random
from math import floor
from PIL import Image


class PerlinNoise(object):
    def __init__(self):
        self.uniform_table = [random.uniform(-1, 1) for _ in range(256)]
        self.p = [211, 255, 2, 250, 19, 133, 166, 202, 95, 159, 155, 235, 253, 10, 225, 92, 167, 131, 52, 219, 231, 76,
                  217,
                  239, 51, 34, 206, 16, 141, 142, 20, 62, 124, 6, 103, 1, 119, 207, 79, 208, 8, 234, 68, 241, 97, 17,
                  70, 99,
                  80, 137, 221, 38, 75, 83, 129, 246, 220, 109, 118, 22, 54, 148, 188, 136, 36, 12, 15, 7, 32, 214, 247,
                  27,
                  108, 240, 236, 60, 23, 238, 105, 248, 144, 44, 244, 89, 42, 252, 64, 115, 31, 29, 222, 223, 101, 143,
                  205,
                  87, 184, 82, 200, 33, 21, 81, 66, 178, 98, 151, 180, 161, 218, 46, 156, 164, 210, 71, 233, 122, 199,
                  135,
                  229, 13, 117, 93, 96, 88, 113, 39, 4, 40, 189, 65, 249, 73, 91, 104, 63, 186, 146, 125, 69, 170, 123,
                  77,
                  145, 196, 112, 110, 47, 114, 224, 30, 100, 9, 25, 45, 173, 102, 72, 162, 147, 3, 111, 232, 5, 242, 43,
                  59,
                  132, 237, 245, 35, 84, 58, 203, 24, 116, 216, 26, 230, 130, 174, 177, 169, 194, 120, 85, 121, 14, 78,
                  74,
                  154, 172, 185, 11, 86, 50, 227, 138, 150, 251, 158, 226, 191, 128, 61, 195, 49, 181, 90, 176, 106,
                  126,
                  254, 127, 183, 153, 243, 228, 192, 57, 18, 56, 140, 213, 48, 165, 139, 28, 37, 197, 41, 67, 107, 55,
                  175,
                  160, 187, 190, 182, 134, 198, 157, 163, 149, 171, 204, 0, 152, 201, 179, 215, 168, 209, 94, 193, 212,
                  53]

    def get_gradient(self, point):
        x, y = point
        gradient_x = self.p[self.p[self.p[self.p[x & 0xff] & (y & 0xff)]]]
        gradient_y = self.p[self.p[self.p[self.p[y & 0xff] & (x & 0xff)]]]
        return self.uniform_table[gradient_x], self.uniform_table[gradient_y]

    @staticmethod
    def fade(t):
        return (6 * (t ** 5)) - (15 * (t ** 4)) + (10 * (t ** 3))

    @staticmethod
    def dot(point_one, point_two):
        return point_one[0] * point_two[0] + point_one[1] * point_two[1]

    def interpolate(self, fade_value, point, points):
        gradients = list(map(self.get_gradient, points))
        p0 = (1-fade_value) * self.dot(gradients[0], (point[0]-points[0][0], point[1]-points[0][1]))
        p1 = fade_value * self.dot(gradients[1], (point[0]-points[1][0], point[1]-points[1][1]))
        return p0+p1

    @staticmethod
    def get_points(point):
        x, y = point
        points = []
        for i in range(0, 2):
            for j in range(0, 2):
                points.append((x+i, y+j))
        return points

    def generate_point(self, point):
        x, y = point
        point_floor = floor(x), floor(y)
        points = self.get_points(point_floor)
        t_0 = self.fade(x - points[0][0])
        t_1 = self.fade(y - points[0][1])
        p0p1 = self.interpolate(t_0, point, points[0:2])
        p2p3 = self.interpolate(t_0, point, points[2:])
        return ((1-t_0) * p0p1) + (t_1 * p2p3)


size = 256
values = [(x/size, y/size) for x in range(0, size) for y in range(0, size)]
noise_generator = PerlinNoise()
noise = list(map(noise_generator.generate_point, values))
image = Image.new("L", (size, size))
image.putdata(noise, 128, 128)
image.save("map.png")