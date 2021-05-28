import math

import numpy as np

import sys

from skimage import measure
from bokeh.plotting import figure, show
from bokeh import palettes
from bokeh.models import ColorBar, FixedTicker, LinearColorMapper, PrintfTickFormatter
from bokeh.resources import CDN


A = [-200, -100, -170, 15]
a = [-1, -1, -6.5, 0.7]
b = [0, 0, 11, 0.6]
c = [-10, -10, -6.5, 0.7]
X = [1, 0, -0.5, -1]
Y = [0, 0.5, 1.5, 1]


def Exy(x, y):
    Exy = 0
    for i in range(4):
        Exy += A[i] * math.exp(
            a[i] * ((x - X[i]) ** 2)
            + b[i] * (x - X[i]) * (y - Y[i])
            + c[i] * ((y - Y[i]) ** 2)
        )
    return Exy


def make_plot(color_tone, interval, xmin, xmax, ymin, ymax):

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
        tooltips=[("X", "$x"), ("Y", "$y"), ("value", "@image")], width=700, height=500
    )
    p.x_range.range_padding = p.y_range.range_padding = 0

    exp_cmap = LinearColorMapper(
        palette=palettes.inferno(color_tone), low=-147, high=100
    )

    p.image(
        image=[Z_list_meshed],
        x=xmin,
        y=ymin,
        dw=xmax - xmin,
        dh=ymax - ymin,
        color_mapper=exp_cmap,
        level="image",
    )
    p.grid.grid_line_width = 0.5

    levels = np.linspace(-147, 100, color_tone)

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

    for level in levels:
        contours = measure.find_contours(Z_list_meshed, level)
        for contour in contours:

            x = contour[:, 1] / 20 + xmin
            y = contour[:, 0] / 20 + ymin
            p.line(x, y, color="grey", line_width=1, alpha=0.7)

    data_set = np.loadtxt(fname="graph2.csv", dtype="float", delimiter=",")

    p_x = []
    p_y = []

    for data in data_set:
        p_x.append(data[0])
        p_y.append(data[1])
    # x_vol = len(p_x)
    # y_vol = len(p_y)

    p.line(p_x, p_y, line_width=2, color="cyan", alpha=0.5)

    return p
