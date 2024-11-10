import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to load and process the log file
def load_logs(file_path):
    # Load data with columns: timestamp and packet_size, using ';' as the delimiter
    data = pd.read_csv(file_path, delimiter=";", names=["timestamp", "packet_size"])
    
    # Convert Unix timestamp (float) to datetime format
    data["timestamp"] = pd.to_datetime(data["timestamp"], unit='s')
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

# Plot bandwidth usage per second
def plot_bandwidth_usage_per_second(data):
    # Group and sum data per second to get bandwidth usage per second
    data_per_second = data['packet_size'].resample('1S').sum()
    
    plt.figure(figsize=(12, 6))
    plt.plot(data_per_second.index, data_per_second, label="Usage per Second", color="blue")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Bandwidth (Bytes)")
    plt.title("Bandwidth Usage Per Second Over Time")
    plt.legend()
    plt.grid()
    plt.savefig("bandwidth_usage_per_second.png")

# Main function to run all processes and export graphs
def main():
    # Run the analysis (replace with actual file path and bandwidth limits)
    file_path = "received_packets.csv"  # Path to your log file
    peak_bandwidth_limit = 8000    # Example peak bandwidth limit (bytes per second)
    burst_size_limit = 16000       # Example burst size limit (bytes)

    data = load_logs(file_path)

    # Calculate bandwidth and moving average for average bandwidth analysis
    data = calculate_moving_average(data)

    # Calculate cumulative bandwidth for burst size analysis
    data = calculate_cumulative_bandwidth(data)

    # Generate and save plots
    plot_bandwidth_usage_per_second(data)

    print("Analysis complete. Graphs have been saved as PNG files.")


main()
