# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 10:28:27 2025

@author: moretti
"""

import numpy as np
from Get_Data_AirFlow import Get_Data_Cap
from Get_Data_AirFlow import Get_Data_Flow

import Plot_AirFlow as plot
import Functions_AirFlow as func
from scipy.signal import welch


""" ---------- Data Readout ---------- """

distances = Get_Data_Cap()
flows = Get_Data_Flow()

""" ---------- Visualisation of Array structures ---------- """
# ==============================
#    DISTANCES STRUCTURE OVERVIEW
# ==============================
#
# Array structure: distances[sample][measurement][type]
#
# sample      = index over all samples
# measurement = index over measurement points for each sample
# type        = 0 for time, 1 for voltage
#
# Visualization for sample s and measurements j:
#
#          type=0 (time)          type=1 (voltage)
# j=0    distances[s][0][0]      distances[s][0][1]
# j=1    distances[s][1][0]      distances[s][1][1]
# j=2    distances[s][2][0]      distances[s][2][1]
#  ...       ...               ...
#
# ==============================
#    FLOWS DATA STRUCTURE OVERVIEW
# ==============================
#
# Array structure: flows[sample][measurement]
#
# sample      = index to select which sample to look at
# measurement = index over measurement values within that sample
#
# Visualization for sample s:
#
# measurement=0    flows[s][0]
# measurement=1    flows[s][1]
# measurement=2    flows[s][2]
#     ...            ...
#


""" ---------- Parameters ---------- """
#Sampling rate determined in data aquisition script
rate = 1024
rate_ = 1

#Time of data aquisition also determined in the aquisition script
t = 60

#Nr of samples per measurement
samples = rate * t

#Scales the capacitor measurement in volts to distance measurement in micrometer
scaling_factor = 100

#Window length for windowing in FFT. Value is given in seconds thus x in [0,60]
window_len = 8
overlap = 0.66

#Setermines sample
m = 6

#Initial parameters for power law fit
p0 = [0.6, 3.3, 40]
p0_HO = [1,40,50]
p0_velo =[1]


""" ---------- DIY ---------- """

freqs, data = func.averaged_FFT(distances[89,:,1], rate, window_len, overlap)
#, data_flows = welch(flows[:,52], rate_, nperseg = 71, noverlap =None)

#plot.plot_fit_HO(freqs, data, p0_HO)

v_mean = func.merge_n_mean(flows,6,18)
v_mean2 = func.merge_n_mean(flows,20,28)



flows_mean = func.flows_average(flows[30:38]) 
flow_mean_1 = func.flows_average(flows[6:19])
flow_mean_2 = func.flows_average(flows[20:29])
flows_mean_4 = func.flows_average(flows[52:71]) 
#flows_mean_5 = func.flows_average(flows[71:87])
flows_mean_6 = func.flows_average(flows[87:102])
flow_mean = func.flows_average_(flows[102:119])
std1 = np.std(flows[116])
std2 = np.std(flows[117])

#p1 = [0.15622127, 2.28059467]
#print(func.comp_intersec(p1))

#plot.velocities(flow_mean[[0,4,6,8,10,12,14]],flow_mean[[1,5,7,9,11,13,15]], p0_velo)

plot.RMS_vs_Flow_comp(distances,41,59,75,90,flows_mean_4[1:],flows_mean_6,p0)
#plot.RMS_vs_Flow_comp(distances,59,75,75,90,flows_mean_5,flows_mean_6,p0)
#plot.RMS_vs_Flow(distances, 13, 18, v_mean2, p0)
#plot.RMS_vs_Flow(distances, 50, 54, flows_mean_5, p0)
#plot.RMS_vs_Flow(distances, 6, 13, flow_mean_1, p0)
#plot.RMS_vs_Flow(distances, 13, 18, flow_mean_2, p0)
#plot.RMS_vs_Flow(distances, 75, 90, flows_mean_6, p0)
#plot.RMS_vs_Flow(distances, 59, 75, flows_mean_5, p0)
#plot.RMS_vs_Flow(distances, 41, 59, flows_mean_4[1:], p0)
#plot.Plot_EV(distances[24])
#plot.Plot_FFT(freqs, data, 24)
#plot.Plot_FFT(freqs, data, 41)




