# AirFlow

This folder contains the code used to acquire, process, and plot the data from the airflow experiment.

The code is organized so that `WindTunnel.py` acts as the main entry point. It is used to choose the relevant parameters and run the desired plotting routines. The plotting routines are defined in `Plot_AirFlow.py`, while the underlying analysis and helper functions are collected in `Functions_AirFlow.py`. Data acquisition is handled separately by `Get_Data_AirFlow.py`.

## File structure

```text
AirFlow/
├── WindTunnel.py
├── Get_Data_AirFlow.py
├── Plot_AirFlow.py
├── Functions_AirFlow.py
└── README.md
