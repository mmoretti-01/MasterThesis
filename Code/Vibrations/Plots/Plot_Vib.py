# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 15:28:33 2025

@author: moretti
"""

import os
import numpy as np
import Functions_Table.Functions_Table_Linear as lin
import Functions_Table.Functions_Table_NL as nl
from matplotlib import pyplot as plt
from collections import OrderedDict




Length, data = lin.Length_Data() 

code_dir = os.path.dirname(os.path.realpath(__file__))

Pic = os.path.join(code_dir, "..", "..", "..", "Pictures")


""" ---------- Parameter Explanation ---------- """

#m and n determine which measurement is being analyzed  
#y and z determine which sensor data is being used  
#p0 defines the initial parameter values for the fitting procedure



""" ---------- Plots ---------- """


#Oxford colours https://communications.admin.ox.ac.uk/communications-resources/visual-identity/identity-guidelines/colours
def plot_fit(m, p0, y):
    
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)
    label_ = "BHO-Model Fit"
    
    if len(p0)/3 == 1:
        popt_ = lin.get_fit_HO_new(m, p0, y)[0]
        popt, pcov = lin.get_fit_HO_new(m, p0, y)
        y_fit = lin.resonance_curve_HO(data[:Length[m],0,m], *popt)
        chi2 = np.sum(((data[:Length[m],y,m] - y_fit) / data[:Length[m],-1,m]) ** 2)
        dof = len(data[:Length[m],0,m]) - len(popt)  # N - number of parameters
        print(chi2)
        chi2_red = chi2 / dof
        
        fit = lin.resonance_curve_HO(data[:Length[m],0,m], *popt_)
        label_ = (
            f"A = {popt[0]:.2f} ± {0.01}\n"
            f"f₀ = {popt[1]:.2f} ± {np.sqrt(pcov[1][1]):.2f} Hz\n"
            f"Q = {popt[2]:.2f} ± {np.sqrt(pcov[2][2]):.2f}\n"
            f"$\\chi_\\nu^2$ = {chi2_red:.2f}")
    
    elif len(p0)/3 == 2:
        popt = nl.get_fit_BB_2(m, p0, y)
        fit = nl.resonance_curve_BB_2(data[:Length[m],0,m], *popt)
    
    elif len(p0)/3 == 3:
        popt = nl.get_fit_BB_3(m, p0, y)
        fit = nl.resonance_curve_BB_3(data[:Length[m],0,m], *popt)
        
    elif len(p0)/3 == 4:
        popt = nl.get_fit_BB_4(m, p0, y)
        fit = nl.resonance_curve_BB_4(data[:Length[m],0,m], *popt)
        
    elif len(p0)/3 == 5:
        popt, pcov = nl.get_fit_BB_5(m, p0, y)
        fit = nl.resonance_curve_BB_5(data[:Length[m],0,m], *popt)
        chi2 = np.sum(((data[:Length[m],y,m] - fit) / data[:Length[m],-1,m]) ** 2) 
        dof = len(data[:Length[m],0,m]) - len(popt)
        print(chi2)
        chi2_red = chi2 / dof
        label_ = ("5th order fit:\n"
            f"$\\chi_\\nu^2$ = {chi2_red:.2f}")
        
    else:
        print("wrong initial guess format")
        return 
    
    print(r"Fit parameter:", popt)
    
    y_min = np.abs(data[:Length[m],y,m]) - data[:Length[m],-1,m]
    y_max = np.abs(data[:Length[m],y,m]) + data[:Length[m],-1,m]
    
    # Scatter plot of measured data (no connecting lines to avoid misleading visuals)
    ax.scatter(data[:Length[m],0,m], np.abs(data[:Length[m],y,m]), marker = "o", s = 2, color = "#FFB81C", label = "Measured data", zorder = 1)
    
    #ax.plot(data[:Length[m],0,m], data[:Length[m],-1,m], linewidth = 2.0, color = "#89827A", label = "Uncertainty", alpha = 1, zorder = 0)
    ax.fill_between(data[:Length[m],0,m], y_min, y_max, color = "#D9D8D6", label = "Uncertainty", alpha = 1, zorder = 0)
    
    # Plot the 2D model fit curve using fitted parameters
    ax.plot(data[:Length[m],0,m], fit, linewidth = 2.0, color = "#002147", label = label_, zorder = 2)
    
    
    # Set axes to logarithmic scale for better visualization of frequency response
    ax.set_xscale("log")
    ax.set_yscale("log")
    
    # Define specific x-axis ticks and y-axis limits
    ax.set_xticks([10,100])
    ax.set_ylim(10**(-2),10**2)
    ax.set_xlim(12,256)
    
    # Enable plot grid
    plt.grid()
    
    # Label the axes
    plt.xlabel("Frequency (Hz)", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("Dimensionless response function", fontsize = 15, fontname ="Times New Roman")

    # Adjust tick label size and length
    plt.tick_params(axis="both", which = "both", labelsize = 8, length = 4 )

    # Increase global plot sharpness
    plt.rcParams["figure.dpi"] = 360

    # Remove surrounding box (spines) from the plot
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Define save path and export figure
    Pict = os.path.join(Pic, "Response Function Fit.png")    
    
    #plt.title("Response Function Carbon Fibre", fontname ="Times New Roman", fontsize = 15, fontstyle='italic')
    
    # Add legend and display the plot
    #plt.legend(markerscale=3, bbox_to_anchor=(0.69, 0.7), borderpad=0.25, fontsize = 10)
    
    legend = plt.legend(
    markerscale=3,
    bbox_to_anchor=(0.66, 0.65),
    borderpad=0.25,
    fontsize=10,
    labelspacing=0.5,
    frameon=True
    )
    
    frame = legend.get_frame()
    frame.set_edgecolor("black")   # black border
    frame.set_linewidth(0.5)       # thin border
    frame.set_facecolor("white")   # optional: white background
    
    plt.savefig(Pict, dpi = 300)
    plt.show()
    return

def two_col_comp(m, n, y, z):
    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (6,4), dpi = 300)
    
    y_min_m = np.abs(data[:Length[m],y,m]) - data[:Length[m],-1,m]
    y_max_m = np.abs(data[:Length[m],y,m]) + data[:Length[m],-1,m]
    
    y_min_n = np.abs(data[:Length[n],z,n]) - data[:Length[n],-1,n]
    y_max_n = np.abs(data[:Length[n],z,n]) + data[:Length[n],-1,n]
    
    
    #/np.sqrt(3) for Kapton
    
    
    ax[0].scatter(data[:Length[m],0,m],np.abs(data[:Length[m],y,m]), marker = "D", s = 2, color = "#002147", label="Carbon-fibre ladder")
    ax[0].fill_between(data[:Length[m],0,m], y_min_m, y_max_m, color='#002147', alpha=0.3)
    #ax[0].plot(data[:Length[m],0,m], data[:Length[m],-1,m], color='#002147', alpha=0.3)
    ax[0].set_xscale("log")
    ax[0].set_yscale("log")
    ax[0].set_ylim(1e-3,1e2)
    ax[0].grid()
    ax[0].set_yticks([1e-3, 1e-2, 1e-1, 1, 10, 100])
    ax[0].tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
    ax[0].axvline(x=41.5, color="black", linestyle="--", linewidth=1, alpha = 0.5)
    ax[0].axvline(x=210, color="black", linestyle="--", linewidth=1, alpha = 0.5)
    
    
    ax[1].scatter(data[:Length[n],0,n],np.abs(data[:Length[n],z,n]), marker = "D", s = 2, color = "#FFB81C", label="Polyimide ladder")
    ax[1].fill_between(data[:Length[n],0,n], y_min_n, y_max_n, color='#002147', alpha=0.3, label = "Uncertainty")
    #ax[1].plot(data[:Length[n],0,n], data[:Length[n],-1,n], color='#002147', alpha=0.3)
    ax[1].set_xscale("log")
    ax[1].set_yscale("log")
    ax[1].set_ylim(1e-3, 1e2)
    ax[1].grid()
    ax[1].tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
    ax[1].axvline(x=19.7, color="black", linestyle="--", linewidth=1, alpha = 0.5)
    ax[1].axvline(x=85, color="black", linestyle="--", linewidth=1, alpha = 0.5)
    ax[1].axvline(x=220, color="black", linestyle="--", linewidth=1, alpha = 0.5)
    
        
    
    fig.supylabel("RMS displacement ($\mu$m)", fontsize=15, fontname="Times New Roman")
    fig.supxlabel("Frequency (Hz)", fontsize=15, fontname="Times New Roman")
    #fig.suptitle("RMS displacements of the table", fontname="Times New Roman", fontsize=20, fontstyle='italic')
    
    for spine in ax[0].spines.values():
        spine.set_visible(False)
    for spine in ax[1].spines.values():
        spine.set_visible(False)
    
        
    handles = []
    labels = []
    for a in ax.flat:
        h, l = a.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(l)

    # Remove duplicates while keeping order
    unique = dict(zip(labels, handles))
    #fig.legend(unique.values(), unique.keys(),
           #loc='upper center', bbox_to_anchor=(0.85, 0.90), ncol=1, fontsize=10, borderpad=0.25, frameon=True, markerscale=5)
           
           
    legend = fig.legend(
    unique.values(), unique.keys(),
    loc='upper center',
    bbox_to_anchor=(0.80, 0.90),
    ncol=1,
    fontsize=10,
    borderpad=0.25,
    frameon=True,
    markerscale=3)
    
    frame = legend.get_frame()
    frame.set_edgecolor("black")   # black border
    frame.set_linewidth(0.5)       # thin border
    frame.set_facecolor("white")   # optional: white background
    
    
    
    Pict = os.path.join(Pic, "two_col_comp.pdf")    
    plt.savefig(Pict)
    plt.show()
    return 



def three_col_comp(m, n, k, y, z, w):
   fig, axs = plt.subplots(ncols=4, nrows=2, figsize=(6, 4), gridspec_kw={'wspace': 0.4})
   gs = axs[0, 0].get_gridspec()
   
   y_min_m = np.abs(data[:Length[m],y,m]) - data[:Length[m],-1,m]
   y_max_m = np.abs(data[:Length[m],y,m]) + data[:Length[m],-1,m]
   
   y_min_n = np.abs(data[:Length[n],y,n]) - data[:Length[n],-1,n]
   y_max_n = np.abs(data[:Length[n],y,n]) + data[:Length[n],-1,n]
   
   y_min_k = np.abs(data[:Length[k],y,k]) - data[:Length[k],-1,k]
   y_max_k = np.abs(data[:Length[k],y,k]) + data[:Length[k],-1,k]
   
   
   for ax in axs.ravel():
       ax.remove()
       
   ax1 = fig.add_subplot(gs[0, 1:3])
   ax1.scatter(data[:Length[m],0,m],np.abs(data[:Length[m],y,m]), marker = "D", s = 2, color = "#002147", label="Centre")
   ax1.fill_between(data[:Length[m],0,m], y_min_m, y_max_m, color='#002147', alpha=0.3)
   #ax1.plot(data[:Length[m],0,m], data[:Length[m],-1,m], color='#002147', alpha=0.3)
   ax1.set_xscale("log")
   ax1.set_yscale("log")
   ax1.set_ylim(1e-3, 1e2)
   ax1.grid()
   ax1.set_yticks([1e-2, 1e-1, 1, 10, 100])
   ax1.tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
   
   ax2 = fig.add_subplot(gs[1, :2])
   ax2.scatter(data[:Length[n],0,n],np.abs(data[:Length[n],z,n]), marker = "D", s = 2, color = "#5A5F66", label="5cm from centre")
   ax2.fill_between(data[:Length[n],0,n], y_min_n, y_max_n, color='#002147', alpha=0.3)
   #ax2.plot(data[:Length[n],0,n], data[:Length[n],-1,n], color='#002147', alpha=0.3)
   ax2.set_xscale("log")
   ax2.set_yscale("log")
   ax2.set_ylim(1e-3, 1e2)
   ax2.grid()
   ax2.tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
   
   ax3 = fig.add_subplot(gs[1, 2:])
   ax3.scatter(data[:Length[k],0,k],np.abs(data[:Length[k],z,k]), marker = "D", s = 2, color = "#496F9D", label="9cm from centre")
   ax3.fill_between(data[:Length[k],0,k], y_min_k, y_max_k, color='#002147', alpha=0.3)
   #ax3.plot(data[:Length[k],0,k], data[:Length[k],-1,k], color='#002147', alpha=0.3)
   ax3.set_xscale("log")
   ax3.set_yscale("log")
   ax3.set_ylim(1e-3, 1e2)
   ax3.grid()
   ax3.tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
   
   for spine in ax1.spines.values():
       spine.set_visible(False)
   for spine in ax2.spines.values():
       spine.set_visible(False)
   for spine in ax3.spines.values():
       spine.set_visible(False)
   
       
   fig.supylabel("RMS displacement in $\mu$m", fontsize=25, fontname="Times New Roman")
   fig.supxlabel("Frequency in Hz", fontsize=25, fontname="Times New Roman")
   fig.suptitle("RMS Displacements of Kapton Design", fontname="Times New Roman", fontsize=25, fontstyle='italic')   
   
   handles = []
   labels = []
   for a in (ax1, ax2, ax3):
       h, l = a.get_legend_handles_labels()
       handles.extend(h)
       labels.extend(l)

   # Remove duplicates while keeping order
   unique = dict(zip(labels, handles))
   fig.legend(unique.values(), unique.keys(),
          loc='upper center', bbox_to_anchor=(0.80, 0.87), ncol=1, fontsize=15, borderpad=0.25, frameon=True, markerscale=5)
   
   Pict = os.path.join(Pic, "two_col_comp.pdf")    
   plt.savefig(Pict)
       
   plt.show()
   return

def four_col_comp(m, n, k, l, y, z):
    fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize = (6,4), dpi = 300)
    
    y_min_m = np.abs(data[:Length[m],y,m]) - data[:Length[m],-1,m]
    y_max_m = np.abs(data[:Length[m],y,m]) + data[:Length[m],-1,m]
    
    y_min_n = np.abs(data[:Length[n],y,n]) - data[:Length[n],-1,n]
    y_max_n = np.abs(data[:Length[n],y,n]) + data[:Length[n],-1,n]
    
    y_min_k = np.abs(data[:Length[k],y,k]) - data[:Length[k],-1,k]
    y_max_k = np.abs(data[:Length[k],y,k]) + data[:Length[k],-1,k]
    
    y_min_l = np.abs(data[:Length[l],y,l]) - data[:Length[l],-1,l]
    y_max_l = np.abs(data[:Length[l],y,l]) + data[:Length[l],-1,l]
    
    ax[0,0].scatter(data[:Length[m],0,m],np.abs(data[:Length[m],y,m]), marker = "D", s = 2, color = "#002147", label="3cm from centre")
    ax[0,0].fill_between(data[:Length[m],0,m], y_min_m, y_max_m, color='#002147', alpha=0.3)
    #ax[0,0].plot(data[:Length[m],0,m], data[:Length[m],-1,m], color='#002147', alpha=0.3)
    ax[0,0].set_xscale("log")
    ax[0,0].set_yscale("log")
    ax[0,0].set_ylim(1e-3, 1e2)
    ax[0,0].grid()
    ax[0,0].set_yticks([1e-2, 1e-1, 1, 10, 100])
    ax[0,0].tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
    
    
    ax[0,1].scatter(data[:Length[n],0,n],np.abs(data[:Length[n],z,n]), marker = "D", s = 2, color = "#FFB81C", label="6cm from centre")
    ax[0,1].fill_between(data[:Length[n],0,n], y_min_n, y_max_n, color='#002147', alpha=0.3)
    #ax[0,1].plot(data[:Length[n],0,n], data[:Length[n],-1,n], color='#002147', alpha=0.3)
    ax[0,1].set_xscale("log")
    ax[0,1].set_yscale("log")
    ax[0,1].set_ylim(1e-3, 1e2)
    ax[0,1].grid()
    ax[0,1].tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
    
    
    ax[1,0].scatter(data[:Length[k],0,k],np.abs(data[:Length[k],z,k]), marker = "D", s = 2, color = "#FE615A", label="9cm from centre")
    ax[1,0].fill_between(data[:Length[k],0,k], y_min_k, y_max_k, color='#002147', alpha=0.3)
    #ax[1,0].plot(data[:Length[k],0,k], data[:Length[k],-1,k], color='#002147', alpha=0.3)
    ax[1,0].set_xscale("log")
    ax[1,0].set_yscale("log")
    ax[1,0].set_ylim(1e-3, 1e2)
    ax[1,0].grid()
    ax[1,0].tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
    
    
    ax[1,1].scatter(data[:Length[l],0,l],np.abs(data[:Length[l],z,l]), marker = "D", s = 2, color = "#007B4B", label="12cm from centre")
    ax[1,1].fill_between(data[:Length[l],0,l], y_min_l, y_max_l, color='#002147', alpha=0.3, label='Uncertainty')
    #ax[1,1].plot(data[:Length[l],0,l], data[:Length[l],-1,l], color='#002147', alpha=0.3, label='Uncertainty')
    ax[1,1].set_xscale("log")
    ax[1,1].set_yscale("log")
    ax[1,1].set_ylim(1e-3, 1e2)
    ax[1,1].grid()
    ax[1,1].tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
        
    
    fig.supylabel("RMS displacement ($\mu$m)", fontsize=15, fontname="Times New Roman")
    fig.supxlabel("Frequency (Hz)", fontsize=15, fontname="Times New Roman")
    #fig.suptitle("RMS Displacements of Carbon Design", fontname="Times New Roman", fontsize=20, fontstyle='italic')
    
    for spine in ax[0,0].spines.values():
        spine.set_visible(False)
    for spine in ax[0,1].spines.values():
        spine.set_visible(False)
    for spine in ax[1,0].spines.values():
        spine.set_visible(False)
    for spine in ax[1,1].spines.values():
        spine.set_visible(False)
        
    handles = []
    labels = []
    for a in ax.flat:
        h, l = a.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(l)

    # Remove duplicates while keeping order
    unique = dict(zip(labels, handles))
    #fig.legend(unique.values(), unique.keys(),
           #loc='upper center', bbox_to_anchor=(0.85, 0.90), ncol=1, fontsize=10, borderpad=0.25, frameon=True, markerscale=5)
           
           
    legend = fig.legend(
    unique.values(), unique.keys(),
    loc='upper center',
    bbox_to_anchor=(0.85, 1),
    ncol=1,
    fontsize=10,
    borderpad=0.25,
    frameon=True,
    markerscale=3)
    
    frame = legend.get_frame()
    frame.set_edgecolor("black")   # black border
    frame.set_linewidth(0.5)       # thin border
    frame.set_facecolor("white")   # optional: white background
    
    
    Pict = os.path.join(Pic, "two_col_comp.pdf")    
    plt.savefig(Pict)
    plt.show()
    return 

def single_pic_comp(m, n, y, z):
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)

    ax.scatter(data[:Length[m],0,m],np.abs(data[:Length[m],y,m]), marker = "o", s = 2, color = "#994636", label="m")
    ax.scatter(data[:Length[n],0,n],np.abs(data[:Length[n],z,n]), marker = "o", s = 2, color = "#002147", label="n")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([10,100])
    plt.xlim([8,256])
    
    plt.grid()
    
    plt.xlabel("Frequency in Hz", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("RMS displacement in $\mu$m", fontsize = 15, fontname ="Times New Roman")
    
    plt.tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
    
    plt.rcParams["figure.dpi"] = 360
    
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    plt.title("RMS Displacement Comparison", fontname ="Times New Roman", fontsize = 15, fontstyle='italic')
    Pict = os.path.join(Pic, "single_pic_comp")    
    plt.savefig(Pict, dpi=360)
    plt.legend()
    plt.show()
    return

def single_pic(m,y):
    
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)
    
    #off, std = uncertainties()
    
    y_min = np.abs(data[:Length[m],y,m]) - data[:Length[m],-1,m]
    y_max = np.abs(data[:Length[m],y,m]) + data[:Length[m],-1,m]
    
    ax.scatter(data[:Length[m],0,m],np.abs(data[:Length[m],y,m]), marker = "o", s = 2, color = "#211D1C", label = "Measured data")
    #ax.errorbar(data[:Length[m],x,m], np.abs(data[:Length[m],y,m]), yerr = off, fmt='none', ecolor='#994636', capsize=5, label='Data with error')
    ax.fill_between(data[:Length[m],0,m], y_min, y_max, color='#002147', alpha=0.3, label='Uncertainty')
    
    #ax.scatter(data[:Length[m],x,m], std, color = "#002147", alpha = 0.3, marker = "o", s = 2, label="Uncertainty")
    
    
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([10,100])

    ax.set_ylim(8*10**(-3),10**2)
    ax.set_xlim(12,256)

    plt.grid()
    
    plt.xlabel("Frequency (Hz)", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("RMS displacement ($\mu$m)", fontsize = 15, fontname ="Times New Roman")
    
    plt.tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
    plt.rcParams["figure.dpi"] = 360
    
    for spine in ax.spines.values():
        spine.set_visible(False)

    Pict = os.path.join(Pic, "single_pic.png")    
    #plt.title("Table RMS Displacement", fontname ="Times New Roman", fontsize = 15, fontstyle='italic')
    #plt.legend(markerscale=3, bbox_to_anchor=(1.05, 0.95), borderpad=0.25, frameon=False, fontsize = 10)
    
    legend = plt.legend(
    markerscale=3,
    bbox_to_anchor=(1, 0.95),
    borderpad=0.25,
    fontsize=10,
    labelspacing=0.5,
    frameon=True
    )
    
    frame = legend.get_frame()
    frame.set_edgecolor("black")   # black border
    frame.set_linewidth(0.5)       # thin border
    frame.set_facecolor("white")   # optional: white background
    
    plt.savefig(Pict, dpi = 300)
    plt.show()
    return

def tension_dep(p0):
    
    T = [32, 56, 75, 82, 87]
    L = [0, 0.25, 0.5, 0.75, 1]
    x = np.linspace(0,1.1,100)
    x_err = [0.1, np.sqrt(2)*0.1, np.sqrt(2)*0.1, np.sqrt(2)*0.1, np.sqrt(2)*0.1]
    
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)
    
    odr_run = lin.get_fit_tension(L, x_err, T, p0)
    A_fit, B_fit = odr_run.beta
    A_err, B_err = odr_run.sd_beta
    chi2_red = odr_run.res_var
    
    fit = lin.tension(odr_run.beta, x)
    
    #ax.scatter(L, T, marker = "o", s = 2, color = "#211D1C")
    ax.plot(x, fit, color = "#FFB81C", linestyle = "--", label=(r"Fit: $A\sqrt{x} + f_0$"
                   f"\nA = {A_fit:.0f} ± {A_err:.0f} Hz/√mm"
                   f"\n$f_0$ = {B_fit:.0f} ± {B_err:.0f} Hz"
                   f"\n$\\chi_\\nu^2$ = {chi2_red:.3f}"))
    plt.errorbar(L,T, xerr = x_err, yerr = 1, fmt='none', ecolor="#002147")
    
    
    plt.xlabel("Elongation (mm)", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("First mode frequency (Hz)", fontsize = 15, fontname ="Times New Roman")

    # Adjust tick label size and length
    plt.tick_params(axis="both", which = "both", labelsize = 8, length = 4 )

    # Increase global plot sharpness
    plt.rcParams["figure.dpi"] = 360

    # Remove surrounding box (spines) from the plot
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Define save path and export figure
    Pict = os.path.join(Pic, "Response Function Fit.pdf")    
    
    #plt.title("Tension dependency of the first mode", fontname ="Times New Roman", fontsize = 15, fontstyle='italic')
    
    # Add legend and display the plot
    #plt.legend(markerscale=3, bbox_to_anchor=(1, 0.7), borderpad=0.25, fontsize = 10)
    
    legend = plt.legend(
    markerscale=3,
    bbox_to_anchor=(0.54, 0.65),
    borderpad=0.25,
    fontsize=10,
    labelspacing=0.5,
    frameon=True
    )
    
    frame = legend.get_frame()
    frame.set_edgecolor("black")   # black border
    frame.set_linewidth(0.5)       # thin border
    frame.set_facecolor("white")   # optional: white background
    
    plt.grid()
    plt.savefig("Tension dependency.png")
    plt.show()
    return
    

