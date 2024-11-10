import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

# Function to load and process the log file
def load_logs(file_path):
    # Load data with columns: timestamp and packet_size, using ';' as the delimiter
    data = pd.read_csv(file_path, delimiter=";", names=["timestamp", "packet_size"])
    
    # Convert Unix timestamp (float) to datetime format
    data["timestamp"] = pd.to_datetime(data["timestamp"], unit='s')
    data = data.set_index("timestamp")
    return data

# Function to plot bandwidth usage
def plot_bandwidth_usage(avg_bandwidth, peak_bandwidth, file_path='received_packets.csv', output_file='bandwidth_usage.png'):
    # Load the log data
    data = load_logs(file_path)
    
    # Resample data to get the total packet size per second
    bandwidth_usage = data.resample('S').sum()  # Resample by second and sum packet sizes
    
    # Calculate average bandwidth and peak burst size (in bytes)
    avg_bandwidth_value = avg_bandwidth  # Average bandwidth in bytes
    peak_bandwidth_value = peak_bandwidth  # Peak burst size in bytes
    
    # Plotting the graph
    plt.figure(figsize=(10, 6))
    plt.plot(bandwidth_usage.index, bandwidth_usage['packet_size'], label="Bandwidth Usage (bytes)", color="b")
    
    # Plot horizontal lines for average and peak bandwidth
    plt.axhline(avg_bandwidth_value, color='g', linestyle='--', label=f"Average Bandwidth ({avg_bandwidth_value} bytes)")
    plt.axhline(peak_bandwidth_value, color='r', linestyle='--', label=f"Peak Bandwidth ({peak_bandwidth_value} bytes)")
    
    # Adding labels and title
    plt.xlabel("Time")
    plt.ylabel("Bandwidth Usage (bytes)")
    plt.title("Bandwidth Usage per Second")
    plt.grid(True)
    plt.legend()
    
    # Export the graph to a PNG file
    plt.savefig(output_file, format="png")
    plt.close()  # Close the plot to avoid memory issues

# Main function to parse arguments and call the plot function
def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Plot bandwidth usage with traffic shaping values")
    parser.add_argument("avg", type=int, help="Average Bandwidth (in bytes)")
    parser.add_argument("peak", type=int, help="Peak Bandwidth Burst Size (in bytes)")

    # Parse the arguments
    args = parser.parse_args()

    # Call the plot function with the provided arguments
    plot_bandwidth_usage(args.file_path, args.avg, args.peak)

# Run the script
if __name__ == "__main__":
    main()
