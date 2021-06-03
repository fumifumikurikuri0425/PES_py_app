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


def Exy(x, y):
    Exy = 0
    Exy = 0.5 * np.exp(np.sin(x - 2) + np.cos(y)) + np.exp(np.sin(x - y) - np.cos(y)) + np.exp(np.sin(y) + 3 * np.cos(x - y)) / 14 + 2 / (np.exp(x + y - 3) + 1) + np.exp((x ** 2) / 3 + (y ** 2) / 5) / 1000
    return Exy


def Exy(x, y):
    Exy = 0
    Exy = (
        1
        + (x + y + 1) ** 2
        * (19 - 14 * x + 3 * x ** 2 - 14 * y + 6 * x * y + 3 * y ** 2)
    ) * (
        30
        + (2 * x - 3 * y) ** 2
        * (18 - 32 * x + 12 * x * x + 48 * y - 36 * x * y + 27 * y ** 2)
    )
    return Exy

def Exy(x, y):
    Exy = 0
    Exy = np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

    return Exy

def Exy(x, y):
    Exy = 0
    t1 = 20
    t2 = x**2 -10*np.cos(2*np.pi*x)
    t3 = y**2 -10*np.cos(2*np.pi*y)
    Exy = t1 + t2 + t3

    return Exy