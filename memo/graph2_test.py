import math
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
#from scipy.stats import multivariate_normal

from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import matplotlib.animation as animation

import sys

A=[-200,-100,-170,15]
a=[-1,-1,-6.5,0.7]
b=[0,0,11,0.6]
c=[-10,-10,-6.5,0.7]
X=[1,0,-0.5,-1]
Y=[0,0.5,1.5,1]

def Exy(x,y):
    Exy = 0
    for i in range(4):
        Exy += A[i]*math.exp(a[i]*((x - X[i])**2) + b[i]*(x - X[i])*(y - Y[i]) + c[i]*((y - Y[i])**2))
    return Exy
"""
data_set = np.loadtxt(
    fname="graph2.csv",
    dtype="float",
    delimiter=","
)

for data in data_set:
    plt.scatter(data[0], data[1],c='blue',s=5)
    plt.plot(data[0], data[1])

plt.show()
"""


#x,y,zの配列を生成
np.set_printoptions(precision=6, floatmode='fixed', suppress=True)

X_list = []
Y_list = []
Z_list = []

for i, x in enumerate(np.arange(-2.5, 1.51, 0.1)):
    for j, y in enumerate(np.arange(-1.0, 3.01, 0.1)):
        X_list.append(float(x))
        Y_list.append(float(y))
        MBP = Exy(x,y)
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

X_list_meshed, Y_list_meshed, Z_list_meshed = get_meshgrid_from_xyzArray(X_list, Y_list, Z_list)


# norm = plt.Normalize(vmin=-200, vmax=20)
# colors = plt.cm.jet(norm(Z_list_meshed))
# colors[np.array(Z_list_meshed) > 20] = (0, 0, 0, 0)

levels = MaxNLocator(nbins=20).tick_values(-147, 200)

fig, ax= plt.subplots()
cont = plt.contourf(X_list_meshed,Y_list_meshed,Z_list_meshed,
                    cmap='coolwarm',
                    levels=levels,

                    )
plt.colorbar()
ax.set_xlabel('X')
ax.set_ylabel('Y')

"""=================================================================
散布図の表示
=================================================================="""
data_set = np.loadtxt(
    fname="graph2.csv",
    dtype="float",
    delimiter=","
)

# for data in data_set:
#     plt.scatter(data[0], data[1],c='c',s=5,alpha=0.6)
#     #plt.plot(data[0], data[1],"o-",c="c") 

p_x = []
p_y = []

for data in data_set:
    p_x.append(data[0])
    p_y.append(data[1])
x_vol = len(p_x)
# y_vol = len(p_y)

def update(i,fig_title,alp):
    if i != 0:
        plt.cla()
    plt.plot(p_x[0:i], p_y[0:i], c='c',alpha=0.6)
    plt.title(fig_title + 'i=' + str(i))


ani = animation.FuncAnimation(fig, update,fargs = ('Initial Animation! ', 0.8), interval = 50, frames= x_vol)
ani.save("test.gif", writer = 'imagemagick')
#plt.show()
