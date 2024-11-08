import argparse
import time
from scapy.all import sniff
from scapy.layers.inet import IP, UDP, TCP

# Set up argument parser
parser = argparse.ArgumentParser(description="Receive and log TCP or UDP packets")
parser.add_argument('-l4', type=str, choices=["TCP", "UDP"], default="UDP", help="Protocol to listen to: TCP or UDP (default: UDP)")
parser.add_argument('-sport', type=int, default=12345, help="Source port to listen on (default: 12345)")

args = parser.parse_args()

# Log file for storing received packets information
log_file = "received_packets.log"

# Packet counter
packet_count = 0

# Function to process each packet
def process_packet(packet):
    global packet_count
    protocol = UDP if args.l4 == "UDP" else TCP
    
    # Check if the packet is the right protocol and source port
    if packet.haslayer(protocol) and packet[protocol].sport == args.sport:
        # Increment packet count
        packet_count += 1
        
        # Record the timestamp and size of the packet
        timestamp = time.time()
        packet_size = len(packet)
        
        # Write to log file
        with open(log_file, "a") as f:
            f.write(f"Timestamp: {timestamp}, Packet Size: {packet_size} bytes\n")
        
        print(f"Total packets received: {packet_count}")

# Function to start packet sniffing
def start_sniffing():
    print("Starting to listen for packets...")
    # Define the protocol filter for sniffing
    protocol = "udp" if args.l4 == "UDP" else "tcp"
    # Start sniffing
    sniff(filter=f"{protocol} and src port {args.sport}", prn=process_packet)

# Start the receiving process
start_sniffing()
