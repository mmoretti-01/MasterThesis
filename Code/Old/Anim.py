# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 13:12:05 2025

@author: moretti
"""

import numpy as np
import matplotlib 
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import scipy as sp
from scipy.optimize import curve_fit
import os

pi = np.pi
x = np.linspace(0,36,50)
y = np.linspace(0,3,50)
X, Y = np.meshgrid(x, y)
Z = (np.sin(X*pi/36)+np.sin(X*pi/36)*np.cos(Y*pi/3))
t = np.linspace(0,100,100)

fig, ax = plt.subplots(figsize = (10,3))
contour = ax.contourf(X, Y, Z, levels = 35, cmap="coolwarm")



def update(t):
    Z_ = (np.sin(X*pi/36)+np.cos(Y*pi/3))*np.sin(2*pi*t/100)
    contour = ax.contourf(X, Y, Z_, levels = 35, cmap="coolwarm", alpha = 0.75)
    ax.set_title(f"Time Step: {t}")
    cbar = plt.colorbar(contour)
    plt.show()
    return contour.collections

anim = animation.FuncAnimation(fig, update, frames = 50, interval = 100)


plt.xlim(0,36)
plt.ylim(0,3)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_yticks([0,1,2,3])

plt.tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
plt.rcParams["figure.dpi"] = 360
plt.savefig("C:/Users/moretti/Desktop/contour", dpi=300)
plt.show()