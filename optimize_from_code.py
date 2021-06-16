import numpy as np


def calculate_distance(x, y):
    distance = 0
    distance = np.sqrt(x ** 2 + y ** 2)
    return distance


def make_data_from_code(code, first_x, first_y, check, step):

    a = dict()
    exec(code, globals(), a)

    def Exy(x, y):
        Exy = a["E"](x, y)
        return Exy

    # 1階微分
    h = 1e-7

    def fx(x, y):
        result = (Exy(x + h, y) - Exy(x - h, y)) / (2 * h)
        return result

    def fy(x, y):
        result = (Exy(x, y + h) - Exy(x, y - h)) / (2 * h)
        return result

    # 2階微分
    def fxx(x, y):
        result = (fx(x + h, y) - fx(x - h, y)) / (2 * h)
        return result

    def fyy(x, y):
        result = (fy(x, y + h) - fy(x, y - h)) / (2 * h)
        return result

    def fxy(x, y):
        result = (fx(x, y + h) - fx(x, y - h)) / (2 * h)
        return result

    def fyx(x, y):
        result = (fy(x + h, y) - fy(x - h, y)) / (2 * h)
        return result

    # へシアン*一次微分
    def hessian_x(x, y):
        denominator = fxx(x, y) * fyy(x, y) - fxy(x, y) * fyx(x, y)
        if denominator == 0:
            denominator = 1e-7
        result = (fyy(x, y) * fx(x, y) - fxy(x, y) * fy(x, y)) / denominator
        return result

    def hessian_y(x, y):
        denominator = fxx(x, y) * fyy(x, y) - fxy(x, y) * fyx(x, y)
        if denominator == 0:
            denominator = 1e-7
        result = (-fxy(x, y) * fx(x, y) + fxx(x, y) * fy(x, y)) / denominator
        return result

    x = first_x
    y = first_y
    fx_tmp = 1
    fy_tmp = 1
    step = step

    X1_list = []
    Y1_list = []
    X2_list = []
    Y2_list = []
    Energy_list = []
    Distance_list = []
    distance = 0
    x_before = 0
    y_before = 0
    x_after = 0
    y_after = 0
    count = 0

    # Newton法で鞍点まで行く

    while fx_tmp > 1e-5 and fy_tmp > 1e-5:
        X1_list.append(x)
        Y1_list.append(y)
        Exy_tmp = Exy(x, y)

        if count != 1:
            distance += calculate_distance(x_after - x_before, y_after - y_before)
            Distance_list.append(distance)
            Energy_list.append(Exy(x, y))

        hessian_x_tmp = hessian_x(x, y)
        hessian_y_tmp = hessian_y(x, y)
        x = x - step * hessian_x_tmp
        y = y - step * hessian_y_tmp
        x_before = x_after
        y_before = y_after
        x_after = x
        y_after = y
        fx_tmp = abs(fx(x, y))
        fy_tmp = abs(fy(x, y))
        count += 1

    X2_list.append(x)
    Y2_list.append(y)
    distance += calculate_distance(x_after - x_before, y_after - y_before)
    Distance_list.append(distance)
    Energy_list.append(Exy(x, y))
    TS_point = [distance, Exy(x, y)]

    # 固有値,固有ベクトルを求めたい
    # ヤコビ法のθを求める
    def theta(x, y):
        result = 0.5 / (np.tan(2 * fxy(x, y) / (fxx(x, y) - fyy(x, y))))
        return result

    # 固有値
    def Eigenvalue_x(x, y, theta):
        result = (
            fxx(x, y) * (np.cos(np.radians(theta))) ** 2
            + fyy(x, y) * (np.sin(np.radians(theta))) ** 2
            + fxy(x, y) * (np.sin(2 * np.radians(theta)))
        )
        return result

    def Eigenvalue_y(x, y, theta):
        result = (
            fxx(x, y) * (np.sin(np.radians(theta))) ** 2
            + fyy(x, y) * (np.cos(np.radians(theta))) ** 2
            - fxy(x, y) * (np.sin(2 * np.radians(theta)))
        )
        return result

    # 虚振動の方向に1回降りる
    z = theta(x, y)

    omega1 = Eigenvalue_x(x, y, z)
    omega2 = Eigenvalue_y(x, y, z)
    step = 0.1
    x_before = x
    y_before = y
    # saddleで落ちる方向の条件分岐
    if check == 0:
        if omega1 < 0:
            x = x - step * np.cos(np.radians(z)) / np.sqrt(
                (np.cos(np.radians(z))) ** 2 + (np.sin(np.radians(z))) ** 2
            )
            y = y - step * np.sin(np.radians(z)) / np.sqrt(
                (np.cos(np.radians(z))) ** 2 + (np.sin(np.radians(z))) ** 2
            )

        if omega2 < 0:
            x = x - step * np.sin(np.radians(z)) / np.sqrt(
                (np.cos(np.radians(z))) ** 2 + (np.sin(np.radians(z))) ** 2
            )
            y = y - step * (
                -np.cos(np.radians(z))
                / np.sqrt((np.cos(np.radians(z))) ** 2 + (np.sin(np.radians(z))) ** 2)
            )

    elif check == 1:
        if omega1 < 0:
            x = x + step * np.cos(np.radians(z)) / np.sqrt(
                (np.cos(np.radians(z))) ** 2 + (np.sin(np.radians(z))) ** 2
            )
            y = y + step * np.sin(np.radians(z)) / np.sqrt(
                (np.cos(np.radians(z))) ** 2 + (np.sin(np.radians(z))) ** 2
            )

        if omega2 < 0:
            x = x + step * np.sin(np.radians(z)) / np.sqrt(
                (np.cos(np.radians(z))) ** 2 + (np.sin(np.radians(z))) ** 2
            )
            y = y + step * (
                -np.cos(np.radians(z))
                / np.sqrt((np.cos(np.radians(z))) ** 2 + (np.sin(np.radians(z))) ** 2)
            )
    count += 1
    X2_list.append(x)
    Y2_list.append(y)
    x_after = x
    y_after = y
    distance += calculate_distance(x_after - x_before, y_after - y_before)
    Distance_list.append(distance)
    Energy_list.append(Exy(x, y))

    checkdx = 1
    checkdy = 1
    Eb = 10
    while checkdx > 1.0e-5 and checkdy > 1.0e-5:

        fx_tmp = fx(x, y)
        checkdx = abs(fx_tmp)
        # dxExy_tmpが正の時は、ｘを負の方向に、dxExy_tmpが負の時は、xを正の方向に動かす
        x = x - step * fx_tmp / np.sqrt(fx_tmp ** 2 + fy_tmp ** 2)

        fy_tmp = fy(x, y)
        checkdy = abs(fy_tmp)
        y = y - step * fy_tmp / np.sqrt(fx_tmp ** 2 + fy_tmp ** 2)
        Exy_tmp = Exy(x, y)
        Ea = Eb
        Eb = Exy_tmp
        dE = Eb - Ea
        if dE > 0:
            step /= 10
        count += 1
        x_before = x_after
        y_before = y_after
        x_after = x
        y_after = y
        X2_list.append(x)
        Y2_list.append(y)
        distance += calculate_distance(x_after - x_before, y_after - y_before)
        Distance_list.append(distance)
        Energy_list.append(Exy(x, y))

    TS = Exy(X1_list[-1], Y1_list[-1])
    EQ = Exy(X2_list[-1], Y2_list[-1])

    return (
        X1_list,
        Y1_list,
        X2_list,
        Y2_list,
        TS,
        EQ,
        count,
        Distance_list,
        Energy_list,
        TS_point,
    )
