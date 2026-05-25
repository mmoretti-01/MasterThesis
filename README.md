Welcome to my Projcet.

As you see there are two folders. In the Data folder you'll find the measurement data separated into Background and Laserdisp which belong to the Shaker-Table analysis and WindTunnel. The second folder is where you'll find the code.
In all subfolders of the Code you'll find a README file with further infos and instructions.
The general structure of the Project is as follows:

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
