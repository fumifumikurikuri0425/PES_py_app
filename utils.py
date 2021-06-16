import sys
import numpy as np
import function_memo


def get_meshgrid_from_xyzArray(xar, yar, zar):
    # mx, my, mz : in meshgrid
    x_count = len(np.unique(xar))
    y_count = len(np.unique(yar))

    Z_list_meshed = np.reshape(zar, (x_count, y_count))
    Z_list_meshed = np.transpose(Z_list_meshed)
    return Z_list_meshed


def create_pes_data(function, xmin, xmax, ymin, ymax, resolution):
    np.set_printoptions(precision=6, floatmode="fixed", suppress=True)

    X_list = np.linspace(xmin, xmax, resolution)
    Y_list = np.linspace(ymin, ymax, resolution)
    # print(X_list)
    # print(Y_list)

    Z_list = []

    for x in X_list:
        for y in Y_list:
            MBP = Exy(x, y, function)
            Z_list.append(float(MBP))

    return X_list, Y_list, Z_list


def create_pes_data_from_code(code, xmin, xmax, ymin, ymax, resolution):
    np.set_printoptions(precision=6, floatmode="fixed", suppress=True)
    # print(code)
    a = dict()
    exec(code, globals(), a)
    # test = eval("E(4,3)")
    # print("test:", str(test))

    X_list = np.linspace(xmin, xmax, resolution)
    Y_list = np.linspace(ymin, ymax, resolution)
    # print(X_list)
    # print(Y_list)

    Z_list = []

    for x in X_list:
        for y in Y_list:
            MBP = a["E"](x, y)
            Z_list.append(float(MBP))

    return X_list, Y_list, Z_list


def Exy(x, y, function_name):
    Exy = 0
    if function_name == "mbp":
        Exy = function_memo.muller_brown_potential(x, y)
    elif function_name == "pes1":
        Exy = function_memo.pes1(x, y)
    elif function_name == "pes2":
        Exy = function_memo.pes2(x, y)
    elif function_name == "pes3":
        Exy = function_memo.pes3(x, y)
    elif function_name == "pes4":
        Exy = function_memo.pes4(x, y)
    elif function_name == "pes5":
        Exy = function_memo.pes5(x, y)

    return Exy
