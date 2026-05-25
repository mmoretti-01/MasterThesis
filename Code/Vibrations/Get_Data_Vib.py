# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 16:49:14 2025

@author: moretti
"""

import numpy as np
import os
import pandas as pd





# Number of primary measurement files and additional files
Nr = 40
Nr__ = 50

# These lists will hold opened file objects after reading
Doc = []      # Measurement data
Doc_a = []    # Background dataset L
Doc_a2 = []   # Background dataset V
Doc_a3 = []   # Background dataset T

""" ---------- Read Folders  ---------- """

# Reads all files in a given folder, sorts them by last modified time,
# and appends them (opened) to the global list Doc
def read_folder(Folder):
    Dateien = os.listdir(Folder)  # List all files
    #Dateien.sort(key = lambda f: os.path.getmtime(os.path.join(Folder, f)))  # Sort by modification date
    Dateien = sorted(os.listdir(Folder))
    Di0 = len(Dateien)
    for j in range(Di0):
        Doc.append(open(os.path.join(Folder, Dateien[j]), "r"))  # Open and store file handles
    return 0  # Dummy return value

# Get the absolute path of the current script
code_dir = os.path.dirname(os.path.realpath(__file__))

# Define paths to data directories and files relative to the script
Folder = os.path.join(code_dir, "..", "..", "Data", "Laserdisp")
Site_0 = os.path.join(code_dir, "..", "..", "Data", "Background", "DatasetA1_Bracket_L.txt")
Site_1 = os.path.join(code_dir, "..", "..", "Data", "Background", "DatasetA1_Bracket_V.txt")
Site_2 = os.path.join(code_dir, "..", "..", "Data", "Background", "DatasetA1_Bracket_T.txt")
Site_b = os.path.join(code_dir, "..", "..", "Data", "Background", "Mu3E_20201202_A1A2.xlsx")

# Read main measurement files into Doc


# If a single file is needed instead, you can manually append it to Doc:
# Doc.append(open('C:/Users/moretti/Desktop/data/' + 'Laserdisp 04-03-2025 14-08-56.dat', "r"))

# Open the three background PSI data files




""" ---------- Copy Data into Array  ---------- """

# Arrays to hold the number of lines per file
Length = []     # For main displacement data
Length_a = []



def data_c():
    read_folder(Folder)
    # Arrays to hold the number of lines per file
    Length = []     # For main displacement data
    
    # Select specific columns from the data files
    selected_columns = [0, 7, 11, 15, 43]  # For main files
    data = np.zeros([500, len(selected_columns) + 2, Nr + Nr__])  # Preallocate 3D array: [lines, columns, files]
    
    for i in range(Nr):
        Lines = Doc[i].readlines()[2:]  # Skip first 2 lines (headers?)
        Length.append(len(Lines))       # Store number of lines for each file
        b = 0
        for line in Lines:
            numbers = [float(value) for value in line.split()]  # Convert line to list of floats
            inumbers = [numbers[j] for j in selected_columns]   # Select relevant columns
            full_row = np.zeros(7)
            full_row[:5] = inumbers
            data[b, :, i] = full_row
            #data[b, :, i] = inumbers                           # Store in data array
            b += 1
            
    
    selected_columns = [0, 7, 11, 15, 43]

    for i in range(Nr, Nr + Nr__):
        Lines = Doc[i].readlines()[2:]
        l = len(Lines)
        Length.append(l)
        b = 0
        for line in Lines:
            numbers = [float(values) for values in line.split()]
            inumbers = [numbers[j] for j in selected_columns]
            full_row = np.zeros(7)
            full_row[:5] = inumbers
            data[b, :, i] = full_row
            #data[b, :, i] = inumbers
            b = b + 1 
            
    #The following loop determines the average displacement of the two table movements right and left of the ladder     
    for i in range(len(Length)):
        average = 0.5*(data[:Length[i],2,i] + data[:Length[i],3,i])
        
        #linearity_table = 0.05/100 * average 
        linearity_table = 0.5/np.sqrt(3) 
        
        #deviation = 1/np.sqrt(2000) #Max. Sensitivity deviation 0.1% of FSO
        deviation = 1/np.sqrt(3) 
        
        resolution = 1.5/np.sqrt(3) #Resolution is 0.15% of Full Scale Output
        
        #linearity_ladder = 0.03/100 * data[:Length[i],1,i] #Linearity would be 0.3% of FSO.
        linearity_ladder = 0.5/np.sqrt(3) 
        
        uncertainty_table = np.sqrt(linearity_table**2 + (resolution/np.sqrt(2))**2 + (deviation)**2)/np.sqrt(2000)
        uncertainty_ladder = np.sqrt(linearity_ladder**2 + (resolution)**2 + (deviation)**2)/np.sqrt(2000)
        
        #Determines the normalised response function and saves it in the data array as the 6th entry
        data[:Length[i],5,i] = data[:Length[i],1,i]/average
        
        #For uncertainties on normalised response uncomment the line below
        #data[:Length[i],6,i] = data[:Length[i],5,i]*np.sqrt((uncertainty_ladder/data[:Length[i],1,i])**2 + (uncertainty_table/average)**2)
        #For uncertainties on measured data uncomment the line below
        data[:Length[i],6,i] = uncertainty_ladder
    
            
    return Length, data

# --- Read and structure PSI background data ---

# Process background dataset L
def data_a():
    # Arrays to hold the number of lines per file
    Length_a = []
    
    Doc_a.append(open(Site_0, "r"))
    Lines_a = Doc_a[0].readlines()[50:]  # Skip first 50 lines
    l = len(Lines_a)
    Length_a.append(l)
    data_a = np.zeros([3, Length_a[0], 2])  # Shape: [3 datasets, time, 2 columns (x/y)]
    b = 0
    for line_a in Lines_a:
        for values_a in line_a.split():
            numbers_a = [float(values_a) for values_a in line_a.split()]
        inumbers_a = numbers_a[0:2]
        data_a[1, b, :] = inumbers_a  # Store in second layer
        b = b + 1


# Process background dataset V
    Doc_a2.append(open(Site_1, "r"))
    Lines_a2 = Doc_a2[0].readlines()[50:]
    l = len(Lines_a2)
    Length_a.append(l)
    b = 0
    for line_a2 in Lines_a2:
        for values_a2 in line_a2.split():
            numbers_a2 = [float(values_a2) for values_a2 in line_a2.split()]
        inumbers_a2 = numbers_a2[0:2]
        data_a[0, b, :] = inumbers_a2  # Store in first layer
        b = b + 1


# Process background dataset T
    Doc_a3.append(open(Site_2, "r"))
    Lines_a3 = Doc_a3[0].readlines()[50:]
    l = len(Lines_a3)
    Length_a.append(l)
    b = 0
    for line_a3 in Lines_a3:
        for values_a3 in line_a3.split():
            numbers_a3 = [float(values_a3) for values_a3 in line_a3.split()]
        inumbers_a3 = numbers_a3[0:2]
        data_a[2, b, :] = inumbers_a3  # Store in third layer
        b = b + 1
    return Length_a, data_a


# --- Read Excel file containing PSI readings ---
def data_b():
    xls = pd.ExcelFile(Site_b)
    df = pd.read_excel(xls, sheet_name="A1")
    data_b = df.iloc[59:, [16, 21, 26, 0]].to_numpy()  # Select specific columns and rows
    return data_b
# data_b = data_b[:, [3, 0, 1, 2]]  # Optional reorder if needed

""" ---------- General Functions ---------- """

""" --> Get Data <-- """

# Retrieve selected dataset based on a key:
# 'a' - background PSI data (from 3 text files)
# 'b' - background PSI data from Excel
# 'c' - displacement measurements
def Get_Data(key):
    if key == 'a':
        return data_a()
    elif key == 'b':
        return data_b()
    elif key == 'c':
        return data_c()
    else:
        raise ValueError("Invalid key. Use 'a', 'b' or 'c'.")
    return 

        

