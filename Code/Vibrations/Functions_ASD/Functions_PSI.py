# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 10:20:52 2025

@author: moretti
"""


from Functions_ASD.Functions_A import *
from Functions_ASD.Functions_B import *


#------------------------------------------------------------------------------------------------------------------------
#+++++++++++- This file won't compute anything, it is a selection-element distinguishing between "a" and "b" -+++++++++++
#------------------------------------------------------------------------------------------------------------------------

def get_ASD(i, n, points, overlap):
    if i == "a":
        freqs, asd = get_ASD_a(n, points, overlap)
        
    elif i == "b":
        freqs, asd = get_ASD_b(n)
        
    else:
        print("wrong input")
        return 0
    return freqs, asd

def get_PSD(i, n , points, overlap):
    if i == "a":
        freqs, psd = get_PSD_a(n, points, overlap)
        
    elif i == "b":
        freqs, psd = get_PSD_b(n)
        
    else:
        print("wrong input")
        return 0
    return freqs, psd

def SG_smooth(i, n, points, overlap, window_length, polyorder):
    if i == "a":
        freqs, asd_smooth = SG_smooth_a(n, points, overlap, window_length, polyorder)
        
    elif i == "b":
        freqs, asd_smooth = SG_smooth_b(n, window_length, polyorder)
    
    else:
        print("wrong input")
        return 0
    return freqs, asd_smooth

def move_av(i, n, points, overlap, window_length):
    if i == "a":
        freqs, asd_av = move_av_a(n, points, overlap, window_length)
        
    elif i == "b":
        freqs, asd_av = move_av_b(n, window_length)
    
    else:
        print("wrong input")
        return 0
    return freqs, asd_av

def envelope(i, n, points, overlap):
    if i == "a":
        freqs, env = get_env_a(n, points, overlap)
        
    elif i == "b":
        freqs, env = get_env_b(n)
        
    else:
        print("wrong input")
        return 0
    return freqs, env