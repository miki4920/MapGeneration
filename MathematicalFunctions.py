from random import random, gauss
from math import log, sin, pi


def gaussian_random(mean, std):
    u1 = 1-random()
    u2 = 1-random()
    return mean + std*((-2*log(u1))**0.5)*sin(2*pi*u2)


def gaussian_vector(dimension):
    vector_components = [gaussian_random(0, 1) for _ in range(dimension)]
    vector_magnitude = sum([vector_component**2 for vector_component in vector_components])**-0.5
    return [vector_component*vector_magnitude for vector_component in vector_components]
