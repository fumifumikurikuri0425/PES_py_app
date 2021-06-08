import numpy as np

import sys

from skimage import measure
from bokeh.plotting import figure, show
from bokeh import palettes
from bokeh.models import (
    ColorBar,
    FixedTicker,
    LinearColorMapper,
    EqHistColorMapper,
    LogColorMapper,
    PrintfTickFormatter,
    Title,
)
import function_memo
from optimize_line import make_data
from bokeh.resources import CDN


def Exy(x, y):
    Exy = function_memo.muller_brown_potential(x, y)
    return Exy


def make_plot(color_tone, interval, xmin, xmax, ymin, ymax, zmin, zmax, judge):

    np.set_printoptions(precision=6, floatmode="fixed", suppress=True)

    X_list = [i for i in np.arange(xmin, xmax + 0.01, interval)]
    Y_list = [i for i in np.arange(ymin, ymax + 0.01, interval)]
    Z_list = []

    for x in X_list:
        for y in Y_list:
            MBP = Exy(x, y)
            Z_list.append(float(MBP))
    print("calculate1 finished!")

    x_count = len(np.unique(X_list))
    y_count = len(np.unique(Y_list))

    Z_list_meshed = np.reshape(Z_list, (x_count, y_count))
    Z_list_meshed = np.transpose(Z_list_meshed)
    print("calculate2 finished!")

    p = figure(
        tooltips=[("X", "$x"), ("Y", "$y"), ("value", "@image")],
        width=700,
        height=530,
    )
    p.x_range.range_padding = p.y_range.range_padding = 0
    # choose colors from cividis, gray, inferno, magma, viridis
    exp_cmap = LinearColorMapper(
        palette=palettes.inferno(color_tone), low=zmin, high=zmax
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


# def get_contour_line(Z_list_meshed, zmin, zmax, color_tone):
#     levels = np.linspace(zmin, zmax, color_tone + 1)
#     x_shape = Z_list_meshed.shape[1] - 1
#     y_shape = Z_list_meshed.shape[0] - 1

#     contours_list = []

#     for level in levels:

#         if level == levels[-1]:
#             break

#         contours = measure.find_contours(Z_list_meshed, level)
#         contours_list.append(contours)

#     return contours_list


def get_contour_line(Z_list_meshed, xmin, xmax, ymin, ymax, zmin, zmax, color_tone):
    levels = np.linspace(zmin, zmax, color_tone + 1)
    x_shape = Z_list_meshed.shape[1] - 1
    y_shape = Z_list_meshed.shape[0] - 1

    contours_list = []

    for level in levels:

        if level == levels[-1]:
            break

        contours = measure.find_contours(Z_list_meshed, level)
        c_list = []
        for contour in contours:
            x = contour[:, 1] / x_shape * (xmax - xmin) + xmin
            y = contour[:, 0] / y_shape * (ymax - ymin) + ymin
            d = {"x_list": x.tolist(), "y_list": y.tolist()}
            c_list.append(d)

        contours_list.append(c_list)

    return contours_list
