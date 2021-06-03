import sys
import numpy as np


def get_meshgrid_from_xyzArray(xar, yar, zar):
    # mx, my, mz : in meshgrid
    xuniq = np.unique(xar)
    yuniq = np.unique(yar)
    mz = np.empty([len(yuniq), len(xuniq)])
    for ix in range(len(xuniq)):
        for iy in range(len(yuniq)):
            xx, yy = xuniq[ix], yuniq[iy]
            for idx in range(len(xar)):
                tx, ty = xar[idx], yar[idx]
                if abs(tx - xx) >= sys.float_info.epsilon:
                    continue
                if abs(ty - yy) >= sys.float_info.epsilon:
                    continue
                mz[iy][ix] = zar[idx]
    mx, my = np.meshgrid(xuniq, yuniq)
    return mx, my, mz


def create_test_data(xmin, xmax, ymin, ymax, interval):
    np.set_printoptions(precision=6, floatmode="fixed", suppress=True)

    X_list = []
    Y_list = []
    Z_list = []

    for i, x in enumerate(np.arange(xmin, xmax + 0.01, interval)):
        for j, y in enumerate(np.arange(ymin, ymax + 0.01, interval)):
            X_list.append(float(x))
            Y_list.append(float(y))
            MBP = Exy(x, y)
            MBP = "{:.6f}".format(MBP)
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
