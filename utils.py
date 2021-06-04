import sys
import numpy as np


def get_meshgrid_from_xyzArray(xar, yar, zar):
    # mx, my, mz : in meshgrid
    x_count = len(np.unique(xar))
    y_count = len(np.unique(yar))

    Z_list_meshed = np.reshape(zar, (x_count, y_count))
    Z_list_meshed = np.transpose(Z_list_meshed)
    return Z_list_meshed


def create_test_data(xmin, xmax, ymin, ymax, interval):

    np.set_printoptions(precision=6, floatmode="fixed", suppress=True)

    X_list = [i for i in np.arange(xmin, xmax + 0.01, interval)]
    Y_list = [i for i in np.arange(ymin, ymax + 0.01, interval)]
    Z_list = []

    for x in X_list:
        for y in Y_list:
            MBP = Exy(x, y)
            Z_list.append(float(MBP))

    return X_list, Y_list, Z_list


def Exy(x, y):
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
