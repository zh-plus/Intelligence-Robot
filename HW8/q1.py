from sympy import Symbol, solve, nsolve, symbols, Eq
from math import sqrt
from functools import partial

import random


# x = Symbol('x')
# print(solve(x * 3 - 6, x))

def get_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def add_gaussian_noise(x):
    return x + random.gauss(0, 1)


if __name__ == '__main__':
    x, y = 150, 120
    x0, y0 = 0, 0  # Unknown
    a = 200  # Unknown

    points = [(x0, y0), (x0 + a, y0), (x0, y0 + a), (x0 + a, y0 + a)]

    xy_distance = partial(get_distance, (x, y))
    r = [xy_distance(points[0]), xy_distance(points[1]), xy_distance(points[2]), xy_distance(points[3])]
    r = list(map(add_gaussian_noise, r))
    print(r)

    a, x0, y0 = symbols('a x0 y0')
    points = [(x0, y0), (x0 + a, y0), (x0, y0 + a), (x0 + a, y0 + a)]

    functions = [
        Eq(xy_distance(points[0]), r[0]),
        Eq(xy_distance(points[1]), r[1]),
        Eq(xy_distance(points[2]) + xy_distance(points[3]), r[2] + r[3]),
        # Eq(xy_distance(points[3]), r[3])
    ]

    result = solve(functions, [a, x0, y0])
    print(result)


