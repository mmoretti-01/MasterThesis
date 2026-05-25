In this folder you'll find the code for the Shaker-Table experiment:

My workflow consisted of writing plot functions in the Plot subfolder and executing them from the main.py file. 
You can find two word documents in this folder. The Run List can be used to map the Nr to an exact measurement. The second file gives a list of all available plots.
If you want to use functions, you are free to do so. Don't forget to import them: import ... as ... 
You'll find more about the functions provided in the README file of the corresponding subfolders. The functions are divided into ASD and Table. So if you want to analyse acceleration spectral density open the ASD folder, else the Table folder.

The Arrays used look as follows:
==============================
   DATA STRUCTURE OVERVIEW
==============================

Array structure: data[y][j][N]

j = index for measurement data points
y = 0 for frequency, 1 for sensor 2 measurement, 2 for sensor 4 measurement 
N = selects which of the N measurements to consider

Visualization (for a single i):

       y=0 (frequency)      y=1 (sensor 2 measurement)
j=0    data[0][0][N]          data[0][1][N]
j=1    data[1][0][N]          data[1][1][N]
j=2    data[2][0][N]          data[2][1][N]
...        ...                    ...

 

==============================
     DATA_A ARRAY STRUCTURE
==============================

Array structure: data_a[n][j][l]

n = selects which of the 3 measurements to consider
j = index for measurement data points
l = 0 for frequency, 1 for sensor measurement

Visualization (for a single i):

       l=0 (frequency)      l=1 (sensor measurement)
j=0    data_a[n][0][0]          data_a[n][0][1]
j=1    data_a[n][1][0]          data_a[n][1][1]
j=2    data_a[n][2][0]          data_a[n][2][1]
 ...         ...                     ...

