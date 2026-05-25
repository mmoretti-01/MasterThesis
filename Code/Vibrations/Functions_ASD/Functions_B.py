# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 10:29:11 2025

@author: moretti
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import welch
from scipy.signal import savgol_filter
from scipy import integrate
from Get_Data_Vib import Get_Data
from scipy.signal import find_peaks
from scipy.interpolate import interp1d
from scipy.ndimage import maximum_filter1d
import time


data_b = Get_Data("b") 

#----------------------------------------
""" --> Freq/ASD/PSD <-- """
#----------------------------------------

def get_ASD_b(n):
    freqs = data_b[:,3]
    freqs = freqs.astype(float)
    asd = data_b[:,n]*(2*np.pi*(freqs))**(4)
    asd = asd[:].astype(float)
    asd = asd * 10 ** (12)
    return freqs, asd
    
def get_PSD_a(n, m, over):
    f, asd = get_ASD_b(n)
    psd = asd * (2 * np.pi * f)**(-4)
    psd = psd.astype(float)
    return f, psd

def SG_smooth_b(n, window, order):
    f, asd = get_ASD_b(n)
    asd_log = np.log10(asd)
    asd_log_smooth = savgol_filter(asd_log, window_length = window, polyorder = order)
    return f, 10**asd_log_smooth

def move_av(n, points, overlap, window):
    window_s = window
    weights = np.ones(window_s)/window_s
    #One could use further np.log10(np.log10(...)) to get the curve shifted even more to the lower end!
    f, asd = get_ASD_b(n)
    asd_av = np.convolve(np.log10(asd), weights, mode = "same")
    return f, 10**asd_av

def get_env_b(n):
    f, asd = get_ASD_b(n)
    peaks, _ = find_peaks(asd)
    f_peaks = f[peaks]
    y_peaks = asd[peaks]
    envelope_func = interp1d(f_peaks, y_peaks, kind='cubic', fill_value="extrapolate")
    envelope = np.abs(envelope_func(f))
    return f, envelope