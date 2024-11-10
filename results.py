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
    
    # Convert packet_size from bytes to kilobytes
    data["packet_size"] = data["packet_size"] / 1024  # Convert bytes to kilobytes
    
    return data

# Function to track burst credit and plot bandwidth usage
def plot_bandwidth_usage(avg_bandwidth, peak_bandwidth, file_path='received_packets.csv', output_file='bandwidth_usage.png'):
    # Load the log data
    data = load_logs(file_path)
    
    # Resample data to get the total packet size per second
    bandwidth_usage = data.resample('S').sum()  # Resample by second and sum packet sizes
    
    # Initialize burst credit
    burst_credit = 0
    burst_credit_history = []
    usage_exceeded = []
    
    # Iterate over the bandwidth usage to apply the credit system
    for index, row in bandwidth_usage.iterrows():
        current_bandwidth = row['packet_size']
        
        if current_bandwidth < avg_bandwidth:
            # If usage is below average, add to the burst credit
            burst_credit += (avg_bandwidth - current_bandwidth)
            burst_credit = min(burst_credit, peak_bandwidth)  # Credit can't exceed peak burst size
        elif current_bandwidth > avg_bandwidth:
            # If usage exceeds average, use burst credit if available
            if burst_credit >= (current_bandwidth - avg_bandwidth):
                burst_credit -= (current_bandwidth - avg_bandwidth)
                usage_exceeded.append(False)  # Burst size respected
            else:
                usage_exceeded.append(True)  # Burst size exceeded
                burst_credit = 0  # Deplete the credit
        else:
            usage_exceeded.append(False)  # Usage exactly equal to average
        
        burst_credit_history.append(burst_credit)
    
    # Plotting the graph
    plt.figure(figsize=(10, 6))
    plt.plot(bandwidth_usage.index, bandwidth_usage['packet_size'], label="Bandwidth Usage (KB)", color="b")
    
    # Plot horizontal lines for average and peak bandwidth
    plt.axhline(avg_bandwidth, color='g', linestyle='--', label=f"Defined Average Bandwidth ({avg_bandwidth:.2f} KB)")
    plt.axhline(peak_bandwidth, color='r', linestyle='--', label=f"Defined Peak Bandwidth ({peak_bandwidth:.2f} KB)")
    
    # Highlight when burst size was exceeded
    for i, exceeded in enumerate(usage_exceeded):
        if exceeded:
            plt.axvline(bandwidth_usage.index[i], color='orange', linestyle=':', label="Burst Size Exceeded" if i == 0 else "")
    
    # Adding labels and title
    plt.xlabel("Time")
    plt.ylabel("Bandwidth Usage (KB)")
    plt.title("Bandwidth Usage per Second (with Burst Credit)")
    plt.grid(True)
    plt.legend()
    
    # Export the graph to a PNG file
    plt.savefig(output_file, format="png")
    plt.close()  # Close the plot to avoid memory issues

# Main function to parse arguments and call the plot function
def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Plot bandwidth usage with traffic shaping values")
    parser.add_argument("avg", type=float, help="Average Bandwidth (in KB)")
    parser.add_argument("peak", type=float, help="Peak Bandwidth Burst Size (in KB)")

    # Parse the arguments
    args = parser.parse_args()

    # Call the plot function with the provided arguments
    plot_bandwidth_usage(args.avg, args.peak)

# Run the script
if __name__ == "__main__":
    main()
