from math import *
from scipy.integrate import dblquad
from functools import partial, reduce
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt
import sys

info = sys.version_info
if float('{}.{}'.format(info[0], info[1])) < 3.7:
    import warnings
    warnings.warn('this code is written by python 3.7, scipy 1.1.0')

SAMPLES = int(1e3)
print('Using sample times: {:e}'.format(SAMPLES))

w, h = 100, 70
exp_point = [80, 35]
landmarks = [(0, 0), (50, 0), (50, 70)]


def gaussian_circle(x, y, landmark, mean_distance, sigma=1):
    distance = get_distance((x, y), landmark)
    return np.exp(-np.power(distance - mean_distance, 2.) / (2 * np.power(sigma, 2.))) / (np.sqrt(2 * pi) * sigma)


def get_distance(p1, p2):
    t = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    if type(t) not in (float, int, np.float64):
        d = np.array(list(map(sqrt, t)))
    else:
        d = sqrt(t)
    return d


def get_mu(f):
    mu, error = dblquad(f, 0, w, 0, h)
    return 1 / mu


def hit(landmark, sigma):
    mean_distance = get_distance(landmark, exp_point)
    f = partial(gaussian_circle, landmark=landmark, mean_distance=mean_distance, sigma=sigma)
    mu = get_mu(f)

    return lambda x, y: mu * f(x, y)


def draw(f):
    x = np.linspace(0, w, SAMPLES)
    y = np.linspace(0, h, SAMPLES)
    X, Y = np.meshgrid(x, y)
    Y = Y[::-1]  # change y direction
    Z = np.array(list(map(f, X, Y)))

    fig = plt.figure()
    plt.imshow(Z, extent=[0, w, 0, h])

    # draw landmarks
    p_X, p_Y = zip(*landmarks)
    plt.scatter(p_X, p_Y, color='red')

    # add axis label
    plt.xlabel('x')
    plt.ylabel('y')

    plt.show()


def do_hw():
    hit_fns = [hit(l, 4) for l in landmarks]
    hit_sum = lambda x, y: reduce(lambda a, b: a * b, [f(x, y) for f in hit_fns]) / len(hit_fns)

    draw(hit_sum)


if __name__ == "__main__":
    do_hw()
