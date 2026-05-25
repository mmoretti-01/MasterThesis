# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 10:26:04 2025

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
import time



Length_a, data_a = Get_Data("a")  

#----------------------------------------
""" --> Freq/ASD/PSD <-- """
#----------------------------------------

def get_ASD_a(n, points, overlap):
    fs = 512
    
    if points == "full":
        points = len(data_a[n, :, 1])
        overlap = 0
        
    freqs, asd = welch(data_a[n,:,1], fs, nperseg=points, return_onesided=True,  noverlap = points * overlap)
    asd = asd * 10 ** (12)
    return freqs, asd
    
    
def get_PSD_a(n, points, overlap):
    f, asd = get_ASD_a(n, points, overlap)
    psd = asd * (2 * np.pi * f)**(-4)
    psd = psd.astype(float)
    return f, psd

# The Savitzky-Golay (SG) filter is a smoothing technique similar to a moving average,
# but instead of simply averaging points, it fits a polynomial to a window of data points.
# The value at the center of the window is replaced by the polynomial's value at that point,
# which helps preserve features like peaks and slopes better than a simple moving average.
def SG_smooth_a(n, points, overlap, window, order):
    f, asd = get_ASD_a(n, points, overlap)
    asd_log = np.log10(asd)
    asd_log_smooth = savgol_filter(asd_log, window_length = window, polyorder = order)
    asd_smooth = 10**asd_log_smooth
    #asd_smooth = savgol_filter(asd, window_length = window, polyorder = order)
    return f, asd_smooth

def move_av(n, points, overlap, window):
    window_s = window
    weights = np.ones(window_s)/window_s
    #One could use further np.log10(np.log10(...)) to get the curve shifted even more to the lower end!
    f, asd = get_ASD_a(n, points, overlap)
    asd_av = np.convolve(np.log10(asd), weights, mode = "same")
    return f, 10**asd_av

def get_env_a(n, points, overlap):
    f, asd = get_ASD_a(n, points, overlap)

    # convert 10 Hz to samples based on your frequency step
    df = np.median(np.diff(f))
    min_distance_samples = max(1, int(round(5.0 / df)))

    # find peaks at least 10 Hz apart
    peaks, _ = find_peaks(asd, distance=min_distance_samples)

    f_peaks = f[peaks]
    y_peaks = asd[peaks]
    envelope_func = interp1d(f_peaks, y_peaks, kind='linear', fill_value="extrapolate")
    envelope = np.abs(envelope_func(f))
    return f, envelope