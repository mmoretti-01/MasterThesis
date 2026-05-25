# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 09:54:11 2025

@author: moretti
"""

import numpy as np
import Functions_ASD.Functions_PSI as PSI
from scipy.optimize import curve_fit
from scipy import integrate
from Get_Data_Vib import Get_Data
from scipy import odr



Length, data = Get_Data("c")


def Length_Data():
    return Length, data

#----------------------------------------
""" --> Max & Mins <-- """
#----------------------------------------

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
    


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
""" ---------- Fits for the ladder response in frequency space ---------- """  
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  


def resonance_curve_m(f, A, f0, Q, S):
    return f**(S)*A/(np.sqrt((1-(f/f0)**2)**2 + (1/Q)**2 * (f/f0)**2))

#This function corresponds to a HO Model function
def resonance_curve_HO(f, A, f0, Q):
    return A/(np.sqrt((1-(f/f0)**2)**2 + (1/Q)**2 * (f/f0)**2))

def resonance_curve_HO_normalised(f, A, f0, Q):
    return 1/(np.sqrt((1-(f/f0)**2)**2 + (1/Q)**2 * (f/f0)**2))

def tension(B, L):
    m, b = B
    n = 1
    return m * (L ** (n/2)) + b

#----------------------------------------
""" --> Get fit parameters <-- """
#----------------------------------------

#m for modified. Given an array of 4 initial values p0 and which data we should consider this function returns the ideal fit parameters for the unphysical fit
def get_fit_m(m, p0, y):
    popt, pcov = curve_fit(resonance_curve_m, data[:Length[m],0,m], np.abs(data[:Length[m],y,m]), p0, maxfev=1000)
    return popt

#Given an array of 3 initial values p0 and which data we should consider this function returns the ideal fit parameters for the unphysical fit
def get_fit_HO(m, p0, y):
    popt, pcov = curve_fit(resonance_curve_HO, data[:Length[m],0,m], np.abs(data[:Length[m],y,m]), p0, maxfev=100000, bounds=([-10, p0[1]-3, 0], [10, p0[1]+3, 130]))
    return popt

def get_fit_HO_new(m, p0, y):
    f = data[:Length[m],0,m]
    print(data[Length[m]-1,0,m])
    popt, pcov = curve_fit(resonance_curve_HO, f, np.abs(data[:Length[m],y,m]), p0, sigma = data[:Length[m],-1,m], maxfev=100000, bounds=(0, np.inf))
    return popt, pcov

def get_fit_tension(L, L_err, T, p0):
    
    model = odr.Model(tension)
    data = odr.RealData(L, T, sx=L_err)        # <-- only x-errors
    odr_run = odr.ODR(data, model, p0).run()
    return odr_run


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
""" ---------- ASD/PSD stuff for displacement RMS analysis """
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#----------------------------------------
""" --> Table <-- """
#----------------------------------------

def Table(m):
    table = data[:Length[m],7,m] - data[:Length[m],43,m]
    return np.abs(table)


def Table_PSD(m):
    a = Table(m)*10**(-6)
    a = a**2
    PSD = a/data[:Length[m],0,m]
    return PSD

def Table_ASD(m):
    PSD = Table_PSD(m)
    ASD = PSD * (2 * np.pi * data[:Length[m],0,m])**4
    return ASD


#----------------------------------------
""" --> Discrete Integrals <-- """
#----------------------------------------

def integrate_disc_HO(i, n, points, overlap, window, order, m, y, p0_HO):
    
   def integrand(f):
       return (asd[20:]*(resonance_curve_HO_normalised(f,*popt))**2)
    
   popt = get_fit_HO(m, p0_HO, y)
   freq, asd = PSI.SG_smooth(i, n, points, overlap, window, order)
   Int = integrate.simpson(integrand(freq[20:]),freq[20:])
   #a = np.sqrt(np.average(asd[20:])*np.abs(popt[2])/(32*(np.pi*popt[1])**3))   
   return np.sqrt(Int)

def integrate_disc_HO_env(i, n, points, overlap, m, y, p0_HO):
    
    def integrand(f):
        return (asd[20:]*(resonance_curve_HO_normalised(f,*popt))**2)/(2*np.pi*f)**(4)
    
    popt = get_fit_HO(m, p0_HO, y)
    freq, asd = PSI.envelope(i, n, points, overlap)
    Int = integrate.simpson(integrand(freq[20:]),freq[20:])
    return np.sqrt(Int)
    

def integrate_disc_HO_100(i, n, points, overlap, window, order, m, y, p0_HO):
     
   def integrand(f):
       return (asd[20:]*(resonance_curve_HO_normalised(f,*popt))**2)/(2*np.pi*f)**(4)
    
   popt = get_fit_HO(m,p0_HO,1)
   popt[1] = 100
   
   freq, asd = PSI.SG_smooth(i, n, points, overlap, window, order)
   Int = integrate.simpson(integrand(freq[20:]),freq[20:])
   #a = np.sqrt(np.average(asd[20:])*np.abs(popt[2])/(32*(np.pi*popt[1])**3))   
   return np.sqrt(Int)

def integrate_ASD(i, n, points, overlap, window, order):
    
    def integrand(f):
        return (asd[20:])/(2*np.pi*f)**4
    
    freq, asd = PSI.SG_smooth(i, n, points, overlap, window, order)
    Int = integrate.simpson(integrand(freq[20:]),freq[20:])
    #a = np.sqrt(np.average(asd[20:])*np.abs(popt[2])/(32*(np.pi*popt[1])**3))   
    return np.sqrt(Int)
    