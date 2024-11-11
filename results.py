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
def plot_bandwidth_usage(avg_bandwidth_kbit, peak_bandwidth_kbit, burst_credit_kb, file_path='received_packets.csv', output_file='bandwidth_usage.png'):
    # Convert average and peak bandwidth from Kbits to KBytes for internal calculations
    avg_bandwidth = avg_bandwidth_kbit * 1000 / 8 / 1024
    peak_bandwidth = peak_bandwidth_kbit * 1000 / 8 / 1024

    # Load the log data
    data = load_logs(file_path)
    
    # Resample data to get the total packet size per second
    bandwidth_usage = data.resample('S').sum()  # Resample by second and sum packet sizes

    # Initialize credit and burst exceeded tracking
    current_credit = burst_credit_kb
    burst_exceeded = []  # List to store burst exceeded information

    # Iterate over each second of bandwidth usage
    for i, row in bandwidth_usage.iterrows():
        # If bandwidth usage is below the average, the credit is replenished
        if row['packet_size'] < avg_bandwidth:
            # Add credit if there's bandwidth under the average
            current_credit = min(current_credit + (avg_bandwidth - row['packet_size']), burst_credit_kb)
            burst_exceeded.append(0)  # Burst not exceeded
        elif row['packet_size'] > avg_bandwidth:
            
            # If usage exceeds the average bandwidth, check if there is enough credit
            if row['packet_size'] > avg_bandwidth + current_credit:
                current_credit = 0  # Reset credit to 0
                burst_exceeded.append(1)  # Burst exceeded
            else:  # Burst not exceeded
                current_credit -= (row['packet_size'] - avg_bandwidth)  # Use burst credit for the excess bandwidth
                burst_exceeded.append(0)
        else:  # Burst not exceeded (equal to average bandwidth)
            burst_exceeded.append(0)  # No excess, burst not exceeded

    # Ensure the burst_exceeded list matches the length of bandwidth_usage DataFrame
    if len(burst_exceeded) != len(bandwidth_usage):
        # In case of mismatch, pad the list to match the length
        burst_exceeded.extend([0] * (len(bandwidth_usage) - len(burst_exceeded)))

    # Add the burst exceeded status to the bandwidth usage data for plotting
    bandwidth_usage['burst_exceeded'] = burst_exceeded

    # Plotting the graph
    plt.figure(figsize=(10, 6))
    plt.plot(bandwidth_usage.index, bandwidth_usage['packet_size'], label="Bandwidth Usage (Kbit)", color="b")
    
    # Plot horizontal lines for average and peak bandwidth in Kbits
    plt.axhline(avg_bandwidth_kbit, color='g', linestyle='--', label=f"Defined Average Bandwidth ({avg_bandwidth_kbit:.2f} Kbit)")
    plt.axhline(peak_bandwidth_kbit, color='r', linestyle='--', label=f"Defined Peak Bandwidth ({peak_bandwidth_kbit:.2f} Kbit)")
    
    # Highlight periods where burst credit was exceeded
    exceeded_times = bandwidth_usage[bandwidth_usage['burst_exceeded'] == 1]
    plt.scatter(exceeded_times.index, exceeded_times['packet_size'], color='red', label="Burst Size Exceeded", zorder=5)
    
    # Add the burst credit label in the legend without color
    plt.plot([], [], color='none', label=f"Defined Burst Credit ({(burst_credit_kb * 1000 * 8 / 1024):.2f} KB = {burst_credit_kb:.2f} Kb)")  # Invisible line for label
    
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
    parser.add_argument("burst_credit", type=float, help="Burst Credit Size (in KB)")

    # Parse the arguments
    args = parser.parse_args()

    # Call the plot function with the provided arguments
    plot_bandwidth_usage(args.avg, args.peak, args.burst_credit * 1024 * 8 / 1000)  # Convert burst credit from KB to Kbit

# Run the script
if __name__ == "__main__":
    main()
