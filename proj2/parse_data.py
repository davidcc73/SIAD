import os
import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
import argparse

def parse_lat_log(directory):
    # Use glob to match files with any number between the dots
    lat_log_pattern = os.path.join(directory, '_lat.*.log')
    
    # Get the list of matching files
    lat_log_files = glob.glob(lat_log_pattern)
    
    if not lat_log_files:
        print(f"Error: No files matching {lat_log_pattern} found.")
        return None
    
    # Read the log file into a pandas DataFrame
    data = []

    # Iterate over each file
    for lat_log_path in lat_log_files:
        with open(lat_log_path, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 5:
                    index, latency, _, block_size, status = parts
                    # Only add the data if the latency is a valid number
                    try:
                        latency = int(latency)
                        data.append([int(index), latency, int(block_size), status])
                    except ValueError:
                        continue
    
    # Create a DataFrame
    df = pd.DataFrame(data, columns=["Index", "Latency", "Block Size", "Status"])
    
    return df

def group_by_intervals(df, interval_seg):
    """
    Groups the data into intervals of 'interval_seg' seconds based on Index
    and calculates the average Latency for each group.
    """

    # Change timestamp from milliseconds to seconds
    df["Index"] = df["Index"] / 1000.0  # Convert from ms to seconds

    # Calculate the interval group (Index divided by the interval)
    df["Time Group"] = (df["Index"] // interval_seg) * interval_seg

    # Group by the interval and calculate the mean latency
    grouped = df.groupby("Time Group")["Latency"].mean().reset_index()

    # Rename columns for clarity
    grouped.columns = ["Time Group", "Average Latency"]
    
    return grouped

def plot_latency(destination_directory, df_grouped, output, title, x, y):
    # Create a plot of averaged latency over time
    plt.figure()
    plt.plot(df_grouped["Time Group"], df_grouped["Average Latency"], label="Average Latency")
    
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(True)
    
    # Save or show the plot
    plt.savefig(os.path.join(destination_directory, output), format="svg")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process latency logs and generate latency plots.")
    parser.add_argument("--source_directory", type=str, help="Path to the source directory containing the latency logs.")
    parser.add_argument("--destination_directory", type=str, help="Path to the destination directory for output files.")
    parser.add_argument("--interval_seg", type=int, help="Interval duration in seconds for averaging latency (default: 30 seconds).")
    args = parser.parse_args()
    
    source_directory = args.source_directory
    destination_directory = args.destination_directory
    interval_seg = args.interval_seg

    # Parse the latency log
    df = parse_lat_log(source_directory)
    
    if df is not None:
        # Group data into intervals and compute averages
        grouped_df = group_by_intervals(df, interval_seg)
        
        # Plot the latency evolution with averages
        plot_latency(
            destination_directory, 
            grouped_df, 
            f"latency_avg_{interval_seg}s.svg", 
            f"Latency Sequential Read/Write - {interval_seg} Second Averages", 
            "Time (Seconds)", 
            "Average Latency (ms)"
        )

if __name__ == "__main__":
    main()