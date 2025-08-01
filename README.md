# Radiostat_Testing

**Radiostat_Testing** is a classroom-oriented electrochemical experiment suite built in Python. It combines real potentiostat control (via the Rodeostat) with an interactive GUI to walk students through a simulated battery research investigation.

## Purpose

This tool is designed to guide high school or early undergraduate students through:
- Selecting electrolytes for beaker cell testing
- Running real cyclic voltammetry experiments
- Analyzing charge integration to determine Coulombic Efficiency
- Writing scientific explanations and conclusions

It supports up to 3 test runs per student and provides visualization, annotation, and guided reflection for each.

## Features

- Tkinter-based multi-page GUI with scroll support
- Potentiostat integration via Rodeostat firmware
- Automatic CV test execution and graphing
- Embedded Matplotlib visualizations
- Data upload, processing, and student input
- JSON-based response saving for grading or review

## How to Run

1. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

2. Run the app:
   ```
   runRadiostat
   ```

3. Follow the guided workflow from introduction to conclusion.

## Requirements

See `requirements.txt` for package dependencies.