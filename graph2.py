import math
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
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

first_x = -0.75
first_y = 0.55
h = 1e-8

def Exy(x,y):
    Exy = 0
    for i in range(4):
        Exy += A[i]*math.exp(a[i]*((x - X[i])**2) + b[i]*(x - X[i])*(y - Y[i]) + c[i]*((y - Y[i])**2))
    return Exy
#1階微分
def fx(x,y):
    result = (Exy(x+h,y) - Exy(x-h,y))/(2*h)
    return result

def fy(x,y):
    result = (Exy(x,y+h) - Exy(x,y-h))/(2*h)
    return result
#2階微分
def fxx(x,y):
    result = (fx(x+h,y) - fx(x-h,y))/(2*h)
    return result

def fyy(x,y):
    result = (fy(x,y+h) - fy(x,y-h))/(2*h)
    return result

def fxy(x,y):
    result = (fx(x,y+h) - fx(x,y-h))/(2*h)
    return result

def fyx(x,y):
    result = (fy(x+h,y) - fy(x-h,y))/(2*h)
    return result
#へシアン*一次微分
def hessian_x(x,y):
    result = (fyy(x,y)*fx(x,y) - fxy(x,y)*fy(x,y))/(fxx(x,y)*fyy(x,y) - fxy(x,y)*fyx(x,y))
    return result

def hessian_y(x,y):
    result = (-fxy(x,y)*fx(x,y) + fxx(x,y)*fy(x,y))/(fxx(x,y)*fyy(x,y) - fxy(x,y)*fyx(x,y))
    return result

x = first_x
y = first_y
fx_tmp = 1
fy_tmp = 1

#Newton法で鞍点まで行く
with open('final_A.dat','w') as f:
    while(fx_tmp >1e-5 and fy_tmp > 1e-5):
        Exy_tmp = Exy(x,y)
        result1 = "{:.6f} {:.6f} {:.6f}\n".format(x,y,Exy_tmp)
        f.write(result1)
        hessian_x_tmp = hessian_x(x,y)
        hessian_y_tmp = hessian_y(x,y)
        x = x - hessian_x_tmp
        y = y - hessian_y_tmp
        fx_tmp = abs(fx(x,y))
        fy_tmp = abs(fy(x,y))
    #固有値,固有ベクトルを求めたい
    #ヤコビ法のθを求める
    def theta(x,y):
        result = 0.5/(math.tan(2*fxy(x,y)/(fxx(x,y) - fyy(x,y))))
        return result
    #固有値
    def Eigenvalue_x(x,y,theta):
        result = fxx(x,y)*(math.cos(math.radians(theta)))**2 + fyy(x,y)*(math.sin(math.radians(theta)))**2 + fxy(x,y)*(math.sin(2*math.radians(theta)))
        return result

    def Eigenvalue_y(x,y,theta):
        result = fxx(x,y)*(math.sin(math.radians(theta)))**2 + fyy(x,y)*(math.cos(math.radians(theta)))**2 - fxy(x,y)*(math.sin(2*math.radians(theta)))
        return result
    #虚振動の方向に1回降りる
    z = theta(x,y)

    omega1 = Eigenvalue_x(x,y,z)
    omega2 = Eigenvalue_y(x,y,z)
    step = 0.01

    if (omega1 < 0):
        x = x - step*math.cos(math.radians(z))/math.sqrt((math.cos(math.radians(z)))**2 + (math.sin(math.radians(z)))**2)
        y = y - step*math.sin(math.radians(z))/math.sqrt((math.cos(math.radians(z)))**2 + (math.sin(math.radians(z)))**2)

    if (omega2 < 0):
        x = x - step*math.sin(math.radians(z))/math.sqrt((math.cos(math.radians(z)))**2 + (math.sin(math.radians(z)))**2)
        y = y - step*( -math.cos(math.radians(z))/math.sqrt((math.cos(math.radians(z)))**2 + (math.sin(math.radians(z)))**2))

    result2 = "{:.6f} {:.6f} {:.6f}\n".format(x,y,Exy(x,y))
    f.write(result2)

    checkdx = 1
    checkdy = 1
    Eb =10
    while(checkdx > 1.0E-5 and checkdy > 1.0E-5):

        fx_tmp = fx(x,y)
        checkdx = abs(fx_tmp)
        #dxExy_tmpが正の時は、ｘを負の方向に、dxExy_tmpが負の時は、xを正の方向に動かす
        x = x - step*fx_tmp/math.sqrt(fx_tmp**2 + fy_tmp**2)

        fy_tmp = fy(x,y)
        checkdy = abs(fy_tmp)
        y = y - step*fy_tmp/math.sqrt(fx_tmp**2 + fy_tmp**2)
        Exy_tmp = Exy(x,y)
        Ea = Eb
        Eb = Exy_tmp
        dE = Eb - Ea
        if (dE > 0):
            step /= 10
        result3 = "{:.6f} {:.6f} {:.6f}\n".format(x,y,Exy_tmp)
        f.write(result3)
f.close