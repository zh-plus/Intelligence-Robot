from math import *

import numpy as np
import matplotlib.pyplot as plt

# It's a little slow, you maybe wait for several seconds
SAMPLE_TIME = int(1e6)
print('Using sample times: {:e}'.format(SAMPLE_TIME))


def normal(x, sigma=1):
    return 1 / (sqrt(2 * pi) * sigma) * exp(- 0.5 * x ** 2 / sigma ** 2)


def triangular(x, sigma=1):
    return max(0, 1 / (sqrt(6) * sigma) - abs(x) / (6 * sigma ** 2))


def abs_fn(x):
    return abs(x)


def get_max(f, sigma=None):
    if sigma:
        return max([f(x, sigma) for x in np.arange(-5, 6, 0.1)])
    else:
        return max([f(x) for x in np.arange(-5, 6, 0.1)])


normal_max = get_max(normal, 1)
triangular_max = get_max(triangular, 1)
abs_fn_max = get_max(abs_fn)
fn_max_map = {normal: normal_max,
              triangular: triangular_max, abs_fn: abs_fn_max}


def rejection_sampling(f, x_min, x_max, iter_num=SAMPLE_TIME):
    fn_max = fn_max_map[f]

    X = np.random.uniform(x_min, x_max, iter_num)
    Y = np.random.uniform(0, fn_max, iter_num)

    samples = [sample for sample in zip(X, Y) if sample[1] <= f(sample[0])]

    return samples


def draw(samples, y_axis_max):
    X, Y = zip(*samples)
    plt.plot(X, Y, 'g.', label='Samples')
    plt.xlim([-6, 6])
    plt.ylim([0, y_axis_max])

    plt.show()


def do_hw(f, x_min, x_max, y_axis_max):
    samples = rejection_sampling(f, x_min, x_max)
    draw(samples, y_axis_max)


if __name__ == "__main__":
    do_hw(normal, -5, 5, 0.5)
    do_hw(triangular, -5, 5, 0.5)
    do_hw(abs_fn, -1, 1, 1)
