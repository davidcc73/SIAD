import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to load and process the log file
def load_logs(file_path):
    # Load data with columns: timestamp and packet_size
    data = pd.read_csv(file_path, names=["timestamp", "packet_size"])
    data["timestamp"] = pd.to_datetime(data["timestamp"])  # Convert timestamp to datetime
    data = data.set_index("timestamp")
    return data

# Calculate average bandwidth over time
def calculate_moving_average(data, window='1S'):
    data['bandwidth'] = data['packet_size'].resample(window).sum()  # Packet sizes summed per second
    data['moving_average'] = data['bandwidth'].rolling(window='5S', min_periods=1).mean()  # 5-second moving average
    return data

# Calculate cumulative bandwidth for burst analysis
def calculate_cumulative_bandwidth(data):
    data['cumulative_bandwidth'] = data['packet_size'].cumsum()
    return data

# Plot average bandwidth to check if it adheres to the defined limit
def plot_average_bandwidth(data, avg_bandwidth_limit):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['moving_average'], label="Moving Average Bandwidth", color="blue")
    plt.axhline(y=avg_bandwidth_limit, color='green', linestyle='--', label="Average Bandwidth Limit")
    plt.xlabel("Time")
    plt.ylabel("Bandwidth (Bytes/sec)")
    plt.title("Average Bandwidth Over Time")
    plt.legend()
    plt.grid()
    plt.savefig("average_bandwidth.png")

# Plot peak bandwidth to verify peak limit adherence
def plot_peak_bandwidth(data, peak_bandwidth_limit):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['bandwidth'], label="Bandwidth Per Second", color="purple")
    plt.axhline(y=peak_bandwidth_limit, color='red', linestyle='--', label="Peak Bandwidth Limit")
    plt.xlabel("Time")
    plt.ylabel("Bandwidth (Bytes/sec)")
    plt.title("Peak Bandwidth Over Time")
    plt.legend()
    plt.grid()
    plt.savefig("peak_bandwidth.png")

# Plot cumulative bandwidth to visualize burst size compliance
def plot_cumulative_bandwidth(data, burst_size_limit):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['cumulative_bandwidth'], label="Cumulative Bandwidth", color="orange")
    plt.axhline(y=burst_size_limit, color='red', linestyle='--', label="Burst Size Limit")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Bandwidth (Bytes)")
    plt.title("Cumulative Bandwidth Over Time")
    plt.legend()
    plt.grid()
    plt.savefig("cumulative_bandwidth.png")

# Main function to run all processes and export graphs
def analyze_traffic_shaping(file_path, avg_bandwidth_limit, peak_bandwidth_limit, burst_size_limit):
    data = load_logs(file_path)

    # Define total time window
    total_time_window = data.index[-1] - data.index[0]

    # Calculate bandwidth and moving average for average bandwidth analysis
    data = calculate_moving_average(data)

    # Calculate cumulative bandwidth for burst size analysis
    data = calculate_cumulative_bandwidth(data)

    # Generate and save plots
    plot_average_bandwidth(data, avg_bandwidth_limit)
    plot_peak_bandwidth(data, peak_bandwidth_limit)
    plot_cumulative_bandwidth(data, burst_size_limit)

    print("Analysis complete. Graphs have been saved as PNG files.")

# Run the analysis (replace with actual file path and bandwidth limits)
file_path = "received_packets.csv"  # Path to your log file
avg_bandwidth_limit = 5000     # Example average bandwidth limit (bytes per second)
peak_bandwidth_limit = 8000   # Example peak bandwidth limit (bytes per second)
burst_size_limit = 16000      # Example burst size limit (bytes)

analyze_traffic_shaping(file_path, avg_bandwidth_limit, peak_bandwidth_limit, burst_size_limit)