import pandas as pd
import numpy as np

def analyze_cv_file(filepath):
    """
    Reads a tab-delimited CV data file and calculates oxidation and reduction charge.
    Assumes columns: 'Time (s)' and 'Current (mA)'
    Returns: (charge_ox, charge_red, coulombic_efficiency, time, current, current_ox, current_red)
    """

    try:
        data = pd.read_csv(filepath, sep='\t')
        time = data['Time (s)']
        current = data['Current (uA)'] / 1000  # convert µA to mA

        threshold = 0.05 * max(abs(current))
        active_mask = abs(current) > threshold
        time_active = time[active_mask]
        current_active = current[active_mask]

        current_ox = current_active.clip(lower=0)
        current_red = current_active.clip(upper=0)

        charge_ox = np.trapz(current_ox, time_active)
        charge_red = np.trapz(current_red, time_active)

        # Use absolute values to calculate CE safely
        ce = abs(min(charge_ox, charge_red)) / abs(max(charge_ox, charge_red)) * 100

        return charge_ox, charge_red, ce, time_active, current_active, current_ox, current_red

    except Exception as e:
        raise ValueError(f"Error processing file: {e}")