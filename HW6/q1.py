from math import *
from scipy.integrate import quad
from functools import partial

import numpy as np
import matplotlib.pyplot as plt

SAMPLES = int(1e4)
MAX_DIS = 500
print('Using sample times: {:e}'.format(SAMPLES))

z_exp = 250
lamda = 0.01
sigma = 25
z_small = 10


def gaussian(z, sigma=sigma):
    return np.exp(-np.power(z - z_exp, 2.) / (2 * np.power(sigma, 2.))) / (np.sqrt(2 * pi) * sigma)


def exp_fn(z, lamda=lamda):
    return lamda * exp(-lamda * z)


def get_mu(f):
    mu, error = quad(f, 0, MAX_DIS)
    return 1 / mu


def hit():
    mu = get_mu(gaussian)

    return lambda z: mu * gaussian(z)


def unexp():
    mu = get_mu(exp_fn)

    return lambda z: mu * exp_fn(z)


def rand():
    return lambda z: 1 / MAX_DIS


def max_range():
    return lambda z: 1 / z_small if abs(z - MAX_DIS) < z_small else 0


def draw(f):
    X = np.linspace(0, MAX_DIS, SAMPLES)

    Y = list(map(f, X))

    plt.plot(X, Y)
    plt.xlabel('z')
    plt.ylabel('p')
    plt.show()


def do_hw(alphas):
    p_hit = hit()
    p_unexp = unexp()
    p_rand = rand()
    p_max_range = max_range()

    # draw(p_hit)
    # draw(p_unexp)
    # draw(p_rand)
    # draw(p_max_range)

    f = lambda z: np.array(alphas).T @ [p_hit(z), p_unexp(z), p_rand(z), p_max_range(z)]
    draw(f)


if __name__ == "__main__":
    alphas = [0.4, 0.3, 0.2, 0.1]
    do_hw(alphas)
