#!/usr/bin/env python3

import os
import argparse
import numpy as np
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Set global font to Arial
plt.rcParams["font.family"] = "Arial"

# Set global rounded capstyle and joinstyle
plt.rcParams["lines.solid_capstyle"] = "round"  # Round line ends
plt.rcParams["lines.solid_joinstyle"] = "round"  # Round line joints

# Function to extract harmonics from file headers
def extract_harmonics(filepath):
    harmonics = {}
    voltage = None
    with open(filepath, "r") as file:
        for line in file:
            if "Input RMS" in line:
                match = re.search(r'([\d\.]+)V', os.path.basename(filepath))
                if match:
                    voltage = float(match.group(1))
            if "* Note" in line:
                parts = line.split()
                harmonics[2] = float(parts[parts.index("2nd") + 2])
                harmonics[3] = float(parts[parts.index("3rd") + 2])
                harmonics[4] = float(parts[parts.index("4th") + 2])
                harmonics[5] = float(parts[parts.index("5th") + 2])
                harmonics[6] = float(parts[parts.index("6th") + 2])
                harmonics[7] = float(parts[parts.index("7th") + 2])
                harmonics[8] = float(parts[parts.index("8th") + 2])
                harmonics[9] = float(parts[parts.index("9th") + 2])
                THD          = float(parts[parts.index("THD:") + 1])
                THDN         = float(parts[parts.index("THD+N:") + 1])

    return voltage, harmonics, THD, THDN

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Extract and compile harmonics from multiple files.")
parser.add_argument("files", nargs="+", help="List of spectrum data files")
parser.add_argument("--output", type=str, help="Save the compiled data as a CSV file")
args = parser.parse_args()

# get common file base name:
basename = os.path.commonprefix([os.path.basename(file) for file in args.files])

# Read data from all files
compiled_data = []

for filename in args.files:
    if os.path.exists(filename):
        voltage, harmonics, THD, THDN = extract_harmonics(filename)
        compiled_data.append([filename, voltage, THD, THDN, harmonics[2], harmonics[3], harmonics[4], harmonics[5], harmonics[6], harmonics[7], harmonics[8], harmonics[9]])

# Convert to DataFrame
columns = ["Filename", "Voltage (V-RMS)", "THD (%)", "THD+N (%)", "H2 (%)", "H3 (%)", "H4 (%)", "H5 (%)", "H6 (%)", "H7 (%)", "H8 (%)", "H9 (%)"]
df = pd.DataFrame(compiled_data, columns=columns)
df = df.sort_values(by="Voltage (V-RMS)", ascending=True)

# Save or print results
if args.output:
    df.to_csv(args.output, index=False)
    print(f"Harmonic data saved to {args.output}")
else:
    print(df)

# Plot THD, H2, and H3 vs. Voltage
plt.figure(figsize=(7, 4))
plt.plot(df["Voltage (V-RMS)"], df["H2 (%)"], marker='.', label="H2 (%)")
plt.plot(df["Voltage (V-RMS)"], df["H3 (%)"], marker='.', label="H3 (%)")
plt.plot(df["Voltage (V-RMS)"], df["H4 (%)"], marker='.', label="H4 (%)")
plt.plot(df["Voltage (V-RMS)"], df["H5 (%)"], marker='.', label="H5 (%)")

# Configure plot
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Fundamental Voltage (V-RMS)")
plt.ylabel("Harmonic Level")
if "MU-OUT" in basename:
    info = "µ Output"
elif "A-OUT" in basename:
    info = "Anode Output"
else:
    info = "??? Output"
plt.title("Harmonic Levels vs. Fundamental Voltage (" + info + ")")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

plt.ylim(0.0001, 0.1)
plt.xlim(0.7, 150)

custom_ticks = [1, 3, 10, 30, 100]
plt.xticks(custom_ticks, [str(tick) for tick in custom_ticks])  # Set non-exponential labels

# Custom function to add "%" to y-axis labels
def percentage_formatter(x, pos):
    return f"{x:g}%"  # Removes trailing zeros and adds "%"


plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter())  # Disable scientific notation
### plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter("%g"))  # Removes trailing zeros
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(percentage_formatter))

# Save as PDF
plt.savefig(basename + "harmonics_vs_voltage.pdf", format="pdf", bbox_inches="tight")

# Show plot
plt.show()


