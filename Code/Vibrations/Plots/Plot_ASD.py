# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 13:57:02 2025

@author: moretti
"""

import os
import numpy as np
import Functions_ASD.Functions_PSI as PSI
import Functions_Table.Functions_Table_Linear as lin
import Functions_Table.Functions_Table_NL as nl
from scipy import integrate
from matplotlib import pyplot as plt
from scipy.interpolate import griddata



code_dir = os.path.dirname(os.path.realpath(__file__))
Pic = os.path.join(code_dir, "..", "..", "..", "Pictures")

""" ---------- Parameter Explenation ---------- """
# i: Dataset selector — either "a" or "b", determining which dataset to use.
# n: Direction index — selects the directional component of the dataset:
#    0 → x-direction
#    1 → y-direction
#    2 → z-direction
# points: FFT window length in data points (not in seconds). Defines the FFT window size.
# overlap: Number of points overlapping between consecutive FFT windows.
# window_length: Window length for the Savitzky-Golay (SG) filter used in smoothing ASD data.
# polyorder: Polynomial order used in the SG filter.
# m: Sample number or index specifying which sample to analyze.
# y: Sensor identifier indicating which sensor’s data is used.
# p0: Initial parameters for the fit function (used in fitting resonance curves).



""" ---------- Plots ---------- """


#Oxford colours https://communications.admin.ox.ac.uk/communications-resources/visual-identity/identity-guidelines/colours

def ASD_response(i, n, points, overlap, m, y, p0):
    
    # Create a high-resolution plot figure and axis
    fig, ax = plt.subplots(figsize=(6,4), dpi=300)
    
    # Get frequency array and ASD (Acceleration Spectral Density) data for the given parameters
    freqs, asd = PSI.get_ASD(i, n, points, overlap)
    
    # Discard low-frequency points (first 20 indices) to avoid instability or irrelevant data
    freqs = freqs[20:]
    asd = asd[20:]
    
    fit_label = "BB-Model Fit"
    
    if len(p0)/3 == 1:
        popt = lin.get_fit_HO(m, p0, y)
        fit = lin.resonance_curve_HO(freqs, *popt)
        fit_sq = fit **2
        fit_label = "HO-Model Fit"
    
    elif len(p0)/3 == 2:
        popt = nl.get_fit_BB_2(m, p0, y)
        fit = nl.resonance_curve_BB_2(freqs, *popt)
        fit_sq = fit **2
    
    elif len(p0)/3 == 3:
        popt = nl.get_fit_BB_3(m, p0, y)
        fit = nl.resonance_curve_BB_3(freqs, *popt)
        fit_sq = fit **2
        
    elif len(p0)/3 == 4:
        popt = nl.get_fit_BB_4(m, p0, y)
        fit = nl.resonance_curve_BB_4(freqs, *popt)
        fit_sq = fit **2
        
    elif len(p0)/3 == 5:
        popt = nl.get_fit_BB_5(m, p0, y)
        fit = nl.resonance_curve_BB_5(freqs, *popt)
        fit_sq = fit **2
        
    else:
        print("wrong initial guess format")
        return 
    
    # Plot the normalized squared resonance curve (label 'a')
    ax.plot(freqs, fit_sq, color="#002147", label = fit_label)
    
    # Scatter plot of the smoothed ASD data points
    ax.scatter(freqs, asd / (2 * np.pi * freqs)**4, marker="o", s=2, color="#002147", alpha=0.33, label="Smoothed PSD")
    
    # Plot the integrand: ASD multiplied by normalized resonance curve squared and scaled by frequency factor
    integrand = asd * fit_sq / (2 * np.pi * freqs)**4
    ax.plot(freqs, integrand, color="#776885", label="Integrand")
    
    # Set both axes to logarithmic scale for better visualization of frequency domain data
    ax.set_yscale("log")
    ax.set_xscale("log")
    
    # Label the axes with appropriate units and font styling
    plt.xlabel("Frequency in Hz", fontsize=15, fontname="Times New Roman")
    plt.ylabel("Integral Terms w/ corresponding units", fontsize=13, fontname="Times New Roman")
    
    # Limit x-axis frequency range to between 8 Hz and 500 Hz
    plt.xlim([12, 256])
    
    # Add grid lines for easier reading of plot
    plt.grid()
    
    # Hide plot spines for a cleaner look
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    # Define the path to save the figure (assumes 'Pic' and 'os' are defined elsewhere)
    Pict = os.path.join(Pic, "LadderRes")
    
    # Set the plot title with font styling
    plt.title("Ladder Response Function", fontname="Times New Roman", fontsize=15, fontstyle='italic')
    
    # Save the figure with high DPI
    plt.savefig(Pict, dpi=300)
    
    # Add legend and display the plot
    plt.legend(markerscale=3, bbox_to_anchor=(0.85, 0.95), borderpad=0.25, frameon=False, fontsize = 8)
    
    # Show the plot interactively
    plt.show()
    
    return

def ASD_plot(i, n, points, overlap):
    # Create a figure and axis for plotting, high resolution for clarity
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    
    # Obtain frequency and raw ASD data from the provided parameters
    freq, asd = PSI.get_ASD(i, n, points, overlap)
    # Scatter plot of the original ASD data with transparency for visual comparison
    ax.scatter(freq, asd, marker="o", s=2, color="#002147", label="Longitudinal Direction")
    # Set y-axis to logarithmic scale for better visualization of spectral density over wide range
    ax.set_yscale("log")
    
    # Set specific frequency ticks on x-axis for better readability
    ax.set_xticks([1, 10, 100, 200])
    
    # Limit the x-axis frequency range from 0 to 250 Hz
    plt.xlim([0, 256])
    
    # Enable grid lines for easier interpretation of the plot
    plt.grid()
    
    # Label axes with appropriate units and font styling
    plt.xlabel("Frequency in Hz", fontsize=15, fontname="Times New Roman")
    plt.ylabel("Acceleration spectral density $\mu m^2/s^3$", fontsize=15, fontname="Times New Roman")
    
    # Set tick parameters to control size and length of axis ticks for neatness
    plt.tick_params(axis="both", which="both", labelsize=8, length=4)
    
    # Set figure DPI globally (affects subsequent figures as well)
    plt.rcParams["figure.dpi"] = 360
    
    # Hide plot frame lines (spines) for a cleaner look
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Define path to save the plot (assumes Pic and os are defined globally)
    Pict = os.path.join(Pic, "ASD")
    
    # Set plot title with font styling
    plt.title("Mu3e Site Vibrations", fontname="Times New Roman", fontsize=15, fontstyle='italic')
    
    # Display legend outside plot area for clarity with customized marker scale
    plt.legend(markerscale=1.5, bbox_to_anchor=(1.00, 0.95), borderpad=0.25, frameon=False, fontsize=10)
    
    # Save figure with high dpi
    plt.savefig(Pict, dpi=300)
    
    # Show plot interactively
    plt.show()
    
    return

def ASD_smooth_SG(i, n, points, overlap, window, order):
    # Create a figure and axis for plotting, high resolution for clarity
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    
    # Obtain frequency and raw ASD data from the provided parameters
    freq, asd = PSI.get_ASD(i, n, points, overlap)
    
    # Apply Savitzky-Golay smoothing filter to the ASD data with specified window length and polynomial order
    _, asd_smooth = PSI.SG_smooth(i, n, points, overlap, window, order)
    
    # Scatter plot of the smoothed ASD data in a distinct color and marker size
    #ax.scatter(freq, asd_smooth, marker="o", s=2, color="#994636", label="Smoothed")
    #ax.plot(freq, asd_smooth, linewidth=2.0, color="#994636", label="Smoothed")
    
    # Scatter plot of the original ASD data with transparency for visual comparison
    ax.scatter(freq, asd, marker="o", s=2, color="#002147", label="Transverse direction")
    
    # Set y-axis to logarithmic scale for better visualization of spectral density over wide range
    ax.set_yscale("log")
    
    # Set specific frequency ticks on x-axis for better readability
    #ax.set_xticks([1, 10, 100, 200])
    
    # Limit the x-axis frequency range from 0 to 250 Hz
    plt.xlim([0, 256])
    
    # Enable grid lines for easier interpretation of the plot
    plt.grid()
    
    # Label axes with appropriate units and font styling
    plt.xlabel("Frequency (Hz)", fontsize=15, fontname="Times New Roman")
    plt.ylabel(r"Acceleration SD ($\mu$m$^{2}$/s$^{3}$)", fontsize=15, fontname="Times New Roman")
    
    # Set tick parameters to control size and length of axis ticks for neatness
    plt.tick_params(axis="both", which="both", labelsize=8, length=4)
    
    # Set figure DPI globally (affects subsequent figures as well)
    plt.rcParams["figure.dpi"] = 360
    
    # Hide plot frame lines (spines) for a cleaner look
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Define path to save the plot (assumes Pic and os are defined globally)
    Pict = os.path.join(Pic, "ASD_smooth_re.png")
    
    # Set plot title with font styling
    #plt.title("Mu3e Site Vibrations and Smoothed Fit", fontname="Times New Roman", fontsize=15, fontstyle='italic')
    
    # Display legend outside plot area for clarity with customized marker scale
    #plt.legend(markerscale=3, bbox_to_anchor=(1.00, 0.90), borderpad=0.25, fontsize=10)
    
    legend = plt.legend(
    markerscale=3,
    bbox_to_anchor=(1, 0.90),
    borderpad=0.25,
    fontsize=10,
    labelspacing=0.5,
    frameon=True
    )
    
    frame = legend.get_frame()
    frame.set_edgecolor("black")   # black border
    frame.set_linewidth(0.5)       # thin border
    frame.set_facecolor("white")   # optional: white background
    
    
    # Save figure with high dpi
    plt.savefig(Pict, dpi = 300)
    
    # Show plot interactively
    plt.show()
    
    return


def envelope_plot(i, n, points, overlap):
    # Obtain frequency vector and acceleration spectral density (ASD)
    f, asd = PSI.get_ASD(i, n, points, overlap)
    
    # Obtain envelope data corresponding to the ASD frequencies
    _, data = PSI.envelope(i, n, points, overlap)
    
    
    # Create figure and axis for plotting
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    
    # Plot the envelope data points as orange scatter plot
    #ax.scatter(f, data, marker="o", s=2, color="#994636", label="Envelope (upper)")
    ax.plot(f, data, linestyle = "--", linewidth=2.0, color="#FFB81C", label="Envelope (upper)")
    
    # Plot the raw ASD data points as blue scatter plot with some transparency
    ax.scatter(f, asd, marker="o", s=2, color="#002147", label="Segmented FFT data")
    
    # Set y-axis to logarithmic scale to cover broad range of spectral densities
    ax.set_yscale("log")
    plt.xlim([0, 256])
    
    # Enable grid for better readability
    plt.grid()
    
    # Label x and y axes with units and Times New Roman font
    plt.xlabel("Frequency (Hz)", fontsize=15, fontname="Times New Roman")
    plt.ylabel(r"Acceleration SD ($\mu$m$^{2}$/s$^{3}$)", fontsize=15, fontname="Times New Roman")
    
    # Customize tick parameters for readability on both axes
    plt.tick_params(axis="both", which="both", labelsize=8, length=4)
    
    # Set high resolution for the figure globally (affects subsequent figures too)
    plt.rcParams["figure.dpi"] = 360
    
    # Hide the plot spines (frame lines) for cleaner appearance
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Add a title with font styling
    #plt.title("Mu3e Site Vibrations and Envelope Fit", fontname="Times New Roman", fontsize=15, fontstyle='italic')
    
    # Add a legend placed outside the plot area to the right, with scaled markers and no frame
    #plt.legend(markerscale=3, bbox_to_anchor=(1.00, 0.90), borderpad=0.25, fontsize=10)
    
    legend = plt.legend(
    markerscale=3,
    bbox_to_anchor=(1, 0.90),
    borderpad=0.25,
    fontsize=10,
    labelspacing=0.5,
    frameon=True
    )
    
    frame = legend.get_frame()
    frame.set_edgecolor("black")   # black border
    frame.set_linewidth(0.5)       # thin border
    frame.set_facecolor("white")   # optional: white background
    
    Pict = os.path.join(Pic, "ASD_enve.pdf")
    plt.savefig(Pict)
    # Display the figure
    plt.show()
    
    return

def Histo_env(i, points, overlap, y, l, p0_HO):
    # Initialize array to hold integral values for 3 directions over l samples
    int_values = np.zeros([3, l])
    
    # Calculate integral values for each index j and each direction (0,1,2)
    for j in range(l):
        int_values[:, j] = [
            lin.integrate_disc_HO_env(i, 0, points, overlap, j, y, p0_HO),
            lin.integrate_disc_HO_env(i, 1, points, overlap, j, y, p0_HO),
            lin.integrate_disc_HO_env(i, 2, points, overlap, j, y, p0_HO)
        ]
        
    # Create figure and axis for plotting
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    
    # Separate first 14 samples (Carbon) and rest (Kapton) for histogram
    values = int_values[0, :14]
    values = np.append(values, int_values[1, :14])
    values = np.append(values, int_values[2, :14])
    
    values1 = int_values[0, 14:l]
    values1 = np.append(values1, int_values[1, 14:l])
    values1 = np.append(values1, int_values[2, 14:l])
    
    # Plot histograms for Carbon and Kapton groups with different colors and transparency
    ax.hist(values, np.arange(0, 10.1, 0.5), edgecolor='black', alpha=0.66, color="#994636", label="Carbon")
    ax.hist(values1, np.arange(0, 10.1, 0.5), edgecolor='black', alpha=0.66, color="#002147", label="Kapton")
    
    # Set x-axis to logarithmic scale due to wide range of RMS displacement values
    ax.set_xscale("log")
    
    # Enable grid for better readability
    plt.grid()
    
    # Set figure DPI globally (affects subsequent plots too)
    plt.rcParams["figure.dpi"] = 360
    
    # Hide plot frame lines for cleaner look
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Set path to save figure (only one assignment needed)
    Pict = os.path.join(Pic, "Histo_envelope")
    
    # Label axes with appropriate units and font
    plt.xlabel("RMS Displacement in $\mu m$", fontsize=15, fontname="Times New Roman")
    plt.ylabel("Multiplicity", fontsize=15, fontname="Times New Roman")
    
    # Title with italic font style
    plt.title("Histogram of RMS displacement", fontname="Times New Roman", fontsize=15, fontstyle='italic')
    
    # Legend placement and styling
    plt.legend(markerscale=0.5, bbox_to_anchor=(0.95, 0.95), borderpad=0.25, frameon=False, fontsize=10)
    
    # Save figure to file
    plt.savefig(Pict, dpi=300)
    
    # Show the plot
    plt.show()
    
    return


def Displacement_vs_frequency_xyz(i, points, overlap, window_length, polyorder, m, y, p0):

    # Prepare arrays to hold data for 244 frequency points
    data_L = np.zeros(244)
    data_V = np.zeros(244)
    data_T = np.zeros(244)
    
    fit_label = "BB-Model Fit"
    g = 0
    
    if len(p0)/3 == 1:
        popt = lin.get_fit_HO(m, p0, y)
        fit_label = "HO-Model Fit"
        g = 1
    
    elif len(p0)/3 == 2:
        popt = nl.get_fit_BB_2(m, p0, y)
        g = 2
    
    elif len(p0)/3 == 3:
        popt = nl.get_fit_BB_3(m, p0, y)
        g = 3
        
    elif len(p0)/3 == 4:
        popt = nl.get_fit_BB_4(m, p0, y)
        g = 4
        
    elif len(p0)/3 == 5:
        popt = nl.get_fit_BB_5(m, p0, y)
        g = 5
        
    else:
        print("wrong initial guess format")
        return 
       
    def integrate__(n, p0_mod):
        
        # Define integrand as a function of frequency f
        def integrand(f):
            return (asd[20:] * (fit(f, p0_mod))**2) / (2*np.pi*f)**4

        # Get smoothed ASD data and frequency array
        freq, asd = PSI.SG_smooth(i, n, points, overlap, window_length, polyorder)
        
        # Use Simpson's integration over frequency range starting at index 20
        Int = integrate.simpson(integrand(freq[20:]), freq[20:])
        
        # Return RMS displacement as sqrt of integral
        return np.sqrt(Int)
    
    def fit(f, p0_fit):
         
        if g == 1:
            return lin.resonance_curve_HO(f, *p0_fit)
         
        elif g == 2:
            return nl.resonance_curve_BB_2(f, *p0_fit)
         
        elif g == 3:
            return nl.resonance_curve_BB_3(f, *p0_fit)
             
        elif g == 4:
            return nl.resonance_curve_BB_4(f, *p0_fit)
             
        elif g == 5:
            return nl.resonance_curve_BB_5(f, *p0_fit)
             
        else:
            print("wrong initial guess format")
            return 
        return
    
    # Frequency range from 12 to 255 (inclusive)
    f = np.arange(12,256,1)
    
    # Loop over frequency values to compute RMS displacement for each axis
    for f0 in f:
        
        # Update the resonance frequency in parameters
        popt[1] = f0
        
        # Calculate RMS displacement for each axis and store in arrays
        data_L[f0-12] = integrate__(0, popt)
        data_V[f0-12] = integrate__(1, popt)
        data_T[f0-12] = integrate__(2, popt)
            
        
    # Plotting section
    fig, ax = plt.subplots(figsize=(6,4), dpi=300)
    
    # Scatter plot for each axis displacement vs frequency
    ax.scatter(f, data_L, marker="o", s=2, color="#002147", label="Longitudinal-Axis")
    ax.scatter(f, data_V, marker="o", s=2, color="#994636", label="Z-Axis")
    ax.scatter(f, data_T, marker="o", s=2, color="#426A5A", label="Transversal-Axis")
    
    # Log scale for y-axis to handle wide range of displacement values
    ax.set_yscale("log")
    plt.grid()
    plt.xlabel("Frequency in Hz", fontsize=15, fontname="Times New Roman")
    plt.ylabel("RMS displacement in $\mu m$", fontsize=15, fontname="Times New Roman")
    plt.tick_params(axis="both", which="both", labelsize=8, length=4)
    plt.rcParams["figure.dpi"] = 360
    
    # Remove plot frame borders for cleaner look
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    plt.title("Mu3e Site Vibrations " + fit_label, fontname="Times New Roman", fontsize=15, fontstyle='italic')
    plt.legend(markerscale=1.5, bbox_to_anchor=(1.00, 0.95), borderpad=0.25, frameon=False, fontsize=10)
    plt.show()
    return

def Displacement_vs_frequency_ana(i, n, points, overlap, window_length, polyorder, m, y, p0):
    # Get frequency and ASD data from envelope, smoothed, and pure envelope methods
    f_env, asd_env = PSI.envelope(i, n, points, overlap)
    f_smooth, asd_smooth = PSI.SG_smooth(i, n, points, overlap, window_length, polyorder)
    f_pure, asd_pure = PSI.get_ASD(i, n, points, overlap)
    
    # Integration over envelope ASD data to compute RMS displacement
    def integrate__(i, p0_fit):
        def integrand(f):
            # Note: asd_env[20:] matches frequency slice f_env[20:]
            return (asd_env[20:] * (fit(f,p0_fit))**2) / (2*np.pi*f)**4
        Int = integrate.simpson(integrand(f_env[20:]), f_env[20:])
        return np.sqrt(Int)
    
    # Integration over smoothed ASD data
    def integrate_(i, p0_fit):
        def integrand(f):
            return (asd_smooth[20:] * (fit(f,p0_fit))**2) / (2*np.pi*f)**4
        Int = integrate.simpson(integrand(f_smooth[20:]), f_smooth[20:])
        return np.sqrt(Int)
    
    # Integration over pure envelope ASD data (full range)
    def integrate___(i, p0_fit):
        def integrand(f):
            return (asd_pure[20:] * (fit(f,p0_fit))**2) / (2*np.pi*f)**4
        Int = integrate.simpson(integrand(f_pure[20:]), f_pure[20:])
        return np.sqrt(Int)
    
    def fit(f, p0_fit):
         
        if g == 1:
            return lin.resonance_curve_HO(f, *p0_fit)
         
        elif g == 2:
            return nl.resonance_curve_BB_2(f, *p0_fit)
         
        elif g == 3:
            return nl.resonance_curve_BB_3(f, *p0_fit)
             
        elif g == 4:
            return nl.resonance_curve_BB_4(f, *p0_fit)
             
        elif g == 5:
            return nl.resonance_curve_BB_5(f, *p0_fit)
             
        else:
            print("wrong initial guess format")
            return 
        return

    # Initialize arrays for RMS displacement results over frequency range
    data_smooth = np.zeros(244)
    data_env = np.zeros(244)
    data_env_pure = np.zeros(244)

    # Get initial fit parameters for harmonic oscillator model
    fit_label = "BB-Model Fit"
    g = 0
    
    if len(p0)/3 == 1:
        popt = lin.get_fit_HO(m, p0, y)
        fit_label = "HO-Model Fit"
        g = 1
    
    elif len(p0)/3 == 2:
        popt = nl.get_fit_BB_2(m, p0, y)
        g = 2
    
    elif len(p0)/3 == 3:
        popt = nl.get_fit_BB_3(m, p0, y)
        g = 3
        
    elif len(p0)/3 == 4:
        popt = nl.get_fit_BB_4(m, p0, y)
        g = 4
        
    elif len(p0)/3 == 5:
        popt = nl.get_fit_BB_5(m, p0, y)
        g = 5
        
    else:
        print("wrong initial guess format")
        return 

    # Loop over frequencies 12 Hz to 255 Hz to calculate RMS displacements
    for f0 in range(12, 256, 1):
        popt[1] = f0  # Update resonance frequency parameter
        data_smooth[f0 - 12] = integrate_(i, popt)       # Using smoothed ASD
        data_env[f0 - 12] = integrate__(i, popt)         # Using envelope ASD
        data_env_pure[f0 - 12] = integrate___(i, popt)   # Using pure envelope ASD


    threshold = 23
    index = np.zeros([3,2], dtype=int)
    
    indices = np.where(data_smooth > threshold)[0]
    if indices.size == 0:
        print("No values above threshold found.")
        # Handle this case, maybe skip or assign a default value
    else:
        index[0,0] = indices[0]

        indices_below = np.where(data_smooth[index[0,0]:] < threshold)[0]
        if indices_below.size == 0:
            print("No values below threshold after first crossing.")
            # Handle this case too
        else:
            index[0,1] = index[0,0] + indices_below[0]
            print(r"1st Mode must not be in between: ", 12 + index[0,0], 12 + index[0,1])
    
    indices = np.where(data_env_pure > threshold)[0]
    if indices.size == 0:
        print("No values above threshold found.")
        # Handle this case, maybe skip or assign a default value
    else:
        index[1,0] = indices[0]

        indices_below = np.where(data_env_pure[index[1,0]:] < threshold)[0]
        if indices_below.size == 0:
            print("No values below threshold after first crossing.")
            # Handle this case too
        else:
            index[1,1] = index[1,0] + indices_below[0]
            print(r"1st Mode must not be in between: ", 12 + index[1,0], 12 + index[1,1])
    
    indices = np.where(data_env > threshold)[0]
    if indices.size == 0:
        print("No values above threshold found.")
        # Handle this case, maybe skip or assign a default value
    else:
        index[2,0] = indices[0]

        indices_below = np.where(data_env[index[2,0]:] < threshold)[0]
        if indices_below.size == 0:
            print("No values below threshold after first crossing.")
            # Handle this case too
        else:
            index[2,1] = index[2,0] + indices_below[0]
            print(r"1st Mode must not be in between: ", 12 + index[2,0], 12 + index[2,1])

    # Plotting results
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    f = np.arange(12, 256, 1)
    #ax.scatter(f, data_env, marker="o", s=2, color="#002147", label="Segmented & Envelope")
    ax.scatter(f, data_env_pure, marker="o", s=2, color="#002147", label = "Transverse & HO model")
    #ax.scatter(f, data_smooth, marker="o", s=2, color="#994636", label="Segmented & Smoothed")
    ##FFB81C
    
    ax.set_yscale("log")  # Logarithmic y-axis for RMS displacement
    plt.grid()
    plt.xlabel("First mode frequency (Hz)", fontsize=15, fontname="Times New Roman")
    plt.ylabel("RMS displacement ($\mu m$)", fontsize=15, fontname="Times New Roman")
    plt.tick_params(axis="both", which="both", labelsize=8, length=4)
    plt.rcParams["figure.dpi"] = 360
    plt.xlim([12,256])

    # Remove axis spines for cleaner appearance
    for spine in ax.spines.values():
        spine.set_visible(False)

    #plt.title("Expected RMS vs First Mode Frequency", fontname="Times New Roman", fontsize=15, fontstyle='italic')
    #plt.legend(markerscale=3, bbox_to_anchor=(0.50, 0.65), borderpad=0.25,  fontsize=10)
    
    legend = plt.legend(
    markerscale=3,
    bbox_to_anchor=(0.5, 0.65),
    borderpad=0.25,
    fontsize=10,
    labelspacing=0.5,
    frameon=True
    )
    
    frame = legend.get_frame()
    frame.set_edgecolor("black")   # black border
    frame.set_linewidth(0.5)       # thin border
    frame.set_facecolor("white")   # optional: white background
    
    
    plt.savefig("first mdoe dependency.pdf")
    plt.savefig("first mdoe dependency.png", dpi = 300)
    plt.show()
    return

def Ladder_Contour(i, n, points, overlap, start, stop, y, p0):
    freq, asd = PSI.get_ASD(i, n, points, overlap)
    z = np.array([])
    
    for j in range(start,stop+1):
        print(nl.integrate_disc_n(j, y, asd, freq, p0))
        z = np.append(z,nl.integrate_disc_n(j, y, asd, freq, p0))
        
    z = np.append(z,z)
        
    x = np.array([180, 150, 120, 90, 60, 180, 150, 120, 90, 60, 180, 150, 120, 90, 60, 180, 210, 240, 270, 300, 180, 210, 240, 270, 300, 180, 210, 240, 270, 300])
    y = np.array([0, 0, 0, 0, 0, 10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, -10, -10, -10, -10, -10])
    grid_x, grid_y = np.meshgrid(np.linspace(min(x), max(x), 100), np.linspace(min(y), max(y), 100))
    grid_z = griddata((x, y), z, (grid_x, grid_y), method='linear')
    
    plt.figure(figsize=(12, 2))
    
    contour = plt.contourf(grid_x, grid_y, grid_z, levels=30, cmap='viridis')
    plt.scatter(x, y, c=z, edgecolor = "k")  # Optional: show original points
    plt.colorbar(contour, label='Interpolated z-value')
    plt.gca().set_aspect(1.0)
    plt.title("Contour Plot from Scattered Data")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
    return

def Ladder_Contour_xyz(i, points, overlap, start, stop, r, p0, arr):
    
    x = np.array([180, 150, 120, 90, 60, 180, 150, 120, 90, 60, 180, 150, 120, 90, 60, 180, 210, 240, 270, 300, 180, 210, 240, 270, 300, 180, 210, 240, 270, 300])
    y = np.array([0, 0, 0, 0, 0, 10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, -10, -10, -10, -10, -10])
    grid_x, grid_y = np.meshgrid(np.linspace(min(x), max(x), 100), np.linspace(min(y), max(y), 100))
    
    num_j = 15
    z = np.zeros((3, num_j * 2))  # 2D array, doubled length for each row
    
    if type(arr) == type(5):
        print("yes")
        for n in range(3):
            freq, asd = PSI.get_ASD(i, n, points, overlap)
            row = []

            for j in range(start, stop + 1):
                val = nl.integrate_disc_n(j, r, asd, freq, p0)
                print(val)
                row.append(val)

            row_doubled = row + row

            z[n, :] = row_doubled
    else:
        print("no")
        z = arr
    
    vmin = np.min(z)
    vmax = np.max(z)
    levels = np.linspace(vmin, vmax, 30)  # Explicit levels for consistency

    fig, axes = plt.subplots(3, 1, figsize=(6, 4), sharex=True, sharey=True)
    plt.subplots_adjust(hspace=-0.40)

    contour_set = None

    for plot_idx, n in enumerate([2, 0, 1]):
        grid_zn = griddata((x, y), z[n], (grid_x, grid_y), method='linear')
        cont = axes[plot_idx].contourf(grid_x, grid_y, grid_zn, levels=levels, cmap='viridis', vmin=vmin, vmax=vmax)
        axes[plot_idx].scatter(x, y, c=z[n], edgecolor='k', cmap='viridis', vmin=vmin, vmax=vmax)
        axes[plot_idx].set_aspect(1.0)
        if contour_set is None:
            contour_set = cont


    # Add shared colorbar with full level range
    cbar = fig.colorbar(contour_set, ax=axes, orientation='vertical', label='RMS displacement ($\mu m$)')
    cbar.ax.tick_params(labelsize=8)
    
    for ax in axes:
        ax.tick_params(axis='both', which='major', labelsize=8)

    axes[0].set_title('Transverse direction', fontsize=12, fontname="Times New Roman")
    axes[0].axvline(x=180, color="black", linestyle="-", linewidth=2, alpha = 1)
    axes[1].set_title('Longitudinal direction', fontsize=12, fontname="Times New Roman")
    axes[1].axvline(x=180, color="black", linestyle="-", linewidth=2, alpha = 1)
    axes[2].set_title('Vertical direction', fontsize=12, fontname="Times New Roman")
    axes[2].set_xlabel("x (mm)", fontsize=15, fontname="Times New Roman")
    axes[2].axvline(x=180, color="black", linestyle="-", linewidth=2, alpha = 1)
    axes[1].set_ylabel("y (mm)", fontsize=15, fontname="Times New Roman")
    
    #plt.savefig("Contour.pdf", bbox_inches="tight")
    plt.savefig("Contour.png", dpi = 300)
    plt.show()
    return