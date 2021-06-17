import numpy as np


def make_graph_from_file(file):

    data_set = np.loadtxt(fname=file, dtype="float", delimiter=",")

    X_list = []
    Y_list = []
    Z_list = []

    for data in data_set:
        X_list.append(data[0])
        Y_list.append(data[1])
        Z_list.append(data[2])

    x_count = len(np.unique(X_list))
    y_count = len(np.unique(Y_list))
    z_count = len(Z_list)
    # print(x_count, y_count, z_count)

    Z_list_meshed = np.reshape(Z_list, (x_count, y_count))
    Z_list_meshed = np.transpose(Z_list_meshed)

    # print(Z_list_meshed)
    xmin = min(X_list)
    xmax = max(X_list)
    ymin = min(Y_list)
    ymax = max(Y_list)
    zmin = min(Z_list)

    return xmin, xmax, ymin, ymax, zmin, Z_list_meshed
