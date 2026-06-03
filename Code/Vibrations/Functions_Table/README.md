# Functions_Table

This folder contains the helper and analysis functions used for the vibration analysis.

The functions are split into two files according to the model used in the analysis:

- `Functions_Table_Linear.py`: functions based on a linear harmonic oscillator model.
- `Functions_Table_NL.py`: functions based on the non-linear model developed for this analysis.

These functions are used by the plotting routines in the `Plots/` folder and are usually called from `Main.py` through the corresponding plot functions.

## File structure

```text
Functions_Table/
├── Functions_Table_Linear.py
├── Functions_Table_NL.py
├── __init__.py
└── README.md
