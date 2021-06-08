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

from bokeh.resources import CDN

def make_graph_from_file(file,zmax):

    data_set = np.loadtxt(fname=file, dtype="float", delimiter=",")

    X_list=[]
    Y_list=[]
    Z_list=[]

    for data in data_set:
            X_list.append(data[0])
            Y_list.append(data[1])
            Z_list.append(data[2])

    x_count = len(np.unique(X_list))
    y_count = len(np.unique(Y_list))
    z_count = len(Z_list)
    print(x_count, y_count, z_count)

    Z_list_meshed = np.reshape(Z_list, (x_count, y_count))
    Z_list_meshed = np.transpose(Z_list_meshed)

    print(Z_list_meshed)
    xmin=min(X_list)
    xmax=max(X_list)
    ymin=min(Y_list)
    ymax=max(Y_list)
    zmin=min(Z_list)


    return xmin,xmax,ymin,ymax,zmin,Z_list_meshed



    p = figure(
            tooltips=[("X", "$x"), ("Y", "$y"), ("value", "@image")],
            width=700,
            height=530,
        )
    p.x_range.range_padding = p.y_range.range_padding = 0
    #choose colors from cividis, gray, inferno, magma, viridis
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

    return p