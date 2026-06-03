# Master's Project

Welcome to my Master's Project repository.

This repository contains selected measurement data and analysis code developed during my Master's project at the University of Oxford. It is intended to document the analysis workflow and make the main calculations and plotting routines accessible. While the repository includes the relevant data and code used for the analysis, some scripts may require minor adjustments to paths, parameters, or local settings before being run in a different environment.

## Repository Structure

The repository is divided into two main folders:

- **`Data/`**  
  Contains the measurement data used in the project. The data are organized into:
  - **`Background/`** and **`Laserdisp/`**, which contain measurements related to the shaker-table analysis;
  - **`WindTunnel/`**, which contains measurements from the wind-tunnel experiments.

- **`Code/`**  
  Contains the code used for data processing, analysis, and visualisation. Each subfolder within `Code/` includes its own `README.md` file with further information and instructions specific to that part of the analysis.

## General Project Structure


```
Project_Root/
├── Code/
│   ├── Airflow/
│   │   ├── Functions_AirFlow.py
│   │   ├── Get_Data_AirFlow.py
│   │   ├── Plot_AirFlow.py
│   │   └── WindTunnel.py
│   │
│   └── Vibrations/
│       ├── A Run List.docx
│       ├── AA List of Plot comments.docx
│       ├── Functions_ASD/
│       │   ├── Functions_PSI.py
│       │   ├── Functions_A.py
│       │   └── Functions_B.py
│       ├── Functions_Table/
│       │   ├── Functions_Table_Linear.py
│       │   └── Functions_Table_NL.py
│       ├── Plots/
│       │   ├── Plot_ASD.py
│       │   └── Plot_Vib.py
│       ├── Main.py
│       └── Get_Data_Vib.py
│
└── Data/
    ├── WindTunnel/
    ├── Background/
    └── Laserdisp/
```
