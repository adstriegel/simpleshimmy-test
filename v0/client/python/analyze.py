from scapy.all import rdpcap
import argparse
import numpy as np
import math

def extract_gaps(pcap_file, local_gap):
    packets = rdpcap(pcap_file)
    timestamps = [pkt.time for pkt in packets]
    
    print(f"Total packets: {len(timestamps)}")
    print(f"Inter-packet time gaps (in seconds): ")
    
    diff = []
    
    for i in range(3, 102):
        gap = float(timestamps[i]) - float(timestamps[i - 1])
        diff.append(gap)
        print(f"Packet {i}: {gap:.6f} seconds")
      
    average = np.mean(diff)
    std_deviation = np.std(diff)
    min_gap = np.min(diff)
    max_gap = np.max(diff)
    
    print(f"Average gap: {average:.6f} seconds")
    print(f"Standard deviation: {std_deviation:.6f} seconds")
    print(f"Minimum gap: {min_gap:.6f} seconds")
    print(f"Maximum gap: {max_gap:.6f} seconds")
    
    average_microseconds = average * math.pow(10, 6)   
    
    with open("plot.csv", "a") as f:
        f.write(f"{local_gap},{average_microseconds:.1f}\n")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract inter-packet time gaps from a pcap.")
    parser.add_argument('--pcap', type=str, help='PCAP file to analyze')
    parser.add_argument('--gap', type=int, help='The local gap between packets')
    
    args = parser.parse_args()
    extract_gaps(args.pcap, args.gap)   
        
