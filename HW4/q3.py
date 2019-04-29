import numpy as np
import matplotlib.pyplot as plt

from math import pi
from random import gauss

SAMPLE_TIME = 500


def sample_motion_model_velocity(u, origin_state, alpha, trans):
    x, y, theta = origin_state

    new_v = u[0] + gauss(0, alpha[0] * abs(x) + alpha[1] * abs(u[1]))
    new_w = u[1] + gauss(0, alpha[2] * abs(x) + alpha[3] * abs(u[1]))
    new_g = gauss(0, alpha[4] * abs(x) + alpha[5] * abs(u[1]))

    new_x = x - new_v / new_w * np.sin(theta) + new_v / new_w * np.sin(theta + new_w + trans)
    new_y = y - new_v / new_w * np.cos(theta) + new_v / new_w * np.cos(theta + new_w + trans)
    new_t = theta + new_w * trans + new_g * trans

    # origin_state[2] = new_t

    return [new_x, new_y, new_t]


def draw(u, origin_state, a, d):
    samples = [sample_motion_model_velocity(u, origin_state, a, d) for _ in range(SAMPLE_TIME)]
    X, Y, _ = zip(*samples)
    plt.scatter(0, -1.5)
    plt.scatter(0, 0)
    plt.scatter(X, Y)
    plt.show()


if __name__ == '__main__':
    u = [15, 15]
    origin_state = [3, 2, 2 * pi]

    alpha1 = [0.03, 0.03, 0.01, 0.01, 0.01, 0.01]
    alpha2 = [0.03, 0.03, 0.001, 0.001, 0.001, 0.001]
    alpha3 = [0.01, 0.01, 0.02, 0.02, 0.01, 0.01]
    draw(u, origin_state, alpha3, 0.5)
