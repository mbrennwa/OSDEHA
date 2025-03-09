#!/usr/bin/env python3

import os
import argparse
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import re

# Set global font to Arial
plt.rcParams["font.family"] = "Arial"

# Set global rounded capstyle and joinstyle
plt.rcParams["lines.solid_capstyle"] = "round"  # Round line ends
plt.rcParams["lines.solid_joinstyle"] = "round"  # Round line joints

# Function to read spectrum data from a file
def read_spectrum_data(filepath):
    match = re.search(r'([\d\.]+)V', os.path.basename(filepath))
    if match:
        testvoltage = match.group(1) + " V"
    else:
        testvoltage = "Unknown Voltage"
        
    if "MU-OUT" in filepath:
        info = "µ Output, " + testvoltage 
    elif "A-OUT" in filepath:
        info = "Anode Output, " + testvoltage
    else:
        info = "??? " + testvoltage
    frequencies = []
    voltages = []
    with open(filepath, "r") as file:
        for line in file:
            if line.strip() and ";" in line and "Freq(Hz)" not in line:
                parts = line.strip().split(";")
                try:
                    freq = float(parts[0].strip())
                    volt = float(parts[1].strip())
                    if freq > 750:
                        frequencies.append(freq)
                        voltages.append(volt)
                except ValueError:
                    continue  # Skip malformed lines
    return np.array(frequencies), np.array(voltages), info

# Function to format x-axis labels in kHz
def kHz_formatter(x, pos):
    return f"{int(x / 1000)}"

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Plot a single spectrum from a given file.")
parser.add_argument("file", help="Spectrum data file")
parser.add_argument("--output", type=str, help="Save the plot as an image file (e.g., output.png)")
args = parser.parse_args()

# get common file base name:
basename = os.path.basename(args.file)

# Read data from the file
if os.path.exists(args.file):
    freqs, volts, info = read_spectrum_data(args.file)
    
else:
    print(f"Error: File {args.file} not found.")
    exit(1)

# Create plot
plt.figure(figsize=(7, 4))
plt.plot(freqs, volts, label=os.path.basename(args.file))

# Configure plot
plt.xlim(0, 10000)  # Set x-axis range to 0 - 10000 Hz
plt.ylim(1E-4, 100)  # Set x-axis range to 0 - 10000 Hz
plt.gca().xaxis.set_major_formatter(FuncFormatter(kHz_formatter))
plt.xticks(np.arange(0, 11000, 1000))  # Add frequency labels every 1 kHz
plt.xlabel("Frequency (kHz)")
plt.yscale("log")
plt.ylabel("Voltage (V)")
plt.title("OSDEHA Harmonic Spectrum (" + info + ")")

plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Save as PDF
plt.savefig(basename + "harmonic_spectrum.pdf", format="pdf", bbox_inches="tight")


plt.show()

