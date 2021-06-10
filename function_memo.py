from memo.test import E
import numpy as np


def calculate_energy(x, y, function):
    Exy = 0
    if function == 0:
        Exy = muller_brown_potential(x, y)
    elif function == 1:
        Exy = pes1(x, y)
    return Exy


def muller_brown_potential(x, y):
    A = [-200, -100, -170, 15]
    a = [-1, -1, -6.5, 0.7]
    b = [0, 0, 11, 0.6]
    c = [-10, -10, -6.5, 0.7]
    X = [1, 0, -0.5, -1]
    Y = [0, 0.5, 1.5, 1]

    Exy = 0
    for i in range(4):
        Exy += A[i] * np.exp(
            a[i] * ((x - X[i]) ** 2)
            + b[i] * (x - X[i]) * (y - Y[i])
            + c[i] * ((y - Y[i]) ** 2)
        )
    return Exy


def pes1(x, y):
    Exy = 0
    t1 = 0.5 * np.exp(np.sin(x - 2) + np.cos(y))
    t2 = np.exp(np.sin(x - y) - np.cos(y))
    t3 = np.exp(np.sin(y) + 3 * np.cos(x - y)) / 14
    t4 = 2 / (np.exp(x + y - 3) + 1)
    t5 = np.exp((x ** 2) / 3 + (y ** 2) / 5) / 1000
    Exy = t1 + t2 + t3 + t4 + t5
    return Exy


def pes2(x, y):
    Exy = 0
    t1 = 20
    t2 = x ** 2 - 10 * np.cos(2 * np.pi * x)
    t3 = y ** 2 - 10 * np.cos(2 * np.pi * y)
    Exy = t1 + t2 + t3

    return Exy


def pes3(x, y):
    Exy = 0
    Exy = np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

    return Exy


def pes4(x, y):
    Exy = 0
    Exy = np.sin(x) * np.cos(y)
    return Exy


def pes5(x, y):
    Exy = 0
    Exy = -np.sum(x * np.sin(np.sqrt(np.abs(x))) + y * np.sin(np.sqrt(np.abs(y))))
    return Exy
