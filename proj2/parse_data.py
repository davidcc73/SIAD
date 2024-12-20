import os
import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
import argparse

def parse_lat_log(directory):
    """
    Parses latency log files in the specified directory.
    """
    # Use glob to match files with '_lat.*.log'
    lat_log_pattern = os.path.join(directory, '_lat.*.log')
    lat_log_files = glob.glob(lat_log_pattern)

    if not lat_log_files:
        raise FileNotFoundError(f"No files matching {lat_log_pattern} found.")

    # Load all files into a single DataFrame
    data_frames = []
    for lat_log_path in lat_log_files:
        print(f"Processing file: {lat_log_path}")
        try:
            df = pd.read_csv(lat_log_path, header=None, names=["Index", "Latency", "_", "Block Size", "Status"], usecols=[0, 1, 3, 4])
            df = df.dropna()  # Drop rows with missing values

            # Convert to appropriate types and filter valid rows
            df["Index"] = pd.to_numeric(df["Index"], errors="coerce")
            df["Latency"] = pd.to_numeric(df["Latency"], errors="coerce")
            df["Block Size"] = pd.to_numeric(df["Block Size"], errors="coerce")
            df = df[df["Latency"].notnull()]  # Ensure valid latency values

            data_frames.append(df)
        except Exception as e:
            print(f"Error processing file {lat_log_path}: {e}")

    if not data_frames:
        raise ValueError("No valid data could be extracted from the log files.")

    # Concatenate all data into one DataFrame
    return pd.concat(data_frames, ignore_index=True)

def group_by_intervals(df, interval_seg):
    """
    Groups the data into intervals of 'interval_seg' seconds based on Index
    and calculates the average Latency for each group.
    """
    # Convert Index from milliseconds to seconds
    df["Index"] = df["Index"] / 1000.0

    # Assign rows to time groups
    df["Time Group"] = (df["Index"] // interval_seg) * interval_seg

    # Group by the interval and calculate the mean latency
    grouped = df.groupby("Time Group")["Latency"].mean().reset_index()

    # Rename columns for clarity
    grouped.columns = ["Time Group", "Average Latency Across All Threads"]
    return grouped

def plot_latency(destination_directory, df_grouped, output_filename, title, x_label, y_label):
    """
    Creates and saves a plot of the average latency over time.
    """
    plt.figure()
    plt.plot(df_grouped["Time Group"], df_grouped["Average Latency Across All Threads"])

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)

    # Save the plot
    output_path = os.path.join(destination_directory, output_filename)
    os.makedirs(destination_directory, exist_ok=True)  # Ensure destination directory exists
    plt.savefig(output_path, format="svg")

def main():
    """
    Main function to parse logs, process data, and generate latency plots.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process latency logs and generate latency plots.")
    parser.add_argument("--source_directory", required=True, type=str, help="Path to the source directory containing the latency logs.")
    parser.add_argument("--destination_directory", required=True, type=str, help="Path to the destination directory for output files.")
    parser.add_argument("--interval_seg", required=True, type=int, help="Interval duration in seconds for averaging latency.")
    parser.add_argument("--test_name", required=True, type=str, help="Name of the running test.")
    parser.add_argument("--name_prefix", required=True, type=str, help="Prefix for output graph.")
    parser.add_argument("--id_test", required=True, type=int, help="ID of current scenario")

    args = parser.parse_args()

    try:
        # Parse the latency log
        df = parse_lat_log(args.source_directory)

        # Group data into intervals and compute averages
        grouped_df = group_by_intervals(df, args.interval_seg)

        # Plot the latency evolution with averages
        plot_latency(
            args.destination_directory,
            grouped_df,
            f"{args.name_prefix}_avg_{args.interval_seg}s-ID{args.id_test}.svg",
            f"Latency {args.test_name} - {args.interval_seg} Second Averages",
            "Time (Seconds)",
            "Average Latency (ms)"
        )
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()