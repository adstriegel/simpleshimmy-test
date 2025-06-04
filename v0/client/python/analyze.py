from scapy.all import rdpcap
import argparse
import numpy as np

def extract_gaps(pcap_file):
    packets = rdpcap(pcap_file)
    timestamps = [pkt.time for pkt in packets]
    
    print(f"Total packets: {len(timestamps)}")
    print(f"Inter-packet time gaps (in seconds): ")
    
    for i in range(3, 102):
        gap = timestamps[i] - timestamps[i - 1]
        print(f"Packet {i}: {gap:.6f} seconds")
        
    gaps = np.diff(timestamps[3:101])
    
    average = np.mean(gaps)
    std_deviation = np.std(gaps)
    min_gap = np.min(gaps)
    max_gap = np.max(gaps)
    
    print(f"Average gap: {average:.6f} seconds")
    print(f"Standard deviation: {std_deviation:.6f} seconds")
    print(f"Minimum gap: {min_gap:.6f} seconds")
    print(f"Maximum gap: {max_gap:.6f} seconds")
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract inter-packet time gaps from a pcap.")
    parser.add_argument("pcap_file", help="Path to the pcap")
    
    args = parser.parse_args()
    extract_gaps(args.pcap_file)   
        
