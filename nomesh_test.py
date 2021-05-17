import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
#from scipy.stats import multivariate_normal

from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

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

#x,y,zの配列を生成
np.set_printoptions(precision=6, floatmode='fixed', suppress=True)

X_list = []
Y_list = []
Z_list = []
step = 0.05
for i, x in enumerate(np.arange(-2.5, 1.51, step)):
        for j, y in enumerate(np.arange(-1.0, 3.01, step)):
            X_list.append(float(x))
            Y_list.append(float(y))
            MBP = Exy(x,y)
            MBP = "{:.6f}".format(MBP)
            Z_list.append(float(MBP))

#print(Z_list)

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

z_min = min(Z_list)
print(z_min)



X_list_meshed, Y_list_meshed, Z_list_meshed = get_meshgrid_from_xyzArray(X_list, Y_list, Z_list)
print(Z_list_meshed)
# with open('X_list_meshed.dat','w') as f:
#     f.write(X_list_meshed)
# f.close

# with open('Y_list_meshed.dat','w') as f:
#     f.write(Y_list_meshed)
# f.close

# with open('Z_list_meshed.dat','w') as f:
#     f.write(Z_list_meshed)
# f.close


"""
#contourfは離散的なデータに不向き
# norm = plt.Normalize(vmin=-200, vmax=20)
# colors = plt.cm.jet(norm(Z_list_meshed))
# colors[np.array(Z_list_meshed) > 20] = (0, 0, 0, 0)

levels = MaxNLocator(nbins=10).tick_values(-147, 20)

fig, ax = plt.subplots()
norm = plt.Normalize(vmin=-200, vmax=20)
cont = plt.contourf(X_list,Y_list,Z_list,
                    cmap='coolwarm',
                    levels=levels
                    # vmin=-147,vamx=20,
                    #facecolors=colors

                    )
# ax.set_aspect('equal','box')
plt.colorbar()

plt.show()
"""