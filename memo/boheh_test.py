from skimage import measure
import numpy as np
from bokeh.plotting import figure, show
from bokeh import palettes
from bokeh.models import (ColorBar, FixedTicker, LinearColorMapper, PrintfTickFormatter)
from bokeh.resources import CDN
from bokeh.embed import file_html

N = 500
x = np.linspace(0, 10, N)
y = np.linspace(0, 10, N)
xx, yy = np.meshgrid(x, y)
d = np.sin(xx)*np.cos(yy)

mapper = LinearColorMapper(palette=palettes.d3['Category20'][20], low=-1, high=1)

p = figure(x_range=(0, 10), y_range=(0, 10), tooltips=[('x', '$x'), ('y', '$y'), ('value', '@image')])

# must give a vector of image data for image parameter
p.image(image=[d], x=0, y=0, dw=10, dh=10, palette=palettes.inferno(20))

levels = np.linspace(-1, 1, 12)

color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size='8pt', ticker=FixedTicker(ticks=levels),
                     formatter=PrintfTickFormatter(format='%.2f'), label_standoff=6, border_line_color=None, location=(0, 0))

p.add_layout(color_bar, 'right')

for level in levels:
    contours = measure.find_contours(d, level)
    for contour in contours:
        x = contour[:,1]/50
        y = contour[:,0]/50

        #p.line(x, y, color='grey', line_width=2)
show(p)
html = file_html(p, CDN, "MBP plot")
print(html)