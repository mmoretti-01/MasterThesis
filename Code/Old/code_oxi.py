# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib 
from matplotlib import pyplot as plt
import scipy as sp
from scipy.optimize import curve_fit
import os
from scipy.integrate import quad
from scipy.integrate import quad_vec
from scipy.signal import welch

""" ---------- Initialize Variables ---------- """

#Nr of distinct measurements
Nr = 16

#This array will contain the Files after readout
Doc = []
Doc_a = []

""" ---------- Read Folders  ---------- """

#Reads the Folder, sorts it according to the modification Date and appends it to the Doc array
#Dateien corresponds to the Files in the Folder, the lambda function sorts the document paths according to modification
#os.path.join gives the path to the documents, it is a function that is compatible with different platforms
def read_folder(Folder):
    Dateien = os.listdir(Folder)
    Dateien.sort()
    Di0 = len(Dateien)
    for j in range(Di0):
        Doc.append(open(os.path.join(Folder,Dateien[j]),"r"))
    return 0

Folder = "/Users/main/Desktop/Mu3e/Laserdisp/"
read_folder(Folder)

#If single File needed, use Doc.append(open('C:/Users/moretti/Desktop/data/'+'Laserdisp 04-03-2025 14-08-56.dat',"r"))

Doc_a.append(open('/Users/main/Desktop/DatasetA1_Bracket_L.txt',"r"))


""" ---------- Copy Data into Array  ---------- """

#700 is way to big but Length will take care of it.
#Nr referes to the document number
data = np.zeros([700,72,Nr])


#Length gives the length of the excel columns, corresponds to the number of lines in the excel sheet
Length = []
Length_a = []

#The following copies the data from the files in Doc into the array "data"
for i in range(Nr):
    Lines = Doc[i].readlines()[2:]
    l = len(Lines)
    Length.append(l)
    b = 0
    for line in Lines:
        numbers =[float(values) for values in line.split()]
        inumbers = numbers[0:72]
        data[b,:,i] = inumbers
        b = b + 1

Lines_a = Doc_a[0].readlines()[50:]
l = len(Lines_a)
Length_a.append(l)
data_a = np.zeros([Length_a[0],2])
b = 0
for line_a in Lines_a:
    for values_a in line_a.split():
        numbers_a =[float(values_a) for values_a in line_a.split()]
    inumbers_a = numbers_a[0:2]
    data_a[b,:] = inumbers_a
    b = b + 1
      
""" ---------- Functions ---------- """

#Determines Freq of highest value AFTER first n measurements
def H_max(m,n,y):
    a = np.max(np.abs(data[n:Length[m],y,m]))
    for i in range(len(data[:Length[m],0,m])):
        if np.abs(data[i,y,m]) == a:
            return data[i,0,m]

#Gives absolute difference between the frequencies of the peaks for two measurements
def H_achange(m,n,p,y):
    return np.abs(H_max(n,p,y) - H_max(m,p,y))
        
#Determines highest average displacement value AFTER first 10 measurements
def D_max(m,n,y):
    return np.max(np.abs(data[n:Length[m],y,m]))

#Gives the relative change of the peak Displacement with respect to the first measurements value        
def D_rchange(m,n,p,y):
    return np.abs((D_max(n,p,y)-D_max(m,p,y))/D_max(m,p,y))      
      
#This function corresponds to a modified 1D Model function
def resonance_curve_m(f, A, f0, Q, S):
    return f**(S)*A/(np.sqrt((1-(f/f0)**2)**2 + (1/Q)**2 * (f/f0)**2))

#This function corresponds to a 1D Model function
def resonance_curve_1D(f, A, f0, Q):
    return A/(np.sqrt((1-(f/f0)**2)**2 + (1/Q)**2 * (f/f0)**2))

#This function corresponds to a 2D Model function
def resonance_curve_2D(f, A_1, f0_1, Q_1, A_2, f0_2, Q_2, A_3, f0_3, Q_3, A_4, f0_4, Q_4):
    term_1 = A_1/(np.sqrt((1-(f/f0_1)**2)**2 + (1/Q_1)**2 * (f/f0_1)**2))
    term_2 = A_2/(np.sqrt((1-(f/f0_2)**2)**2 + (1/Q_2)**2 * (f/f0_2)**2))
    term_3 = A_3/(np.sqrt((1-(f/f0_3)**2)**2 + (1/Q_3)**2 * (f/f0_3)**2))
    term_4 = A_4/(np.sqrt((1-(f/f0_4)**2)**2 + (1/Q_4)**2 * (f/f0_4)**2))
    return term_1 + term_2 + term_3 + term_4

def resonance_curve_2D_normalised(f, A_1, f0_1, Q_1, A_2, f0_2, Q_2, A_3, f0_3, Q_3, A_4, f0_4, Q_4):
    term_1 = 1/(np.sqrt((1-(f/f0_1)**2)**2 + (1/Q_1)**2 * (f/f0_1)**2))
    term_2 = 1/(np.sqrt((1-(f/f0_2)**2)**2 + (1/Q_2)**2 * (f/f0_2)**2))
    term_3 = 1/(np.sqrt((1-(f/f0_3)**2)**2 + (1/Q_3)**2 * (f/f0_3)**2))
    term_4 = 1/(np.sqrt((1-(f/f0_4)**2)**2 + (1/Q_4)**2 * (f/f0_4)**2))
    return (term_1 + term_2 + term_3 + term_4)/4

def resonance_curve_2D_3(f, A_1, f0_1, Q_1, A_2, f0_2, Q_2, A_3, f0_3, Q_3):
    term_1 = A_1/(np.sqrt((1-(f/f0_1)**2)**2 + (1/Q_1)**2 * (f/f0_1)**2))
    term_2 = A_2/(np.sqrt((1-(f/f0_2)**2)**2 + (1/Q_2)**2 * (f/f0_2)**2))
    term_3 = A_3/(np.sqrt((1-(f/f0_3)**2)**2 + (1/Q_3)**2 * (f/f0_3)**2))
    return term_1 + term_2 + term_3

def ASD_fit(f,A,f0,Q,B,C,D):
    return f**(B)*A/(np.sqrt((1-(f/f0)**2)**2 + (1/Q)**2 * (f/f0)**2))*C/((f-f0)**2 + C**2)*D

#Same function as above, but to 5th order
def resonance_curve_2D_5(f, A_1, f0_1, Q_1, A_2, f0_2, Q_2, A_3, f0_3, Q_3, A_4, f0_4, Q_4, A_5, f0_5, Q_5):
    term_1 = A_1/(np.sqrt((1-(f/f0_1)**2)**2 + (1/Q_1)**2 * (f/f0_1)**2))
    term_2 = A_2/(np.sqrt((1-(f/f0_2)**2)**2 + (1/Q_2)**2 * (f/f0_2)**2))
    term_3 = A_3/(np.sqrt((1-(f/f0_3)**2)**2 + (1/Q_3)**2 * (f/f0_3)**2))
    term_4 = A_4/(np.sqrt((1-(f/f0_4)**2)**2 + (1/Q_4)**2 * (f/f0_4)**2))
    term_5 = A_5/(np.sqrt((1-(f/f0_5)**2)**2 + (1/Q_5)**2 * (f/f0_5)**2))
    return term_1 + term_2 + term_3 + term_4 + term_5

#m for modified. Given an array of 4 initial values p0 and which data we should consider this function returns the ideal fit parameters for the unphysical fit
def get_fit_m(m,p0):
    popt, pcov = curve_fit(resonance_curve_m, data[:Length[m],x,m], np.abs(data[:Length[m],y,m]), p0, maxfev=1000)
    return popt

#Given an array of 3 initial values p0 and which data we should consider this function returns the ideal fit parameters for the unphysical fit
def get_fit_1D(m,p0):
    popt, pcov = curve_fit(resonance_curve_1D, data[:Length[m],x,m], np.abs(data[:Length[m],y,m]), p0, maxfev=1000)
    return popt

#Same as above but for the Bernoulli 4th order case
def get_fit_2D(m,p0):
    popt, pcov = curve_fit(resonance_curve_2D, data[:Length[m],x,m], np.abs(data[:Length[m],y,m]), p0, maxfev=100000)
    return popt

#Same as above but for the Bernoulli 5th order case
def get_fit_2D_5(m,p0):
    popt, pcov = curve_fit(resonance_curve_2D_5, data[:Length[m],x,m], np.abs(data[:Length[m],y,m]), p0, maxfev=100000)
    return popt

#From here on everything regarding ASD/PSD integratio

#Gives the Displacement as a function of frequencz of the table in mikrons
def Table(m):
    table = data[:Length[m],7,m] - data[:Length[m],43,m]
    return np.abs(table)

def Table_PSD(m):
    a = Table(m)*10**(-6)
    a = a**2
    PSD = a/data[:Length[m],x,m]
    return PSD

#Determines the ASD of the table in m^2/s^4 *1/Hz
def Table_ASD(m):
    PSD = Table_PSD(m)
    ASD = PSD * (2 * np.pi * data[:Length[m],x,m])**4
    return ASD

#Exponential fit used for the ASD
def expon(f,A,B):
    return A*(f**B)

#Gets the parameters for the exponential fit
def get_fit_expon(m,p0):
    popt, pcov = curve_fit(expon, data[:Length[m],x,m], Table_ASD(m), p0, maxfev=100000)
    return popt

#Integrates the object esponse to vibration squared times the ASD and takes the square root. It also devides by freq. so that it outputs the RMS displacement
#The function uses the 1D fit to the average displacement graph and the ASD from the table that is fitted using the expo function
def integrate_1D(m,p0_1D):
    popt = get_fit_1D(m,p0_1D)
    def integrand(f):
        return (10**(6)*(resonance_curve_1D(f,*popt)/popt[0])**2)/(2*np.pi*f)**4
    integral_result, error_estimate = quad_vec(integrand,8,256)     
    a = np.sqrt(10**(6)*np.abs(popt[2])/(32*(np.pi*popt[1])**3))
    return np.sqrt(integral_result)

#Try to implement a fit that resembles the real data with compressor on for the ASD then integrate!
#a gives the theoretical value, derived on Georgs slides
def integrate_1D_R(m,p0_1D,p0):
    popt = get_fit_1D(m,p0_1D)
    popt2 = get_fit_expon(m,p0)
    popt2 = [ 8.80066804e+07, -8.40690554e-01]
    def integrand(f):
        return (expon(f,*popt2)*(resonance_curve_1D(f,*popt)/popt[0])**2)/(2*np.pi*f)**4
    #quad is a scipz function, if lower boundary is chosen to be 0 this diverges
    integral_result, error_estimate = quad(integrand,8,500)     
    a = np.sqrt(10**(6)*np.abs(popt[2])/(32*(np.pi*popt[1])**3))
    return np.sqrt(integral_result)

#Determines the frequency bins of the FFT
def get_freqs_a():
    fs = 512
    freqs, asd = welch(data_a[:,1], fs, nperseg=4096)
    return freqs

#Calculates the ASD by doing a FFT
def ASD_a(m):
    """fs = 512
    fft_vals = np.fft.fft(data_a[:,m])
    freqs = np.fft.fftfreq(Length_a[0],1/fs)
    asd = (np.abs(fft_vals)**2)/(Length_a[0]*300)
    asd = asd*10**(12)"""
    fs = 512
    freqs, asd = welch(data_a[:,m], fs, nperseg=4096)
    return asd * 10**(12)

#Determines the PSD from the ASD above
def PSD_a(m):
    psd = ASD_a(m) * (2 * np.pi * get_freqs_a())**(-4)
    return psd 

#Fits the ASD of the magnet with the modified resonance curve fit
def get_fit_ASD(m,p0):
    popt, pcov = curve_fit(ASD_fit, get_freqs_a()[:int((Length_a[0]+1)/2)], ASD_a(1)[:int((Length_a[0]+1)/2)], p0, maxfev=100000)
    return popt
#Gives the RMS displacement by integrating the PSD times the response function squared, where the response function is fitted as a 1D harmonic osci
def integrate_1D_ASD(m,p0_1D,p0):
    popt = get_fit_1D(m,p0_1D)
    popt2 = get_fit_ASD(m,p0)
    def integrand(f):
        return (ASD_fit(f,*popt2)*(resonance_curve_1D(f,*popt)/popt[0])**2)/(2*np.pi*f)**4
    #quad is a scipz function, if lower boundary is chosen to be 0 this diverges
    integral_result, error_estimate = quad_vec(integrand,8,256)     
    return np.sqrt(integral_result)

def integrate_2D_ASD(m,p0_2D,p0):
    popt = get_fit_2D(m,p0_2D)
    popt2 = get_fit_ASD(m,p0)
    def integrand(f):
        return (ASD_fit(f,*popt2)*(resonance_curve_2D_normalised(f,*popt))**2)/(2*np.pi*f)**4
    #quad is a scipz function, if lower boundary is chosen to be 0 this diverges
    integral_result, error_estimate = quad_vec(integrand,8,256)     
    return np.sqrt(integral_result)




""" ---------- Plots ---------- """

#Oxford colours https://communications.admin.ox.ac.uk/communications-resources/visual-identity/identity-guidelines/colours

def plot_fit_2D_5(m,p0_2D):
    
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)

    #Get fit parameters
    popt = get_fit_2D_5(m,p0_2D)
    #scatter gives the measurement points without connecting them by a unphysical line
    ax.scatter(data[:Length[m],x,m],np.abs(data[:Length[m],y,m]), marker = "o", s = 2, color = "#426A5A")
    ax.plot(data[:Length[m],x,m], resonance_curve_2D_5(data[:Length[m],x,m], *popt), color = "#61615F", label = "2D-Model Fit")
    #loglog plots with grid and labeling
    print(np.max(resonance_curve_2D_5(data[200:Length[m],x,m], *popt)))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([10,100])
    plt.ylim([0.000001,10])
    plt.grid()
    plt.xlabel("Frequency in Hz", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("Average displacement in $\mu$m", fontsize = 15, fontname ="Times New Roman")

    #takes care of the fond size of the axis values
    plt.tick_params(axis="both", which = "both", labelsize = 8, length = 4 )

    #increases sharpness of the plot
    plt.rcParams["figure.dpi"] = 360

    #gets rid of the square surrounding the plot
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.savefig("/Users/main/Desktop/2D_fit", dpi=300)
    plt.legend()
    plt.show()
    return 

def plot_fit_2D(m,p0_2D):
    
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)

    #Get fit parameters
    popt = get_fit_2D(m,p0_2D)
    #scatter gives the measurement points without connecting them by a unphysical line
    ax.scatter(data[:Length[m],x,m],np.abs(data[:Length[m],y,m]), marker = "o", s = 2, color = "#426A5A")
    ax.plot(data[:Length[m],x,m], resonance_curve_2D(data[:Length[m],x,m], *popt), color = "#61615F", label = "2D-Model Fit")
    #loglog plots with grid and labeling
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([10,100])
    plt.ylim([0.000001,30])
    plt.grid()
    plt.xlabel("Frequency in Hz", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("Average displacement in $\mu$m", fontsize = 15, fontname ="Times New Roman")

    #takes care of the fond size of the axis values
    plt.tick_params(axis="both", which = "both", labelsize = 8, length = 4 )

    #increases sharpness of the plot
    plt.rcParams["figure.dpi"] = 360

    #gets rid of the square surrounding the plot
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.savefig("/Users/main/Desktop/2D_fit", dpi=300)
    plt.legend()
    plt.show()
    return 


def plot_fit_1D(m,p0_1D):
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)

    #Get fit parameters
    popt = get_fit_1D(m,p0_1D)
    print(popt)
    #scatter gives the measurement points without connecting them by a unphysical line
    ax.scatter(data[:Length[m],x,m],np.abs(data[:Length[m],y,m]), marker = "o", s = 2, color = "#426A5A")
    ax.plot(data[:Length[m],x,m], resonance_curve_1D(data[:Length[m],x,m], *popt), color = "#61615F", label = "1D-Model Fit")
    
    #loglog plots with grid and labeling
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([10,100])
    plt.ylim([0.000001,40])
    plt.grid()
    plt.xlabel("Frequency in Hz", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("Average displacement in $\mu$m", fontsize = 15, fontname ="Times New Roman")

    #takes care of the fond size of the axis values
    plt.tick_params(axis="both", which = "both", labelsize = 8, length = 4 )

    #increases sharpness of the plot
    plt.rcParams["figure.dpi"] = 360

    #gets rid of the square surrounding the plot
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.savefig("/Users/main/Desktop/1D_fit", dpi=300)
    plt.legend()
    plt.show()
    return 

def two_col_comp(m,n,y,z):
    #Both plots in one picture
    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (10,4), dpi = 300)

    ax[0].scatter(data[:Length[m],x,m],np.abs(data[:Length[m],y,m]), marker = "o", s = 2, color = "#426A5A")
    ax[0].set_xscale("log")
    ax[0].set_yscale("log")
    ax[0].set_xlim([7,550])
    ax[0].grid()
    ax[0].set_ylim([0.000001,10])
    fig.supxlabel("Frequency in Hz", fontsize = 15, fontname ="Times New Roman")
    ax[0].set_ylabel("Average displacement in $\mu$m", fontsize = 15, fontname ="Times New Roman")
    ax[0].tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
    plt.rcParams["figure.dpi"] = 360
    ax[1].scatter(data[:Length[n],x,n],np.abs(data[:Length[n],z,n]), marker = "o", s = 2, color = "#426A5A")
    ax[1].set_xscale("log")
    ax[1].set_yscale("log")
    ax[1].grid()
    ax[1].set_xlim([7,550])
    ax[1].set_ylim([0.000001,10])
    ax[1].tick_params(axis="both", which = "both", labelsize = 8, length = 4 )
    for spine in ax[0].spines.values():
        spine.set_visible(False)
    for spine in ax[1].spines.values():
        spine.set_visible(False)

    plt.savefig("/Users/main/Desktop/two_col_comp", dpi=300)
    plt.show()
    return 

def single_pic_comp(m,n,y,z):
    #Both measurements in one plot
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)

    ax.scatter(data[:Length[m],x,m],np.abs(data[:Length[m],y,m]), marker = "o", s = 2, color = "#994636", label="m")
    ax.scatter(data[:Length[n],x,n],np.abs(data[:Length[n],z,n]), marker = "o", s = 2, color = "#002147", label="n")


    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([10,100])
    plt.ylim([0.00001,30])
    plt.xlim([8,500])
    plt.grid()
    plt.xlabel("Frequency in Hz", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("Average displacement in $\mu$m", fontsize = 15, fontname ="Times New Roman")


    plt.tick_params(axis="both", which = "both", labelsize = 8, length = 4 )


    plt.rcParams["figure.dpi"] = 360


    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.savefig("/Users/main/Desktop/single_pic_comp", dpi=300)
    plt.legend()
    plt.show()
    return

def plot_table(m):
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)
    a = np.abs(Table(m)) #Get table data
    a = a*10**(-6) #Convert to meter
    a = a/(np.sqrt(data[:Length[m],x,m])) #Devide by freq^(1/2)
   
    ax.scatter(data[:Length[m],x,m],a, marker = "o", s = 2, color = "#994636", label="m")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([10,100])
    plt.xlim([8,200])
    plt.grid()
    plt.xlabel("Frequency in Hz", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("Spectral Displacement in $m/\sqrt{Hz}$", fontsize = 15, fontname ="Times New Roman")


    plt.tick_params(axis="both", which = "both", labelsize = 8, length = 4 )


    plt.rcParams["figure.dpi"] = 360


    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.savefig("/Users/main/Desktop/table_pic_comp", dpi=300)
    plt.legend()
    plt.show()
    return

def magnet_ASD_fit(p0):
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)
    popt2 = get_fit_ASD(m,p0)
    freqs = get_freqs_a()
    ax.plot(freqs[:int((Length_a[0]+1)/2)], ASD_fit(freqs[:int((Length_a[0]+1)/2)],*popt2), label = "fit")
    ax.plot(freqs[:int((Length_a[0]+1)/2)], ASD_a(1)[:int((Length_a[0]+1)/2)], color = "#994636", alpha = 0.33, label = "magnet ASD")
    ax.set_yscale("log")
    plt.xlabel("Frequency in Hz", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("ASD in $\mu m^2/s^3$", fontsize = 15, fontname ="Times New Roman")
    plt.xlim([8,200])
    #plt.ylim([10**(-12),10**(-4)])
    #ax.set_yticks([0.00001,0.000001,0.0000001,0.00000001,0.000000001,0.0000000001,0.00000000001])
    plt.grid()
    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.savefig("/Users/main/Desktop/MagnetASD", dpi=300)
    plt.legend()
    plt.show()
    return 
    
def ASD_response_2D(p0,p0_2D):
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)
    popt = get_fit_2D(m,p0_2D)
    popt2 = get_fit_ASD(m,p0)
    freqs = get_freqs_a() + 0.000000000001
    ax.plot(freqs[:int((Length_a[0]+1)/2)], ASD_fit(freqs[:int((Length_a[0]+1)/2)],*popt2), label = "magnet fit")
    ax.plot(freqs[:int((Length_a[0]+1)/2)], (resonance_curve_2D_normalised(freqs[:int((Length_a[0]+1)/2)],*popt))**2, label = "displacement response", color = "#002147")
    ax.plot(freqs[:int((Length_a[0]+1)/2)], (ASD_fit(freqs[:int((Length_a[0]+1)/2)],*popt2)*(resonance_curve_2D_normalised(freqs[:int((Length_a[0]+1)/2)],*popt))**2)/(2*np.pi*freqs[:int((Length_a[0]+1)/2)])**4, label = "integrand")
    #/(2*np.pi*freqs[:int((Length_a[0]+1)/2)])**4
    ax.set_xscale("log")
    ax.set_yscale("log")
    plt.xlabel("Frequency in Hz", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("Ladder response in $\mu m$", fontsize = 15, fontname ="Times New Roman")
    plt.xlim([1,200])
    plt.ylim([10**(-14),10**(12)])
    plt.grid()
    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.savefig("/Users/main/Desktop/LadderRes", dpi=300)
    plt.legend()
    plt.show()
    return 

def ASD_response_1D(p0,p0_1D):
    fig, ax = plt.subplots(figsize = (6,4), dpi = 300)
    popt = get_fit_1D(m,p0_1D)
    popt2 = get_fit_ASD(m,p0)
    freqs = get_freqs_a() + 0.000000000001
    ax.plot(freqs[:int((Length_a[0]+1)/2)], ASD_fit(freqs[:int((Length_a[0]+1)/2)],*popt2), label = "magnet fit")
    ax.plot(freqs[:int((Length_a[0]+1)/2)], (resonance_curve_1D(freqs[:int((Length_a[0]+1)/2)],*popt)/popt[0])**2, label = "displacement response", color = "#002147")
    ax.plot(freqs[:int((Length_a[0]+1)/2)], (ASD_fit(freqs[:int((Length_a[0]+1)/2)],*popt2)*(resonance_curve_1D(freqs[:int((Length_a[0]+1)/2)],*popt)/popt[0])**2)/(2*np.pi*freqs[:int((Length_a[0]+1)/2)])**4, label = "integrand")
    #/(2*np.pi*freqs[:int((Length_a[0]+1)/2)])**4
    ax.set_yscale("log")
    ax.set_xscale("log")
    plt.xlabel("Frequency in Hz", fontsize = 15, fontname ="Times New Roman")
    plt.ylabel("Ladder response in $\mu m$", fontsize = 15, fontname ="Times New Roman")
    plt.xlim([1,200])
    plt.ylim([10**(-14),10**(12)])
    plt.grid()
    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.savefig("/Users/main/Desktop/LadderRes", dpi=300)
    plt.legend()
    plt.show()
    return 


""" ---------- DIY ---------- """

#Specify measurement for plot
m = 14
n = 3

#Initial values for the 1D resonance fit
p0_1D = [1, 30, 60]
p0_2D = [0.2, 33, 50, -1, 10, 50, 1, 80, 50, 1, 150, 50] 
#p0_2D = [1, 80, 60, -1, 10, 50, 1, 150, 50, 0.1, 200, 50]
#p0_2D = [0.2, 81, 56, 0.01, 100, 1, 0.01, 230, 20, 0.1, 300, 1] 
#p0_2D_5 = [0.2, 32, 53, -1, 50, 0.1, 1, 200, 10, 0.001, 65, 30, -0.1, 8, 0.1]


# 0 -> Frequency; 7 -> Average Displacement using 2nd Capacitive Sensor; 43 -> Table subtracted average displacement using 2nd Capacitive Sensor
x = 0
y = 43
z = 43


plot_fit_1D(m,p0_1D)

plot_fit_2D(m,p0_2D)

"""two_col_comp(m,n,y,z)

single_pic_comp(m,n,y,z)"""


"""print(integrate_1D(m,p0_1D,p0))

popt = get_fit_expon(m,p0)
popt = [ 8.80066804e+07, -8.40690554e-01]

plt.loglog(data[:Length[m],x,m],expon(data[:Length[m],x,m],*popt)*10**(-12))
plt.loglog(data[:Length[m],x,m],Table_ASD(m)*10**(-12))
plt.ylim(0.00000001,0.0001)
plt.show()"""

"""fig, ax = plt.subplots(figsize = (6,4), dpi = 300)
ax.plot(data[:Length[m],x,m],np.sqrt(Table_PSD(m)))
ax.set_yscale("log")
plt.xlim([8,200])
plt.grid()
plt.show()"""


#p0 = [1000, 100, 10, 3, 1, 100000]
p0 = [1000, 100, 10, 3, 1, 100000]
p0_1D = [1, 30, 10]

magnet_ASD_fit(p0)
ASD_response_1D(p0,p0_1D)
ASD_response_2D(p0,p0_2D)

print(integrate_1D(m,p0_1D))
print(integrate_1D_ASD(m,p0_1D,p0))
print(integrate_2D_ASD(m,p0_2D,p0))
