import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Function to load and process the log file
def load_logs(file_path):
    # Load data with columns: timestamp and packet_size, using ';' as the delimiter
    data = pd.read_csv(file_path, delimiter=";", names=["timestamp", "packet_size"])
    
    # Convert Unix timestamp (float) to datetime format
    data["timestamp"] = pd.to_datetime(data["timestamp"], unit='s')
    data = data.set_index("timestamp")
    
    # Convert packet_size from bytes to kilobits
    data["packet_size"] = (data["packet_size"] * 8 / 1000)   # Convert bytes to kilobits
    
    return data

# Function to track the credit system for burst size and plot the graph
def plot_bandwidth_usage(avg_bandwidth_kbit, peak_bandwidth_kbit, file_path='received_packets.csv', output_file='bandwidth_usage.png'):
    # Load the log data
    data = load_logs(file_path)
    
    # Resample data to get the total packet size per second
    bandwidth_usage = data.resample('S').sum()  # Resample by second and sum packet sizes

    # Plotting the graph
    plt.figure(figsize=(10, 6))
    plt.plot(bandwidth_usage.index, bandwidth_usage['packet_size'], label="Bandwidth Usage (Kbit)", color="b")
    
    # Plot horizontal lines for average and peak bandwidth in Kbits
    plt.axhline(avg_bandwidth_kbit, color='g', linestyle='--', label=f"Defined Average Bandwidth ({avg_bandwidth_kbit:.2f} Kbit)")
    plt.axhline(peak_bandwidth_kbit, color='r', linestyle='--', label=f"Defined Peak Bandwidth ({peak_bandwidth_kbit:.2f} Kbit)")
    
    # Adding labels and title
    plt.xlabel("Time")
    plt.ylabel("Bandwidth Usage (Kbit)")
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
    parser.add_argument("avg", type=float, help="Average Bandwidth (in Kbit)")
    parser.add_argument("peak", type=float, help="Peak Bandwidth Burst Size (in Kbit)")

    # Parse the arguments
    args = parser.parse_args()

    # Call the plot function with the provided arguments
    plot_bandwidth_usage(args.avg, args.peak)

# Run the script
if __name__ == "__main__":
    main()
