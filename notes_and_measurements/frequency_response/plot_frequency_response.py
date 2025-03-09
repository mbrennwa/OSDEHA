#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

# Function to read data from ASCII file
def read_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    mu_output = {"frequency": [], "v_out": []}
    anode_output = {"frequency": [], "v_out": []}
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line or any(c.isalpha() for c in line.split()[0]):
            if "MU-OUTPUT" in line:
                current_section = mu_output
            elif "ANODE-OUTPUT" in line:
                current_section = anode_output
            continue
        
        if current_section is not None:
            parts = line.split()
            if len(parts) == 2:
                try:
                    freq, vout = float(parts[0]), float(parts[1])
                    current_section["frequency"].append(freq)
                    current_section["v_out"].append(vout)
                except ValueError:
                    pass
    
    if not mu_output["frequency"]:
        print("Warning: No data found for μ-OUTPUT (or MU-OUTPUT). First few lines of the file:")
        for l in lines[:10]:
            print(l.strip())
    if not anode_output["frequency"]:
        print("Warning: No data found for ANODE-OUTPUT")
    
    return mu_output, anode_output

# read data from file:
mu_output, anode_output = read_data("OSDEHA_FREQUENCY_RESPONSE.txt")

# Convert to dB relative to 1000 Hz
ref_freq = 1000

def convert_to_db(data):
    if not data["frequency"]:
        return {"frequency": [], "v_out": []}
    
    if ref_freq in data["frequency"]:
        ref_index = data["frequency"].index(ref_freq)
        ref_vout = data["v_out"][ref_index]
    else:
        if len(data["frequency"]) < 2:
            print("Error: Not enough data points to interpolate for 1000 Hz reference.")
            sys.exit(1)
        ref_vout = np.interp(ref_freq, data["frequency"], data["v_out"])  # Interpolate if 1000 Hz is missing
    
    data_db = {"frequency": data["frequency"], "v_out": 20 * np.log10(np.array(data["v_out"]) / ref_vout)}
    return data_db

mu_output_db = convert_to_db(mu_output)
anode_output_db = convert_to_db(anode_output)

# Plot the data in dB
plt.figure(figsize=(10, 4))
plt.rcParams["font.family"] = "Arial"
plt.rcParams["lines.linewidth"] = 2
plt.rcParams["lines.solid_capstyle"] = "round"
plt.semilogx(mu_output_db["frequency"], mu_output_db["v_out"], color='blue', linestyle='-', label="μ output")
plt.semilogx(anode_output_db["frequency"], anode_output_db["v_out"], color='red', linestyle='-', label="Anode output")

# Formatting
plt.xlabel("Frequency (Hz)")
plt.ylabel("Gain (dB relative to 1 kHz)")
### plt.title("OSDEHA Frequency Response at 100 VRMS Output")
plt.xlim(3, 300000)  # Set x-axis range from 3 Hz to 300 kHz
plt.ylim(-12, 3)     # Set y-axis range from -12 dB to +3 dB

plt.legend(frameon=False)

# Save the plot to a PDF
plt.savefig("frequency_response.pdf", format="pdf", bbox_inches="tight")

# Show the plot
plt.show()

