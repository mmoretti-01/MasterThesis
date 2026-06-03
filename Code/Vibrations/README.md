# Vibrations

This folder contains the code used to analyse and plot the data from the shaker-table vibration experiment.

The workflow is organised around `Main.py`. This file is used to select parameters and execute the desired plot functions. The plot functions themselves are written in the `Plots/` folder, and they use helper and analysis functions defined in the function folders.

There are two separate function folders:

- `Functions_ASD/`: functions related to acceleration spectral density analysis.
- `Functions_Table/`: functions related to the vibration/table analysis.

Because there are many available plot functions, the file `AA List of Plot commands.docx` summarises the available plotting commands and options. The file `A Run list.docx` is used to keep track of which dataset belongs to which measurement.

The additional Python files are used to simplify the handling and organisation of the datasets.

## File structure

```text
Vibrations/
├── Main.py
├── Get_Data_Vib.py
├── Rename_Files.py
├── A Run list.docx
├── AA List of Plot commands.docx
├── Functions_ASD/
├── Functions_Table/
├── Plots/
└── README.md
