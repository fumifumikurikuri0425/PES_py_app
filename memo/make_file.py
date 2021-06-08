import numpy as np

def Exy(x,y):
    Exy = 0
    Exy = 0.5 * np.exp(np.sin(x - 2) + np.cos(y)) + np.exp(np.sin(x - y) - np.cos(y)) + np.exp(np.sin(y) + 3 * np.cos(x - y)) / 14 + 2 / (np.exp(x + y - 3) + 1) + np.exp((x ** 2) / 3 + (y ** 2) / 5) / 1000
    return Exy

with open('pes1.csv','w') as f:
    X_list = [i for i in np.arange(-6.5, 6.5 + 0.01, 0.01)]
    Y_list = [i for i in np.arange(-6, 6+ 0.01, 0.01)]
    Z_list = []

    for x in X_list:
        for y in Y_list:
            MBP = Exy(x, y)
            result1 = "{:.6f},{:.6f},{:.6f}\n".format(x,y,MBP)
            f.write(result1)
    f.close