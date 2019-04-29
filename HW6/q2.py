from math import *
from scipy.integrate import dblquad
from functools import partial
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt
import sys

info = sys.version_info
if float('{}.{}'.format(info[0], info[1])) < 3.7:
    import warnings
    warnings.warn('this code is written by python 3.7, scipy 1.1.0')

SAMPLES = int(1e3)
MAX_DIS = 100
print('Using sample times: {:e}'.format(SAMPLES))

s_index = [20, 40, 55, 70]
square = [(x, y) for x in np.linspace(s_index[0], s_index[1], 4) for y in np.linspace(s_index[2], s_index[3], 4)]
p1 = (42, 30)
p2 = (55, 40)
p_start = (50, 20)
p_end = [50, 80]


def gaussian_2d(x, y, mean, sigma=1):
    m_x, m_y = mean
    return np.exp(-((x - m_x) ** 2 + (y - m_y) ** 2) / (2 * sigma ** 2)) / (2 * pi * sigma ** 2)


def get_mu(f):
    mu, error = dblquad(f, 0, MAX_DIS, 0, MAX_DIS)
    return 1 / mu


def hit(obstacle, sigma):
    f = partial(gaussian_2d, mean=obstacle, sigma=sigma)
    mu = get_mu(f)

    return lambda x, y: mu * f(x, y)


def draw1(f):
    x = np.linspace(0, MAX_DIS, SAMPLES)
    y = np.linspace(0, MAX_DIS, SAMPLES)
    X, Y = np.meshgrid(x, y)
    Y = Y[::-1]  # change y direction
    Z = np.array(list(map(f, X, Y)))

    fig = plt.figure()
    plt.imshow(Z, extent=[0, MAX_DIS, 0, MAX_DIS])

    # draw points
    p_X, p_Y = zip(p1, p2)
    plt.scatter(p_X, p_Y, color='r')

    # draw square
    pca = plt.gca()
    rect = plt.Rectangle((s_index[0], s_index[2]), 20, 15, linewidth=2, edgecolor='r', facecolor='none')
    pca.add_patch(rect)

    # draw start point and line
    plt.scatter(*p_start, color='r')
    line = plt.Line2D(*zip(p_start, p_end), color='w', linestyle='--')
    pca.add_line(line)

    # add axis label
    plt.xlabel('x')
    plt.ylabel('y')

    plt.show()


def draw2(f):
    line_samples = 1000
    x = np.full(line_samples, 50)
    y = np.linspace(p_start[1], p_end[1], line_samples)
    Z = np.array(list(map(f, x, y)))

    fig = plt.figure()
    plt.plot(y, Z)

    plt.xlabel('x')
    plt.ylabel('y')

    plt.show()


def do_hw(alphas):
    p1_hit = hit(p1, 4)
    p2_hit = hit(p2, 4)
    square_hit_fns = [hit(p, 4) for p in square]
    square_hit = lambda x, y: sum([f(x, y) for f in square_hit_fns]) / len(square_hit_fns) * 5

    f = lambda x, y: np.array(alphas).T @ [p1_hit(x, y), p2_hit(x, y), square_hit(x, y)]

    draw1(f)
    # draw(p_unexp)
    # draw(p_rand)
    # draw(p_max_range)

    # f = lambda z: np.array(alphas).T @ [p_hit(z), p_unexp(z), p_rand(z), p_max_range(z)]
    # draw(f)


if __name__ == "__main__":
    w = 1 / 3
    alphas = [w, w, w]
    do_hw(alphas)
