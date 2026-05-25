# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 10:44:11 2025

@author: moretti
"""

from pathlib import Path
import re
import os

code_dir = Path(os.path.realpath(__file__)).parent

Folder = (code_dir / ".." / ".." / "Data" / "Laserdisp").resolve()

pattern = re.compile(r"(Laserdisp) (\d{2})-(\d{2})-(\d{4}) (\d{2}-\d{2}-\d{2})\.dat$")

for file in Folder.iterdir():
    if file.is_file() and file.suffix == ".dat":
        match = pattern.match(file.name)
        if match:
            prefix, day, month, year, time = match.groups()
            new_name = f"{prefix} {year}-{month}-{day} {time}.dat"
            new_path = file.with_name(new_name)
            file.rename(new_path)
            print(f"Renamed: {file.name} -> {new_name}")