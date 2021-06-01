import numpy as np

import sys

from skimage import measure
from bokeh.plotting import figure, show
from bokeh import palettes
from bokeh.models import (
    ColorBar,
    FixedTicker,
    LinearColorMapper,
    PrintfTickFormatter,
    Title,
)
from bokeh.resources import CDN


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


def make_plot(color_tone, interval, xmin, xmax, ymin, ymax, zmin, zmax):

    # x,y,zの配列を生成
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

    X_list_meshed, Y_list_meshed, Z_list_meshed = get_meshgrid_from_xyzArray(
        X_list, Y_list, Z_list
    )

    p = figure(
        tooltips=[("X", "$x"), ("Y", "$y"), ("value", "@image")],
        width=700,
        height=530,
    )
    p.x_range.range_padding = p.y_range.range_padding = 0

    exp_cmap = LinearColorMapper(
        palette=palettes.inferno(color_tone), low=zmin, high=zmax
    )

    image = p.image(
        image=[Z_list_meshed],
        x=xmin,
        y=ymin,
        dw=xmax - xmin,
        dh=ymax - ymin,
        color_mapper=exp_cmap,
        level="image",
    )
    p.grid.grid_line_width = 0

    levels = np.linspace(zmin, zmax, color_tone + 1)

    color_bar = ColorBar(
        color_mapper=exp_cmap,
        major_label_text_font_size="8pt",
        ticker=FixedTicker(ticks=levels),
        formatter=PrintfTickFormatter(format="%.2f"),
        label_standoff=6,
        border_line_color=None,
        location=(0, 0),
    )

    p.add_layout(color_bar, "right")

    print(image)

    print(Z_list_meshed.shape)
    x_shape = Z_list_meshed.shape[1] - 1
    y_shape = Z_list_meshed.shape[0] - 1

    for level in levels:

        if level == levels[-1]:
            break

        contours = measure.find_contours(Z_list_meshed, level)
        for contour in contours:

            x = contour[:, 1] / x_shape * (xmax - xmin) + xmin
            y = contour[:, 0] / y_shape * (ymax - ymin) + ymin

            p.line(x, y, color="grey", line_width=1, alpha=1)

    data_set = np.loadtxt(fname="graph1.csv", dtype="float", delimiter=",")

    p_x1 = []
    p_y1 = []

    for data in data_set:
        p_x1.append(data[0])
        p_y1.append(data[1])

    p.line(p_x1, p_y1, line_width=2, color="#3949AB", alpha=0.5)

    p.circle(p_x1[-1], p_y1[-1], color="lime", line_width=4)

    data_set = np.loadtxt(fname="graph2.csv", dtype="float", delimiter=",")

    p_x2 = []
    p_y2 = []

    for data in data_set:
        p_x2.append(data[0])
        p_y2.append(data[1])

    p.line(p_x2, p_y2, line_width=2, color="cyan", alpha=0.5)

    p.add_layout(
        Title(
            text=(
                "TS:"
                + " x="
                + str(p_x1[-1])
                + " y="
                + str(p_y1[-1])
                + " Energy:"
                + " {:.6f}".format(Exy(p_x1[-1], p_y1[-1]))
            ),
            align="center",
        ),
        "below",
    )

    p.add_layout(
        Title(
            text=(
                "EQ:"
                + " x="
                + str(p_x2[-1])
                + " y="
                + str(p_y2[-1])
                + " Energy:"
                + " {:.6f}".format(Exy(p_x2[-1], p_y2[-1]))
            ),
            align="center",
        ),
        "below",
    )
    return p
