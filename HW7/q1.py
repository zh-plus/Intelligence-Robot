import random

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


# def draw(f):
#     x = np.linspace(0, w, SAMPLES)
#     y = np.linspace(0, h, SAMPLES)
#     X, Y = np.meshgrid(x, y)
#     Y = Y[::-1]  # change y direction
#     Z = np.array(list(map(f, X, Y)))
#
#     fig = plt.figure()
#     plt.imshow(Z, extent=[0, w, 0, h])
#
#     # draw landmarks
#     p_X, p_Y = zip(*landmarks)
#     plt.scatter(p_X, p_Y, color='red')
#
#     # add axis label
#     plt.xlabel('x')
#     plt.ylabel('y')
#
#     plt.show()


def draw_object(position, orientation=0, radius=4):
    fig = plt.gcf()
    ax = fig.gca()
    circle_landmark = plt.Circle(position, radius, color='r', fill=False, clip_on=False)
    dst = [position[0] + cos(orientation) * radius, position[1] + sin(orientation) * radius]

    X, Y = zip(position, dst)
    plt.plot(X, Y, color='r', linewidth=8)

    ax.add_artist(circle_landmark)


def first_sample(f):
    X = np.linspace(0, 100, 200)
    Y = np.linspace(0, 70, 200)
    points = np.array([(a, b) for a in X for b in Y])

    points_weight = np.array(list(map(lambda x: f(*x), points))).flatten()
    points_weight = points_weight / points_weight.sum()

    indices = np.arange(len(points))
    sampled_indices = np.random.choice(indices, size=len(points) // 100, p=points_weight)

    sampled_points = points[sampled_indices]

    return sampled_points


def second_sample(points, f):
    points_weight = np.array(list(map(lambda x: f(*x), points))).flatten()
    points_weight = points_weight / points_weight.sum()

    indices = np.arange(len(points))
    sampled_indices = np.random.choice(indices, size=len(points) // 10, p=points_weight)

    sampled_points = points[sampled_indices]

    return sampled_points


def draw(points):
    X, Y = zip(*points)
    plt.scatter(X, Y, s=5)

    fig = plt.gcf()
    ax = fig.gca()

    # draw landmark
    for l in landmarks:
        circle_landmark = plt.Circle(l, 2, color='r', fill=True, clip_on=False)
        ax.add_artist(circle_landmark)

    # draw object
    draw_object(exp_point)

    # draw circle
    for l in landmarks:
        circle_ring = plt.Circle(l, get_distance(exp_point, l), color='r', fill=False)
        ax.add_artist(circle_ring)

    # add axis label
    plt.xlabel('x')
    plt.ylabel('y')

    # change figure size
    plt.xlim(0, 100)
    plt.ylim(0, 70)

    plt.show()


def do_hw():
    f1 = hit(landmarks[0], 4)
    p1 = first_sample(f1)
    draw(p1)

    hit_fns = [hit(l, 4) for l in landmarks]
    f2 = lambda x, y: reduce(lambda a, b: a * b, [f(x, y) for f in hit_fns[1:]]) / len(hit_fns)
    p2 = second_sample(p1, f2)
    draw(p2)


if __name__ == "__main__":
    do_hw()
