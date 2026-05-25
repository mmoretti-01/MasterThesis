# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 09:54:11 2025

@author: moretti
"""

import numpy as np
import Functions_ASD.Functions_PSI as PSI
from scipy.optimize import curve_fit
from scipy import integrate
import Functions_Table.Functions_Table_Linear as lin
from Functions_Table.Functions_Table_Linear import Length_Data


Length, data = Length_Data()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
""" ---------- Fits for the ladder response in frequency space ---------- """  
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  

#This function corresponds to a 2D Model function
def resonance_curve_BB_2(f, A_1, f0_1, Q_1, A_2, f0_2, Q_2):
    term_1 = A_1/((1-(f/f0_1)**2) + (1j/Q_1) * (f/f0_1))
    term_2 = A_2/((1-(f/f0_2)**2) + (1j/Q_2) * (f/f0_2))
    return np.abs(term_1 + term_2)

def response_function_BB_2(f, A_1, f0_1, Q_1, A_2, f0_2, Q_2):
    term_1 = A_1/((1-(f/f0_1)**2) + (1j/Q_1) * (f/f0_1))
    term_2 = A_2/((1-(f/f0_2)**2) + (1j/Q_2) * (f/f0_2))
    A = A_1 + A_2
    return np.abs(term_1 + term_2)/A

def resonance_curve_BB_3(f, A_1, f0_1, Q_1, A_2, f0_2, Q_2, A_3, f0_3, Q_3):
    term_1 = A_1/((1-(f/f0_1)**2) + (1j/Q_1) * (f/f0_1))
    term_2 = A_2/((1-(f/f0_2)**2) + (1j/Q_2) * (f/f0_2))
    term_3 = A_3/((1-(f/f0_3)**2) + (1j/Q_3) * (f/f0_3))
    return np.abs(term_1 + term_2 + term_3)

def response_function_BB_3(f, A_1, f0_1, Q_1, A_2, f0_2, Q_2, A_3, f0_3, Q_3):
    term_1 = A_1/((1-(f/f0_1)**2) + (1j/Q_1) * (f/f0_1))
    term_2 = A_2/((1-(f/f0_2)**2) + (1j/Q_2) * (f/f0_2))
    term_3 = A_3/((1-(f/f0_3)**2) + (1j/Q_3) * (f/f0_3))
    A = A_1 + A_2 + A_3 
    return np.abs(term_1 + term_2 + term_3)/A

def resonance_curve_BB_4(f, A_1, f0_1, Q_1, A_2, f0_2, Q_2, A_3, f0_3, Q_3, A_4, f0_4, Q_4):
    term_1 = A_1/((1-(f/f0_1)**2) + (1j/Q_1) * (f/f0_1))
    term_2 = A_2/((1-(f/f0_2)**2) + (1j/Q_2) * (f/f0_2))
    term_3 = A_3/((1-(f/f0_3)**2) + (1j/Q_3) * (f/f0_3))
    term_4 = A_4/((1-(f/f0_4)**2) + (1j/Q_4) * (f/f0_4))
    return np.abs(term_1 + term_2 + term_3 + term_4)

def response_function_BB_4(f, A_1, f0_1, Q_1, A_2, f0_2, Q_2, A_3, f0_3, Q_3, A_4, f0_4, Q_4):
    term_1 = A_1/((1-(f/f0_1)**2) + (1j/Q_1) * (f/f0_1))
    term_2 = A_2/((1-(f/f0_2)**2) + (1j/Q_2) * (f/f0_2))
    term_3 = A_3/((1-(f/f0_3)**2) + (1j/Q_3) * (f/f0_3))
    term_4 = A_4/((1-(f/f0_4)**2) + (1j/Q_4) * (f/f0_4))
    A = A_1 + A_2 + A_3 + A_4
    return np.abs(term_1 + term_2 + term_3 + term_4)/A

def resonance_curve_BB_5(f, A_1, f0_1, Q_1, A_2, f0_2, Q_2, A_3, f0_3, Q_3, A_4, f0_4, Q_4, A_5, f0_5, Q_5):
    term_1 = A_1/((1-(f/f0_1)**2) + (1j/Q_1) * (f/f0_1))
    term_2 = A_2/((1-(f/f0_2)**2) + (1j/Q_2) * (f/f0_2))
    term_3 = A_3/((1-(f/f0_3)**2) + (1j/Q_3) * (f/f0_3))
    term_4 = A_4/((1-(f/f0_4)**2) + (1j/Q_4) * (f/f0_4))
    term_5 = A_5/((1-(f/f0_5)**2) + (1j/Q_5) * (f/f0_5))
    return np.abs(term_1 + term_2 + term_3 + term_4 + term_5)

def response_function_BB_5(f, A_1, f0_1, Q_1, A_2, f0_2, Q_2, A_3, f0_3, Q_3, A_4, f0_4, Q_4, A_5, f0_5, Q_5):
    term_1 = A_1/((1-(f/f0_1)**2) + (1j/Q_1) * (f/f0_1))
    term_2 = A_2/((1-(f/f0_2)**2) + (1j/Q_2) * (f/f0_2))
    term_3 = A_3/((1-(f/f0_3)**2) + (1j/Q_3) * (f/f0_3))
    term_4 = A_4/((1-(f/f0_4)**2) + (1j/Q_4) * (f/f0_4))
    term_5 = A_5/((1-(f/f0_5)**2) + (1j/Q_5) * (f/f0_5))
    A = A_1 + A_2 + A_3 + A_4
    return np.abs((term_1 + term_2 + term_3 + term_4 + term_5)/A)

#----------------------------------------
""" --> Get fit parameters <-- """
#----------------------------------------

#m for modified. Given an array of 4 initial values p0 and which data we should consider this function returns the ideal fit parameters for the unphysical fit
#Same as above but for the Bernoulli 4th order case

def get_fit_BB_2(m, p0, y):
    popt, pcov = curve_fit(resonance_curve_BB_2, data[:Length[m],0,m], np.abs(data[:Length[m],y,m]), p0, maxfev=100000, bounds  = ([-10, p0[1]-3, 0, -10, p0[4]-5, 0], [10, p0[1]+3, 1000, 10, p0[4]+5, 1000]))
    return popt

def get_fit_BB_3(m, p0, y):
    popt, pcov = curve_fit(resonance_curve_BB_3, data[:Length[m],0,m], np.abs(data[:Length[m],y,m]), p0, maxfev=100000, bounds  = ([-10, p0[1]-3, 0, -10, p0[4]-5, 0, -10, p0[7]-7 , 0], [10, p0[1]+3, 1000, 10, p0[4]+5, 1000, 10, p0[7]+7, 1000]))
    return popt

def get_fit_BB_4(m, p0, y):
    popt, pcov = curve_fit(resonance_curve_BB_4, data[:Length[m],0,m], np.abs(data[:Length[m],y,m]), p0, maxfev=100000, bounds  = ([-10, p0[1]-3, 0, -10, p0[4]-5, 0, -10, p0[7]-5 , 0, -10, p0[10]-5, 0], [10, p0[1]+3, 1000, 10, p0[4]+5, 1000, 10, p0[7]+5, 1000, 10, p0[10]+5, 1000]))
    return popt

def get_fit_BB_5(m, p0, y):
    popt, pcov = curve_fit(resonance_curve_BB_5, data[:Length[m],0,m], np.abs(data[:Length[m],y,m]), p0, maxfev=1000000, bounds = ([-10, p0[1]-3, 0, -10, p0[4]-5, 0, -10, p0[7]-7 , 0, -10, p0[10]-9, 0, -5, p0[13]-11, 0], [10, p0[1]+3, p0[2]+50, 10, p0[4]+5, p0[5]+50, 10, p0[7]+7, p0[8]+50, 10, p0[10]+9, p0[11]+50, 10, p0[13]+11, p0[14]+50]))
    return popt, pcov


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
""" ---------- ASD/PSD stuff for displacement RMS analysis """
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#----------------------------------------
""" --> Discrete Integrals <-- """
#----------------------------------------

#Uses simpson rule for determining the discrete Integral 
#64 corresponds to 8Hz

def integrate_disc_BB_2(i, n, points, overlap, window, order, m, y, p0_BB_2):
    
    def integrand(f):
        return (asd[20:]*(response_function_BB_2(f,*popt))**2)/(2*np.pi*f)**4
    
    popt = get_fit_BB_2(m, p0_BB_2, y)
    freq, asd = PSI.SG_smooth(i, n, points, overlap, window, order)
    Int = integrate.simpson(integrand(freq[20:]),freq[20:]) 
    return np.sqrt(Int)

def integrate_disc_BB_3(i, n, points, overlap, window, order, m, y, p0_BB_3):
    
    def integrand(f):
        return (asd[20:]*(response_function_BB_3(f,*popt))**2)/(2*np.pi*f)**4
    
    popt = get_fit_BB_3(m, p0_BB_3, y)
    freq, asd = PSI.SG_smooth(i, n, points, overlap, window, order)
    Int = integrate.simpson(integrand(freq[20:]),freq[20:]) 
    return np.sqrt(Int)

def integrate_disc_BB_4(i, n, points, overlap, window, order, m, y, p0_BB):
    
    def integrand(f):
        return (asd[20:]*(response_function_BB_4(f,*popt))**2)/(2*np.pi*f)**4
    
    popt = get_fit_BB_4(m, p0_BB, y)
    freq, asd = PSI.SG_smooth(i, n, points, overlap, window, order)
    Int = integrate.simpson(integrand(freq[20:]),freq[20:]) 
    return np.sqrt(Int)


def integrate_disc_BB_5(i, n, points, overlap, window, order, f, values, p0_BB_5):
    
    def integrand(f):
        return (asd[20:]*(resonance_curve_BB_5(f,*popt))**2)/(2*np.pi*f)**4
    
    popt = get_fit_BB_5(f, values, p0_BB_5)
    freq, asd = PSI.SG_smooth(i, n, points, overlap, window, order)
    Int = integrate.simpson(integrand(freq[20:]),freq[20:]) 
    return np.sqrt(Int)

def integrate_disc_BB_5(i, n, points, overlap, f, values, p0_BB_5):
    
    def integrand(f):
        return (asd[20:]*(resonance_curve_BB_5(f,*popt))**2)/(2*np.pi*f)**4
    
    popt = get_fit_BB_5(f, values, p0_BB_5)
    freq, asd = PSI.ASD(i, n, points, overlap)
    Int = integrate.simpson(integrand(freq[20:]),freq[20:]) 
    return np.sqrt(Int)

def integrate_disc_n(m, y, asd, freq, p0):
    
    if len(p0)/3 == 1:
        popt = lin.get_fit_HO(m, p0, y)
        #popt[1] = 100
        fit = lin.resonance_curve_HO(freq[20:], *popt)
    
    elif len(p0)/3 == 2:
        popt = get_fit_BB_2(m, p0, y)
        fit = resonance_curve_BB_2(freq[20:], *popt)
    
    elif len(p0)/3 == 3:
        popt = get_fit_BB_3(m, p0, y)
        fit = resonance_curve_BB_3(freq[20:], *popt)
        
    elif len(p0)/3 == 4:
        popt = get_fit_BB_4(m, p0, y)
        fit = resonance_curve_BB_4(freq[20:], *popt)
        
    elif len(p0)/3 == 5:
        popt = get_fit_BB_5(m, p0, y)
        fit = resonance_curve_BB_5(freq[20:], *popt)
        
    else:
        print("wrong initial guess format")
        return 
    
    def integrand(x, fit_):
        return (asd[20:]*(fit_)**2)/(2*np.pi*x)**4
    
    Int = integrate.simpson(integrand(freq[20:], fit),freq[20:])
    return np.sqrt(Int)

def integrate_disc__(m, y, p0, i, n, points, overlap):
    
    freq, asd = PSI.get_ASD(i, n, points, overlap)
    
    if len(p0)/3 == 1:
        popt = lin.get_fit_HO(m, p0, y)
        fit = lin.resonance_curve_HO(freq[20:], *popt)
    
    elif len(p0)/3 == 2:
        popt = get_fit_BB_2(m, p0, y)
        fit = resonance_curve_BB_2(freq[20:], *popt)
    
    elif len(p0)/3 == 3:
        popt = get_fit_BB_3(m, p0, y)
        fit = resonance_curve_BB_3(freq[20:], *popt)
        
    elif len(p0)/3 == 4:
        popt = get_fit_BB_4(m, p0, y)
        fit = resonance_curve_BB_4(freq[20:], *popt)
        
    elif len(p0)/3 == 5:
        popt, pcov = get_fit_BB_5(m, p0, y)
        fit = resonance_curve_BB_5(freq[20:], *popt)
        
    else:
        print("wrong initial guess format")
        return 
    
    def integrand(x, fit_):
        return (asd[20:]*(fit_)**2)/(2*np.pi*x)**4
    
    Int = integrate.simpson(integrand(freq[20:], fit),freq[20:])
    return np.sqrt(Int)
