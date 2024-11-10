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

# Function to plot bandwidth usage
def plot_bandwidth_usage(file_path, output_file="bandwidth_usage.png"):
    # Load the log data
    data = load_logs(file_path)
    
    # Resample data to get the total packet size per second
    bandwidth_usage = data.resample('S').sum()  # Resample by second and sum packet sizes
    
    # Plotting the graph
    plt.figure(figsize=(10, 6))
    plt.plot(bandwidth_usage.index, bandwidth_usage['packet_size'], label="Bandwidth Usage (bytes)", color="b")
    
    # Adding labels and title
    plt.xlabel("Time")
    plt.ylabel("Bandwidth Usage (bytes)")
    plt.title("Bandwidth Usage per Second")
    plt.grid(True)
    plt.legend()
    
    # Export the graph to a PNG file
    plt.savefig(output_file, format="png")
    plt.close()  # Close the plot to avoid memory issues

# Example usage
file_path = 'log_file.csv'  # Replace with your actual log file path
plot_bandwidth_usage(file_path, output_file="bandwidth_usage.png")
