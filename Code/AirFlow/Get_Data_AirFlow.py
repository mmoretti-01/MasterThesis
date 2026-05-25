# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 16:36:48 2025

@author: moretti
"""

import numpy as np
import os
import pandas as pd


code_dir = os.path.dirname(os.path.realpath(__file__))

# Set your folder path
folder_path = os.path.join(code_dir,"..", "..", "Data", "WindTunnel", "Displacement")
folder_path_flows = os.path.join(code_dir,"..", "..", "Data", "WindTunnel", "Flows")


def Get_Data_Cap():
    # Get list of all CSV files in the folder_path directory
    #excel_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    excel_files = sorted(f for f in os.listdir(folder_path) if f.endswith('.csv'))
    
    # Uncomment to sort files by modification time if order matters
    # excel_files.sort(key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
    
    all_data = []
    
    for file in excel_files:
        file_path = os.path.join(folder_path, file)
        
        # Read the CSV file, skipping the first row (likely a header or metadata)
        df = pd.read_csv(file_path, skiprows=1)
        
        # Convert the DataFrame to a NumPy array with float data type
        # Assumes the data has only numerical values in the remaining rows
        array = df.to_numpy(dtype=float)
        
        all_data.append(array)
    
    # Stack all the 2D arrays into a 3D NumPy array
    # Note: This will raise an error if the shapes of arrays differ
    distances = np.stack(all_data)
    
    return distances

def Get_Data_Flow():
    # Get list of all CSV files in the folder_path_flows directory
    excel_files_flow = [f for f in os.listdir(folder_path_flows) if f.endswith('.csv')]
    
    all_data_flow = []

    for file in excel_files_flow:
        file_path = os.path.join(folder_path_flows, file)
        
        # Read the CSV file with ';' as delimiter, skip the first row
        # Read only the 3rd column (index 2), and limit to first 55 rows
        df = pd.read_csv(file_path, delimiter=';', skiprows=1, usecols=[2], nrows=55)     
        
        # Convert the single-column DataFrame to a NumPy array of strings
        df = np.array(df)
        
        # Replace commas with dots (European decimal format) and convert to float
        arr_fixed = np.char.replace(df.astype(str), ',', '.').astype(float)
        
        # Append the cleaned data to the list
        all_data_flow.append(arr_fixed)

    # Stack all individual arrays into a 3D array: shape (files, 55, 1)
    flow = np.stack(all_data_flow)
    
    # Extract the actual flow values by removing the last singleton dimension
    flows = flow[:, :, 0]
    
    return flows
