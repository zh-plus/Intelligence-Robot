from sympy import Symbol, solve, nsolve, symbols, Eq
from math import sqrt
from functools import partial

import matplotlib.pyplot as plt

import random


def get_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def add_gaussian_noise(x):
    return x + random.gauss(0, 1)


def get_points(a, x0, y0):
    return [(x0, y0), (x0 + a, y0), (x0, y0 + a), (x0 + a, y0 + a)]


def do_hw(x, y, x0_un, y0_un, a_un):
    points = get_points(a_un, x0_un, y0_un)

    xy_distance = partial(get_distance, (x, y))
    r = [xy_distance(points[0]), xy_distance(points[1]), xy_distance(points[2]), xy_distance(points[3])]
    r = list(map(add_gaussian_noise, r))
    print(r)

    a, x0, y0 = symbols('a x0 y0')
    points = get_points(a, x0, y0)

    functions = [
        Eq(xy_distance(points[0]), r[0]),
        Eq(xy_distance(points[1]), r[1]),
        Eq(xy_distance(points[2]), r[2]),
        # Eq(xy_distance(points[3]), r[3])  # 3 equations is enough to solve this
    ]

    result = solve(functions, [a, x0, y0])
    print(result)

    # the nearest one is the solution
    solution = min(result, key=lambda x: sqrt((a_un - x[0]) ** 2 + (x0_un - x[1]) ** 2 + (y0_un - x[2]) ** 2))
    print(solution)

    solved_points = get_points(*solution)

    return solved_points


def draw(x, y, points):
    plt.scatter(x, y)

    X, Y = zip(*points)
    plt.scatter(X, Y)

    # add annotations
    plt.annotate('[x, y] = ({:.2f}, {:.2f})'.format(x, y), xy=(x, y), xytext=(x - 40, y + 8))

    for p in points:
        plt.annotate('({:.2f}, {:.2f})'.format(*p), xy=p, xytext=(p[0] + 5, p[1] + 3))

    plt.show()


if __name__ == '__main__':
    # Set parameters
    x, y = 150, 120
    x0_un, y0_un = 0, 0  # Unknown
    a_un = 200  # Unknown

    solved_points = do_hw(x, y, x0_un, y0_un, a_un)

    draw(x, y, solved_points)
