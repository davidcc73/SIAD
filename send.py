import argparse
import time
from scapy.all import IP, UDP, TCP, Ether, Dot1Q, sendp, Raw

# Set up argument parser
parser = argparse.ArgumentParser(description="Send TCP or UDP packets with optional VLAN tagging")
parser.add_argument('--i', type=float, default=1, help="Interval of sending packets in seconds (default: 1)")
parser.add_argument('--ip', type=str, default="192.168.1.1", help="Destination IP (default: 192.168.1.1)")
parser.add_argument('--size', type=int, default=64, help="Total size of the packet including Ethernet header in bytes (default: 64)")
parser.add_argument('--c', type=int, default=10, help="Number of packets to be sent (default: 10)")
parser.add_argument('--l4', type=str, choices=["TCP", "UDP"], default="UDP", help="Protocol to use: TCP or UDP (default: UDP)")
parser.add_argument('--sport', type=int, default=12345, help="Source port (default: 12345)")
parser.add_argument('--dport', type=int, default=80, help="Destination port (default: 80)")

args = parser.parse_args()

# Function to create the packet
def create_packet():
    # Construct the Ethernet header
    eth = Ether()

    # Create IP header with destination IP
    ip_layer = IP(dst=args.ip)

    # Determine L4 protocol and construct the appropriate layer
    if args.l4 == "UDP":
        l4_layer = UDP(sport=args.sport, dport=args.dport)
    else:
        l4_layer = TCP(sport=args.sport, dport=args.dport)
    
    # Calculate payload size based on specified packet size and add Raw data to meet that size
    base_packet = eth / ip_layer / l4_layer
    payload_size = max(0, args.size - len(base_packet))
    payload = Raw(load="X" * payload_size)
    
    # Combine all layers
    packet = base_packet / payload
    return packet

# Function to send packets
def send_packets():
    packet = create_packet()
    print("Starting packet sending...")
    first_timestamp = None

    for i in range(args.c):
        if i == 0:
            first_timestamp = time.time()  # Record the timestamp of the first packet
            print(f"Timestamp of the first packet sent: {first_timestamp}")

        sendp(packet, verbose=False)
        time.sleep(args.i)
    
    print("Completed sending packets.")

# Execute packet sending
send_packets()
