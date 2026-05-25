# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 16:38:56 2025

@author: moretti
"""

import numpy as np
import matplotlib.pyplot as plt
import Functions_AirFlow as func

plt.rcParams.update({
    "figure.figsize": (6, 4),   # ~15 × 10 cm
    "font.size": 12,            # base font
    "axes.labelsize": 12,       # x/y labels
    "xtick.labelsize": 11, 
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
})


# Plots FFT magnitude spectrum on a log-log scale
def Plot_FFT(freqs, data, n):
    # freqs : Array of frequency bins (Hz)
    # data  : FFT magnitude data
    # n     : Index to start plotting from (to skip low-frequency noise or DC)

    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)

    # Scatter plot of FFT magnitude starting from index n
    ax.scatter(freqs[n:], np.abs(data[n:]), marker="o", s=2, color="#994636", label="FFT Data with Averaging")
    
    # Logarithmic scale for both axes
    ax.set_xscale("log")
    ax.set_yscale("log")

    # Set x-axis limits
    #plt.xlim([8, 512])

    # Enable grid for readability
    plt.grid()

    # Label axes with font settings
    plt.xlabel("Frequency in Hz", fontsize=15, fontname="Times New Roman")
    plt.ylabel(r"Fourier Transform magnitude $\mu m^2$", fontsize=15, fontname="Times New Roman")

    # Customize tick parameters
    plt.tick_params(axis="both", which="both", labelsize=8, length=4)

    # Set global figure DPI (affects all figures)
    plt.rcParams["figure.dpi"] = 360

    # Remove plot spines for cleaner appearance
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Title with font style
    plt.title("FFT of Wind-Tunnel", fontname="Times New Roman", fontsize=15, fontstyle='italic')

    # Uncomment below to add legend if needed
    # plt.legend(markerscale=1.5, bbox_to_anchor=(1, 1), borderpad=0.25, frameon=False, fontsize=10)

    # Show the plot
    plt.show()
    return

# Plots time evolution of displacement data
def Plot_EV(d):
    # d : 2D array with columns [time, displacement]

    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)

    # Scatter plot: time vs absolute displacement
    ax.scatter(d[:, 0], np.abs(d[:, 1]), marker="o", s=2, color="#994636", label=r'$\sim 5.9\,\mathrm{m/s}$')

    # Enable grid
    plt.grid()

    # Set axis labels with font styling
    plt.xlabel("Time in s", fontsize=15, fontname="Times New Roman")
    plt.ylabel(r"Distance in $\mu$m", fontsize=15, fontname="Times New Roman")

    # Customize ticks
    plt.tick_params(axis="both", which="both", labelsize=8, length=4)

    # Set figure DPI (global setting)
    plt.rcParams["figure.dpi"] = 360

    # Remove axis spines for clean appearance
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Title with font styling
    plt.title("Time evolution in Wind-Tunnel", fontname="Times New Roman", fontsize=15, fontstyle='italic')

    # Uncomment below to add legend if needed
    # plt.legend(markerscale=5, bbox_to_anchor=(0.90, 0.95), borderpad=0.25, frameon=False, fontsize=10)

    # Show plot
    plt.show()
    return

# Plots RMS displacement vs mean flow velocity with two fitted power-law curves
def RMS_vs_Flow(distances, n, m, v, p0):
    # distances : 3D array (e.g., [samples, points, coordinates])
    # n, m      : Start and end indices to select samples from distances
    # v         : Array of mean flow velocities corresponding to selected samples
    # p0        : Initial guess parameters for fit [A, B]

    RMS_val = []
    # Compute RMS displacement (assumed along second coordinate axis) for each sample in range [n, m)
    for i in range(n, m):
        RMS_val.append(func.RMS(distances[i, :, 1]))
    
    # Sort RMS values (Note: sorting may desynchronize with velocities if v is unsorted)
    RMS_values = np.sort(np.array(RMS_val))
    #print(np.max(RMS_values))

    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    
    #x_err is the velocities times 5% plus 0.3m/s
    #y_err is linearity of 0.05% of effective measurement range plus 0.015% of measurement range plus max sensitivity deviation
    #print(v[-1])
    y_err = np.zeros(m-n)
    for i in range(len(RMS_val)): 
        #y_err[i] = np.sqrt(((np.max(distances[n+i, :, 1])-np.min(distances[n+i, :, 1]))*0.0005)**2 + (0.15/np.sqrt(60000))**2 + (1/np.sqrt(60000))**2)
        y_err[i] = 1/np.sqrt(3)*np.sqrt(1 + 0.5**2)
        
    x_err = np.zeros(len(v))
    for i in range(len(v)):
        if v[i] < 2:
            x_err[i] = (v[i]*0.05 + 0.1)/np.sqrt(3)
        else:
            x_err[i] = (v[i]*0.05 + 0.3)/np.sqrt(3)

    # Fit power-law function to velocity vs RMS data
    # By changing the v index you can change up to which index a quadratic fit shall be made 
    odr = func.get_fit_quad(v[:10], x_err[:10], y_err[:10], RMS_values[:10], [p0[0]])
    odr_ = func.get_fit_lin(v[8:], x_err[8:], y_err[8:], RMS_values[8:], [p0[1], p0[2]])
    popt = odr.beta
    popt_ = odr_.beta
    
    t = np.arange(0, 6.25, 0.1)  # Generate smooth x-values for fitted curve
    t_ = np.arange(5.0, 9, 0.1)
    
    #Gets reduced chi2 and parameters with uncertainties for the plot labels
    a, = odr.beta
    da, = odr.sd_beta
    chi2_rel_quad = odr.res_var

    label_quad = (
    r"$x_{\mathrm{RMS}} = a_{\mathrm{quad}}\,v_{\mathrm{us}}^2$" + "\n"
    + fr"$a_{{\mathrm{{quad}}}} = {a:.1f} \pm 0.1\ \mathrm{{\mu m\,s^{{2}}\,m^{{-2}}}}$" + "\n"
    + fr"$\chi^2_\mathrm{{\nu}} = {chi2_rel_quad:.3f}$"
)

    
    b, c = odr_.beta
    db, dc = odr_.sd_beta
    chi2_rel_lin = odr_.res_var


    label_lin = (
    r"$x_{\mathrm{RMS}} = a_{\mathrm{lin}}\,v_{\mathrm{us}} + x_{\mathrm{int}}$" + "\n"
    + fr"$a_{{\mathrm{{lin}}}} = {b:.1f} \pm {db:.1f}\ \mathrm{{\mu m\,s^{{2}}\,m^{{-2}}}}$" + "\n"
    + fr"$x_{{\mathrm{{int}}}} = {c:.1f} \pm {dc:.1f}\ \mathrm{{\mu m}}$" + "\n"
    + fr"$\chi^2_\mathrm{{\nu}} = {chi2_rel_lin:.3f}$"
)

        

    print(y_err[-1])
    print(x_err[-1])
    print(np.max(RMS_values))
    
    # Scatter plot of RMS data vs flow velocity
    ax.scatter(v, RMS_values, marker="o", s = 15, color="#000000")
    ax.errorbar(v, RMS_values, xerr = x_err, yerr = y_err, fmt = "none", color="#000000", capsize = 5)
    # Plot fitted curve
    ax.plot(t, func.fit_function_quad(odr.beta, t), linewidth = 2.0, color="#215CAF", label = label_quad)
    
    ax.plot(t_, func.fit_function_lin(odr_.beta, t_), linewidth = 2.0, color="#CA6CAE", label = label_lin)
    
    # Add black horizontal line at y=23
    ax.axhline(y=23, color='#575757', linestyle='--', linewidth=1)
    

    # Optional error bars (commented out)
    # ax.errorbar(v, RMS_values, xerr=0.5, fmt='none', ecolor='#994636', capsize=5, label='Data with error')

    plt.grid()

    # Axis labels with font styling
    plt.xlabel("Mean upstream flow velocity (ms$^{-1}$)", fontsize=15, fontname="Times New Roman")
    plt.ylabel(r"RMS distance ($\mu$m)", fontsize=15, fontname="Times New Roman")

    # Tick styling
    plt.tick_params(axis="both", which="both", labelsize=8, length=4)

    # Remove axis spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Title and legend
    #plt.title("RMS vs Flow velocity", fontname="Times New Roman", fontsize=15, fontstyle='italic')
    #plt.legend(markerscale=1.5, bbox_to_anchor=(0.5, 0.5), borderpad=0.25, fontsize=10, labelspacing=1.5)
    
    legend = plt.legend(
    markerscale=1.5,
    bbox_to_anchor=(0.6, 0.55),
    borderpad=0.25,
    fontsize=10,
    labelspacing=1.5,
    frameon=True
    )
    
    frame = legend.get_frame()
    frame.set_edgecolor("black")   # black border
    frame.set_linewidth(0.5)       # thin border
    frame.set_facecolor("white")   # optional: white background
    
    plt.savefig("velocity-dependence.pdf")
    plt.show()
    return


# Compares RMS displacement vs mean flow velocity for two datasets (e.g., different materials)
def RMS_vs_Flow_comp(distances, n, m, a, b, v, w, p0):
    # distances : 3D array with displacement data
    # n, m      : Start and end indices for first dataset
    # a, b      : Start and end indices for second dataset
    # v, w      : Mean flow velocities corresponding to datasets [n,m) and [a,b)
    # p0        : Initial guess parameters for curve fitting [A, B]

    # Calculate RMS for first dataset
    print(distances[0,:,1])
    RMS_val = []
    for i in range(n, m):
        RMS_val.append(func.RMS(distances[i, :, 1]))
    RMS_values_0 = np.sort(np.array(RMS_val))  # Sorting might desynchronize pairs

    # Calculate RMS for second dataset
    RMS_val = []
    for i in range(a, b):
        RMS_val.append(func.RMS(distances[i, :, 1]))
    RMS_values_1 = np.sort(np.array(RMS_val))  # Same caution about sorting

    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    
    y_err = np.zeros(m-n)
    for i in range(len(RMS_val)): 
        #y_err[i] = np.sqrt(((np.max(distances[n + i, :, 1])-np.min(distances[n+i, :, 1]))*0.0005)**2 + (0.00015/np.sqrt(60000))**2 + (0.001/np.sqrt(60000))**2)
        y_err[i] = 1/np.sqrt(3)*np.sqrt(1 + 0.5**2)
        
    y_err_ = np.zeros(b-a)
    for i in range(len(RMS_val)): 
        #y_err_[i] = np.sqrt(((np.max(distances[a + i, :, 1])-np.min(distances[a+i, :, 1]))*0.0005)**2 + (0.00015/np.sqrt(60000))**2 + (0.001/np.sqrt(60000))**2)
        y_err_[i] = 1/np.sqrt(3)*np.sqrt(1 + 0.5**2)

    x_err = np.zeros(len(v))
    for i in range(len(v)):
        if v[i] < 2:
            x_err[i] = (v[i]*0.05 + 0.1)/np.sqrt(3)
        else:
            x_err[i] = (v[i]*0.05 + 0.3)/np.sqrt(3)
            
    x_err_ = np.zeros(len(w))
    for i in range(len(w)):
        if w[i] < 2:
            x_err_[i] = (w[i]*0.05 + 0.1)/np.sqrt(3)
        else:
            x_err_[i] = (w[i]*0.05 + 0.3)/np.sqrt(3)
            
    #Here you can determine up to what index the fit shall be made
    odr = func.get_fit_quad(v[0:9], x_err[0:9], y_err[0:9], RMS_values_0[0:9], [p0[0]])
    odr_ = func.get_fit_quad(w[0:10], x_err_[0:10], y_err_[0:10], RMS_values_1[0:10], [p0[0]])
    popt = odr.beta
    popt_ = odr_.beta
    
    t = np.arange(0, 6.1, 0.1)
    t_ = np.arange(0, 6.8, 0.1)
    
    a, = odr.beta
    da, = odr.sd_beta
    chi2_rel_quad = odr.res_var

    label_quad = (
        "Polyimide:\n"
    + r"$x_{\mathrm{RMS}} = a_{\mathrm{quad}}\,v_{\mathrm{us}}^2$" + "\n"
    + fr"$a_{{\mathrm{{quad}}}} = {a:.1f} \pm 0.1\ \mathrm{{\mu m\,s^{{2}}\,m^{{-2}}}}$" + "\n"
    + fr"$\chi^2_\mathrm{{\nu}} = {chi2_rel_quad:.3f}$")
    
    b, = odr_.beta
    db, = odr_.sd_beta
    chi2_rel_quad_ = odr_.res_var


    label_quad_ = (
        "Carbon fibre:\n"
    + r"$x_{\mathrm{RMS}} = a_{\mathrm{quad}}\,v_{\mathrm{us}}^2$" + "\n"
    + fr"$a_{{\mathrm{{quad}}}} = {b:.1f} \pm 0.1\ \mathrm{{\mu m\,s^{{2}}\,m^{{-2}}}}$" + "\n"
    + fr"$\chi^2_\mathrm{{\nu}} = {chi2_rel_quad_:.3f}$")
    
    ax.scatter(v[:10], RMS_values_0[:10], marker="o", s = 15, color="#000000")
    ax.errorbar(v[:10], RMS_values_0[:10], xerr = x_err[:10], yerr = y_err[:10], fmt = "none", color="#000000", capsize = 5)
    ax.plot(t, func.fit_function_quad(odr.beta, t), linewidth = 2.0, color="#215CAF", label = label_quad)
    print(func.fit_function_quad(odr.beta, 5.6))
    print(func.fit_function_quad(odr_.beta, 5.6))
    
    ax.scatter(w[:11], RMS_values_1[:11], marker="o", s = 15, color="#000000")
    ax.errorbar(w[:11], RMS_values_1[:11], xerr = x_err_[:11], yerr = y_err_[:11], fmt = "none", color="#000000", capsize = 5)
    ax.plot(t_, func.fit_function_quad(odr_.beta, t_), linewidth = 2.0, color="#CA6CAE", label = label_quad_)
    
    ax.axhline(y=23, color='#575757', linestyle='--', linewidth=1)
    plt.grid()

    # Axis labels with font styling
    plt.xlabel("Mean upstream flow velocity (ms$^{-1}$)", fontsize=15, fontname="Times New Roman")
    plt.ylabel(r"RMS distance ($\mu$m)", fontsize=15, fontname="Times New Roman")

    # Tick styling
    plt.tick_params(axis="both", which="both", labelsize=8, length=4)

    # Remove axis spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Title and legend
    #plt.title("RMS vs Flow velocity", fontname="Times New Roman", fontsize=15, fontstyle='italic')
    #plt.legend(markerscale=1.5, bbox_to_anchor=(0.55, 0.45), borderpad=0.25, fontsize=10, labelspacing=1.5, frameon=True)
    
    legend = plt.legend(
    markerscale=1.5,
    bbox_to_anchor=(0.55, 0.45),
    borderpad=0.25,
    fontsize=10,
    labelspacing=1.5,
    frameon=True
    )
    
    frame = legend.get_frame()
    frame.set_edgecolor("black")   # black border
    frame.set_linewidth(0.5)       # thin border
    frame.set_facecolor("white")   # optional: white background
    
    plt.savefig("velocity-dependence.png", dpi = 300)
    plt.show()

    return

def plot_fit_HO(f, RMS, p0_HO):
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)
    f = f[5:]
    RMS = RMS[5:]
    f_fit = f[5:-1500]
    RMS_fit = RMS[5:-1500]
    # Get fit parameters for harmonic oscillator model
    popt = func.get_fit_HO(f_fit, RMS_fit, p0_HO)
    fit_func = func.resonance_curve_HO(f, *popt)
    response_func = (np.abs(fit_func/popt[0]))
    
    # Scatter plot of measured data (no lines between points to avoid misinterpretation)
    ax.scatter(f, RMS, marker = "o", s = 2, color = "#426A5A", label = "Measured Data")
    
    # Plot the model fit using the fitted parameters
    ax.plot(f, fit_func, color = "#61615F", label = "HO-Model Fit")
    ax.plot(f, (RMS/response_func)**2, color = "#61615F", label = "PSD")
    
    # Set both axes to logarithmic scale
    ax.set_xscale("log")
    ax.set_yscale("log")
    
    # Set specific x-axis ticks for clarity
    ax.set_xticks([10,100])
    ax.set_ylim(10**(-4),20)
    # Add grid to the plot
    plt.grid()
    
    # Label axes with appropriate units and font
    plt.xlabel("Frequency in Hz", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("RMS displacement in $\mu$m", fontsize = 15, fontname ="Times New Roman")
    
    # Adjust axis tick parameters
    plt.tick_params(axis="both", which = "both", labelsize = 8, length = 4)
    
    # Set global plot resolution (redundant due to initial dpi but ensures sharpness)
    plt.rcParams["figure.dpi"] = 360
    
    # Remove plot border (top, right, etc.)
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    
    plt.title("Fitted RMS Displacement", fontname ="Times New Roman", fontsize = 15, fontstyle='italic')
    
    # Add and format legend
    plt.legend(markerscale=1.5, bbox_to_anchor=(0.98, 0.95), borderpad=0.25, frameon=False, fontsize = 10)
    
    
    # Display the plot
    plt.show()
    
    return

#plots upstream vs downstream velocity
def velocities(v1, v2, p0):
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)
    
    
    x_err = np.zeros(len(v1))
    for i in range(len(v1)):
        if v1[i] < 2:
            x_err[i] = (v1[i]*0.05 + 0.15)/np.sqrt(3)
        else:
            x_err[i] = (v1[i]*0.05 + 0.3)/np.sqrt(3)
    
    y_err = np.zeros(len(v2))
    for i in range(len(v2)):
        if v2[i] < 2:
            y_err[i] = (v2[i]*0.05 + 0.15)/np.sqrt(3)
        else:
            y_err[i] = (v2[i]*0.05 + 0.3)/np.sqrt(3)
    
    
    odr = func.get_lin(v1, x_err, v2, y_err, p0)
    popt = odr.beta
    
    v = np.arange(0,9,0.1)
    
    y_fit = func.fit_lin(odr.beta, v)
    
    
    a = popt[0]          # parameter value
    da = odr.sd_beta[0]  # parameter uncertainty from ODR
    chi2_rel = odr.res_var  # relative chi² from ODR

    label_ = (
    r"$v_{\mathrm{ds}} = a_{\mathrm{lin}}\,v_{\mathrm{us}}$" + "\n"
    + fr"$a_{{\mathrm{{lin}}}} = {a:.1f} \pm 0.1$" + "\n"
    + fr"$\chi^2_\mathrm{{\nu}} = {chi2_rel:.3f}$")
    
    ax.scatter(v1,v2, color = "#000000", marker = "o", s = 10)
    ax.errorbar(v1, v2, xerr = x_err, yerr = y_err, fmt = "none", color="#000000", capsize = 4)
    ax.plot(v, y_fit, color="#215CAF", lw=2.0, label = label_)
    
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    plt.tick_params(axis="both", which = "both", labelsize = 8, length = 4)
    plt.rcParams["figure.dpi"] = 360
    
    plt.xlabel("Mean upstream velocity (ms$^{-1}$)", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("Mean downstream velocity (ms$^{-1}$)", fontsize = 15, fontname ="Times New Roman")
    
    #plt.legend(markerscale=1.5, bbox_to_anchor=(0.4, 0.87), borderpad=0.25, fontsize = 10)
    legend = plt.legend(
    markerscale=1.5,
    bbox_to_anchor=(0.4, 0.8),
    borderpad=0.25,
    fontsize=10,
    labelspacing=1.5,
    frameon=True
    )
    
    frame = legend.get_frame()
    frame.set_edgecolor("black")   # black border
    frame.set_linewidth(0.5)       # thin border
    frame.set_facecolor("white")   # optional: white background
    
    #plt.title("Velocity comparison", fontname ="Times New Roman", fontsize = 15, fontstyle='italic')
    plt.grid()
    plt.savefig("velocity-comparison.png", dpi = 300)
    plt.show()
    return

