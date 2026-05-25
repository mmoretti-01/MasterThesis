# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 16:37:46 2025

@author: moretti
"""

import numpy as np
from scipy.signal import welch
from scipy.fft import fft, fftfreq
from scipy.optimize import curve_fit
from scipy.optimize import brentq
from scipy import odr


# Determines the RMS displacement (i.e., population standard deviation) of the input array
def RMS(dis):
    # Calculate the deviation from the mean, square it, take the mean, then square root
    return np.std(dis)

# Computes the Power Spectral Density (PSD) of the displacement signal using Welch's method
def PSD(dis, rate, points, overlap):
    # dis     : 1D signal array (e.g., displacement over time)
    # rate    : Sampling frequency in Hz
    # points  : Number of points per segment (nperseg)
    # overlap : Fraction of segment overlap (e.g., 0.5 for 50% overlap)

    # Compute PSD using Welch's method
    freq, PSD = welch(dis, fs = rate, nperseg = points, noverlap = points * overlap)
    return freq, PSD


# Computes the one-sided Fast Fourier Transform (FFT) magnitude spectrum of the displacement signal
def FFT(dis, rate):
    # dis     : 1D displacement signal array (time-domain)
    # rate    : Sampling frequency in Hz

    samples = len(dis)  # Number of samples in signal
    fft_vals = fft(dis)  # Compute FFT (complex values)
    fft_freqs = fftfreq(samples, 1/rate)  # Frequency bins in Hz

    # Keep only non-negative frequencies (one-sided spectrum)
    pos_mask = fft_freqs >= 0
    fft_freqs = fft_freqs[pos_mask]

    # Compute magnitude and normalize by number of samples
    fft_magnitude = np.abs(fft_vals[pos_mask]) / samples

    # Double all amplitudes except the DC component to account for single-sided spectrum
    fft_magnitude[1:] *= 2

    return fft_freqs, fft_magnitude

# Computes the averaged FFT magnitude spectrum of a signal using overlapping windowed segments
def averaged_FFT(dis, rate, window_len, overlap):
    # dis         : 1D displacement signal array (time-domain)
    # rate        : Sampling frequency in Hz
    # window_len  : Length of each window segment in seconds
    # overlap     : Fractional overlap between windows (0 <= overlap < 1)

    dis = np.array(dis)

    # Input validation
    if dis.ndim != 1:
        raise ValueError("Input signal must be a 1D array.")
    if np.any(np.isnan(dis)):
        raise ValueError("Input signal contains NaNs.")

    total_len = len(dis)

    if not (0 <= overlap < 1):
        raise ValueError("Overlap must be between 0 and <1.")

    # Convert window length from seconds to number of samples
    window_len_samples = int(window_len * rate)

    if window_len_samples > total_len:
        raise ValueError("Window length is greater than data length.")

    # Calculate step size between windows (accounting for overlap)
    step = int(window_len_samples * (1 - overlap))
    if step < 1:
        raise ValueError("Overlap too high for given window length.")

    segments = []
    window = np.hanning(window_len_samples)  # Hann window
    scale = np.sum(window) / window_len_samples  # Normalize window amplitude

    # Slide window over signal and compute FFT magnitude for each segment
    for start in range(0, total_len - window_len_samples + 1, step):
        segment = dis[start:start + window_len_samples]
        segment_windowed = segment * window / scale

        fft_freqs, fft_magnitude = FFT(segment_windowed, rate)
        segments.append(fft_magnitude)

    if not segments:
        raise ValueError("Not enough data for one FFT window.")

    # Average FFT magnitudes across all segments
    avg_magnitude = np.mean(segments, axis=0)

    return fft_freqs, avg_magnitude

# Averages pairs of rows in 'flows' between indices a and b, then returns sorted means of each averaged pair
#Old relict, where upstream and downstream velocities have been averaged, after CFD simulation I abandoned this approach
def merge_n_mean(flows, a, b):
    # flows : 2D NumPy array with shape (num_rows, 55)
    # a, b  : Start and end indices for merging (inclusive)
    
    # Initialize array to hold averaged pairs
    v = np.zeros([int((b - a + 2) / 2), 55])
    k = 0
    
    # Iterate over indices from a to b in steps of 2 to form pairs
    for i in range(a, b + 1, 2):
        # Average the pair of rows and store in v
        v[k] = 0.5 * (1*flows[i] + 1*flows[i + 1])
        k += 1
    
    # Compute mean of each averaged row (axis=1), then sort the means
    v_mean = np.sort(np.mean(v, axis=1))
    
    return v_mean

#Averages the measured flow values without sorting them, important for upstream downstream comparison
def flows_average_(flows):
    averages = np.mean(flows, axis=1)
    return averages

#Averages the measured flow values and sorts them, important for measurements where v is not strictly increasing (earlier measurements)
def flows_average(flows):
    averages = np.mean(flows, axis=1)
    averages = np.sort(averages)
    return averages

#Again an relict for when I used to average upstream and downstream measurments
def flows_average_2nd(flows):
    # Select every second row (index 0, 2, 4, ...) from the 2D array
    reduced_flows = flows[::2, :]
    
    # Compute the mean along axis 1 (i.e., across columns)
    averages = np.mean(reduced_flows, axis=1)
    
    # Sort the averages
    averages = np.sort(averages)
    
    return averages

# Power-law function for curve fitting
def fit_function_lin(A, v):
    a, b = A
    #a * v**n + 18 - A * (5.2)**n
    n = 1
    return a * v**n + b

def fit_function_quad(A, v):
    # v : Independent variable (e.g., velocity or displacement)
    # A : Scale factor (fit parameter)
    # B : Exponent (fit parameter)
    a = A
    
    return a * v**2 

def fit_lin(A,v):
    
    a = A
    
    return a*v

def comp_intersec(p0):
    
    def f(x):
        return fit_function_quad(x, *p0) - 23
    
    v = brentq(f, a=0, b=50)
    
    return v


def get_fit_quad(v, v_err, RMS_err, RMS, p0):
    
    model = odr.Model(fit_function_quad)
    data = odr.RealData(v, RMS, sx=v_err)        # <-- only x-errors
    odr_run = odr.ODR(data, model, p0).run()
    return odr_run


def get_fit_lin(v, v_err, RMS_err, RMS, p0):
    
    model = odr.Model(fit_function_lin)
    data = odr.RealData(v, RMS, sx=v_err)        # <-- only x-errors
    odr_run = odr.ODR(data, model, p0).run()
    return odr_run

def get_lin(v, v_err, v2, v2_err, p0):
    
    model = odr.Model(fit_lin)
    data = odr.RealData(v, v2, sx=v_err, sy=v2_err)        # <-- only x-errors
    odr_run = odr.ODR(data, model, p0).run()
    return odr_run

def resonance_curve_HO(f, A, f0, Q):
    return A/(np.sqrt((1-(f/f0)**2)**2 + (1/Q)**2 * (f/f0)**2))

def get_fit_HO(f, RMS, p0):
    popt, pcov = curve_fit(resonance_curve_HO, f, RMS, p0, maxfev=1000, bounds=(0, np.inf))
    return popt

