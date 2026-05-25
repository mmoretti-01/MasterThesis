# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from matplotlib import pyplot as plt
import Plots.Plot_Vib as Vib
import Plots.Plot_ASD as ASD
import Functions_Table.Functions_Table_NL as nl
import Functions_Table.Functions_Table_Linear as lin
import Functions_ASD.Functions_PSI as PSI



""" ---------- Visualisation of Array structures ---------- """
# ==============================
#    DATA STRUCTURE OVERVIEW
# ==============================
#
# Array structure: data[y][j][N]
#
# j = index for measurement data points
# y = 0 for frequency, 1 for sensor 2 measurement, 2 for sensor 4 measurement 
# N = selects which of the N measurements to consider
#
# Visualization (for a single i):
#
#       y=0 (frequency)      y=1 (sensor 2 measurement)
# j=0    data[0][0][N]          data[0][1][N]
# j=1    data[1][0][N]          data[1][1][N]
# j=2    data[2][0][N]          data[2][1][N]
#  ...        ...                    ...
#
# 
# ==============================
#      DATA_A ARRAY STRUCTURE
# ==============================
#
# Array structure: data_a[n][j][l]
#
# n = selects which of the 3 measurements to consider
# j = index for measurement data points
# l = 0 for frequency, 1 for sensor measurement
#
# Visualization (for a single i):
#
#       l=0 (frequency)      l=1 (sensor measurement)
# j=0    data_a[n][0][0]          data_a[n][0][1]
# j=1    data_a[n][1][0]          data_a[n][1][1]
# j=2    data_a[n][2][0]          data_a[n][2][1]
#  ...         ...                     ...
#

""" ---------- Parameters ---------- """

# i: Dataset selector — either "a" or "b", determining which dataset to use.
# n: Direction index — selects the directional component of the dataset:
#    0 → Longitudinal-direction
#    1 → z-direction
#    2 → Transversal-direction
# points: FFT window length in data points (not in seconds). Defines the FFT window size. !Use "full" if you don't want to use windowing.!
# overlap: Percentage of window points overlapping between consecutive FFT windows.
# window_length: Window length for the Savitzky-Golay (SG) filter used in smoothing ASD data.
# polyorder: Polynomial order used in the SG filter.
# m: Sample number or index specifying which sample to analyze.
# y: Sensor identifier indicating which sensor’s data is used.
# p0: Initial parameters for the fit function (used in fitting resonance curves).

#Recommended Parameters
i = "a"
n = 2
points = 1024
overlap = 0.66
window = 31
order = 3
N = 40
N = N + 16
y = 1
z = 2
w = 3
r = 5

#Up to which measurement shall the Histogram evaluate
l = 21

start = 56
stop = 70


""" ---------- Initial Values Fits ---------- """

#Initial values for the Harmonic Osci resonance fit
p0_HO = [1, 41, 90]
#p0_HO = [1, 21, 40]
#p0_2D = [1, 80, 60, -1, 10, 50, 1, 180, 50, 0.1, 220, 50]
#p0_2D = [0.5, 81, 56, 0.01, 8, 5, 0.01, 30, 20, 0.1, 114, 10] 

#Initial values for the Bernoulli Beam resonance fit
p0_BB_2 = [0.5, 21, 55, 0.1, 111, 20]

p0_BB_3 = [0.5, 21, 20, 0.1, 111, 30, 0.1, 250, 40]

p0_BB_4 = [0.2, 41, 50, 0.1, 93, 30, 1, 116, 50, 0.1, 200, 20] 

#p0_BB_5 = [1, 39, 84, 0.1, 91, 60, 0.1, 125, 40, 0.1, 200, 15, 0.1, 242, 20]

#p0_BB_5 = [0.90, 39, 84, 0.1, 91, 70, 0.1, 125, 50, 0.1, 200, 15, 0.1, 242, 40] #for 17

#p0_BB_5 = [0.95, 39, 84, 0.1, 93, 80, 0.1, 123, 80, 0.1, 200, 15, 0.1, 242, 20] #for 23

p0_BB_5 = [1, 39, 84, 0.1, 91, 60, 0.1, 125, 30, 0.1, 200, 15, 0.1, 242, 20] #for 28

#p0_BB_5 = [0.9, 19, 40, 0.1, 40, 40, 0.1, 85, 90, 0.01, 180, 14, 0.1, 230, 90]

#p0 = [1000, 100, 10, 3, 1, 100000]
p0 = [1000, 100, 10, 3, 1, 100000]

z = [[0.670, 0.641, 0.577, 0.535, 0.430, 0.409, 0.405, 0.371, 0.320, 0.234, 0.395, 0.398, 0.366, 0.337, 0.244, 0.670, 0.641, 0.577, 0.535, 0.430, 0.409, 0.405, 0.360, 0.307, 0.234, 0.395, 0.398, 0.366, 0.337, 0.244],
             [0.754, 0.897, 0.842, 0.679, 0.375, 0.919, 1.011, 1.012, 0.999, 0.752, 1.209, 1.486, 1.241, 1.269, 0.931, 0.754, 0.897, 0.842, 0.679, 0.375, 0.919, 1.011, 0.671, 0.700, 0.752, 1.209, 1.486, 1.241, 1.269, 0.931],
             [1.943, 2.013, 1.871, 1.714, 1.259, 1.722, 1.808, 1.774, 1.702, 1.307, 2.084, 2.467, 2.091, 2.099, 1.555, 1.943, 2.013, 1.871, 1.714, 1.259, 1.722, 1.808, 1.331, 1.299, 1.307, 2.084, 2.467, 2.091, 2.099, 1.555]]

z = np.array(z)
#z = 0

p0_tension = [1, 32]

""" ---------- DIY ---------- """
#Vib.tension_dep(p0_tension)

#Vib.four_col_comp(71, 76, 77, 78, 1, 1)
#Vib.four_col_comp(57, 58, 59, 60, 1, 1)

#ASD.ASD_response(i, n, points, overlap, N, r, p0_BB_5)
#ASD.ASD_plot(i, n, points, overlap)
Vib.single_pic(N,1)
#Vib.single_pic_comp(N-1,N,r,r)
#Vib.three_col_comp(83, 82, 84 , 1, 1, 1)
#Vib.two_col_comp(56, 83, 1, 1)
#Vib.two_col_comp(82, 84, 1, 1)
#Vib.plot_fit(N, p0_BB_5, r)
#Vib.single_pic_comp(N, N, 1, 5)
#Vib.single_test(N, p0_BB_5, y, z, w)
#ASD.Ladder_Contour(i, n, points, overlap, start, stop, r, p0_HO)
#ASD.Ladder_Contour_xyz(i, points, overlap, start, stop, r, p0_HO, z)


#ASD.ASD_smooth_SG(i, n, points, overlap, window, order) 

#ASD.envelope_plot(i, n, points, overlap)

#ASD.Histo_env(i, points, overlap, y, l, p0_HO)
#ASD.Histo_int_HO(i, points, overlap, window, order, y, l, p0_HO)
#ASD.Histo_int_HO_100(i, points, overlap, window, order, y, l, p0_HO)

#ASD.Displacement_vs_frequency_xyz(i, points, overlap, window, order, N, r, p0_BB_5)
ASD.Displacement_vs_frequency_ana(i, n, points, overlap, window, order, N, r, p0_HO)


#Vib.two_col_comp(79, 79, 2, 3)

print(nl.integrate_disc__(N, r, p0_HO, i, 0, points, overlap))
print(nl.integrate_disc__(N, r, p0_HO, i, 1, points, overlap))
print(nl.integrate_disc__(N, r, p0_HO, i, 2, points, overlap))











