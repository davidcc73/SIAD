#!/usr/bin/python3

import argparse
import time
import os
from scapy.all import sniff
from scapy.layers.inet import IP, UDP, TCP

# Set up argument parser
parser = argparse.ArgumentParser(description="Receive and log TCP or UDP IPv4 packets")
parser.add_argument('--l4', type=str, choices=["TCP", "UDP"], default="UDP", help="Protocol to listen to: TCP or UDP (default: UDP)")
parser.add_argument('--port', type=int, required=True, help="Port to listen on")
parser.add_argument('--iface', type=str, required=True, help="Network interface to listen on")

args = parser.parse_args()

# Log file for storing received packets information
log_file = "received_packets.log"

# Delete old log file if it exists
if os.path.exists(log_file):
    os.remove(log_file)

# Packet counter
packet_count = 0

# Function to process each packet
def process_packet(packet):
    global packet_count

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
    print(f"Starting to listen for IPv4 packets on interface {args.iface}, port {args.port}...")

    # Define the protocol filter for sniffing
    protocol = "udp" if args.l4 == "UDP" else "tcp"
    # Use scapy's sniff function with a filter for the specified protocol, IPv4, and specified port
    sniff(filter=f"ip and {protocol} and port {args.port}", iface=args.iface, prn=process_packet)

# Start the receiving process
start_sniffing()
