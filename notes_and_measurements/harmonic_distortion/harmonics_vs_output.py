#!/usr/bin/env python3

import os
import glob
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Set global font to Arial
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 16
plt.rcParams["lines.solid_capstyle"] = "round"
plt.rcParams["lines.solid_joinstyle"] = "round"

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
                THD = float(parts[parts.index("THD:") + 1])
                THDN = float(parts[parts.index("THD+N:") + 1])

    return voltage, harmonics, THD, THDN

# Function to process all files and compile data
def process_files(file_list):
    compiled_data = []

    for filename in file_list:
        if os.path.exists(filename):
            voltage, harmonics, THD, THDN = extract_harmonics(filename)
            compiled_data.append([
                filename, voltage, THD, THDN, 
                harmonics.get(2, 0), harmonics.get(3, 0), harmonics.get(4, 0), harmonics.get(5, 0), 
                harmonics.get(6, 0), harmonics.get(7, 0), harmonics.get(8, 0), harmonics.get(9, 0)
            ])

    # Convert to DataFrame
    columns = ["Filename", "Voltage (V-RMS)", "THD (%)", "THD+N (%)", 
               "H2 (%)", "H3 (%)", "H4 (%)", "H5 (%)", "H6 (%)", "H7 (%)", "H8 (%)", "H9 (%)"]
    df = pd.DataFrame(compiled_data, columns=columns)
    df = df.sort_values(by="Voltage (V-RMS)", ascending=True)

    return df

# Function to add a plot to a subplot
def plot_harmonics(ax, df, label_text, show_legend=False, show_xlabel=False):
    ax.plot(df["Voltage (V-RMS)"], df["H2 (%)"], marker='.', label="H2 (%)")
    ax.plot(df["Voltage (V-RMS)"], df["H3 (%)"], marker='.', label="H3 (%)")
    ax.plot(df["Voltage (V-RMS)"], df["H4 (%)"], marker='.', label="H4 (%)")
    ax.plot(df["Voltage (V-RMS)"], df["H5 (%)"], marker='.', label="H5 (%)")

    ax.set_xscale("log")
    ax.set_yscale("log")

    if show_xlabel:
        ax.set_xlabel("Fundamental Voltage (V-RMS)")
    
    ax.set_ylabel("Harmonic Level")
    
    if show_legend:
        ax.legend()
    
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)

    ax.set_ylim(0.0001, 0.1)
    ax.set_xlim(0.7, 150)

    custom_ticks = [1, 3, 10, 30, 100]
    ax.set_xticks(custom_ticks)
    ax.set_xticklabels([str(tick) for tick in custom_ticks])

    # Custom function to add "%" to y-axis labels
    def percentage_formatter(x, pos):
        return f"{x:g}%"

    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(percentage_formatter))

    # Add text label at the top center of each subplot (not bold)
    ax.text(0.5, 0.92, label_text, transform=ax.transAxes, fontsize=16, ha="center", va="top")

# Main function
def main():
    # Define file search patterns
    file_patterns = ['OSDEHA_MU-OUT*.txt', 'OSDEHA_A-OUT*.txt']
    dataframes = {}
    labels = {}

    for pattern in file_patterns:
        # Expand wildcards to get actual file list
        files = glob.glob(pattern)
        
        if not files:
            print(f"Warning: No files found for pattern '{pattern}'")
            continue  # Skip to next pattern if no matching files are found

        # Get common file base name
        basename = os.path.commonprefix([os.path.basename(file) for file in files])

        # Process files and get DataFrame
        df = process_files(files)
        print(df)

        # Store data for plotting
        dataframes[basename] = df
        labels[basename] = "μ output" if "MU-OUT" in basename else "Anode output"

    # Create figure with two subplots
    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Plot the first dataset (upper panel)
    first_basename, first_df = list(dataframes.items())[0]
    plot_harmonics(axs[0], first_df, labels[first_basename], show_legend=False, show_xlabel=False)

    # Plot the second dataset (lower panel)
    second_basename, second_df = list(dataframes.items())[1]
    plot_harmonics(axs[1], second_df, labels[second_basename], show_legend=True, show_xlabel=True)

    # Adjust layout and save figure
    plt.tight_layout()
    plt.savefig("harmonics_vs_voltage.pdf", format="pdf", bbox_inches="tight")
    print("Plot saved as harmonics_vs_voltage.pdf")

    # Show plot
    plt.show()

# Run the script only if executed directly
if __name__ == "__main__":
    main()

