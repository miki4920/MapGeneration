from random import random
from math import log, cos, pi


def gaussian_random(mean, std):
    u1 = 1-random()
    u2 = 1-random()
    return mean + std*((-2*log(u1))**0.5)*cos(2*pi*u2)


def gaussian_vector(dimension):
    vector_components = [gaussian_random(0, 1) for _ in range(dimension)]
    vector_magnitude = sum([vector_component*vector_component for vector_component in vector_components])**-0.5
    return tuple(vector_component*vector_magnitude for vector_component in vector_components)
