import socket, time, json, threading
import hmac
import hashlib
import argparse
import csv

PORT = 9999
BUFFER_SIZE = 4096
LOG_FILE = "server_log.txt"

NUM_PACKET_TRAINS = 0

AUTHORIZED_USERS = {
    "bertram": "fightingirish"
}

used_nonces = set()

def verify_hmac(key, username, timestamp, payload, received_signature):
    message = f"{username}|{timestamp}|{json.dumps(payload, sort_keys=True)}"
    expected_signature = hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(received_signature, expected_signature)

def is_nonce_fresh(nonce):
    if nonce in used_nonces:
        return False
    used_nonces.add(nonce)
    return True

def append_gap_to_csv(filename, intended_gap, average_gap):
    with open(filename, 'a') as f:
        f.write(f"{intended_gap:.6f},{average_gap:.6f}\n")
        
def run_server(timings, local_gap):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', PORT))
    print(f"[Server] Listening on UDP port {PORT}")

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        
        type_byte = data[0]
        json_byte = data[1:]
        
        json_data = json.loads(json_byte.decode('utf-8'))
        
        if type_byte == 0x01:
            print("Received config file from client!")
            
            username = json_data["username"]
            timestamp = json_data["timestamp"]
            nonce = json_data["nonce"]
            signature = json_data["signature"]
            payload = json_data["payload"]
            
            if username not in AUTHORIZED_USERS:
                print("[-] Unknown user")
                continue
            
            if not verify_hmac(AUTHORIZED_USERS[username], username, timestamp, payload, signature):
                print("[-] Invalid signature")
                continue
            
            if not is_nonce_fresh(nonce):
                print("[-] Reused nonce - possibly replay attack")
                continue
            
            print(f"[+] Authenticated request from {username}")
            
            NUM_PACKET_TRAINS = json_data["payload"]["count"]
        
        elif type_byte == 0x02:
            print("Received pattern file from client!")
            durations = []
            
            for packet_train in range(1, NUM_PACKET_TRAINS + 1, 1): 
                sequence = json_data[f"{packet_train}"]
                
                num_packets = sequence["num_packets"]
                packet_size = sequence["packets_size"]
                local_gap = sequence["local_gap"]
                global_gap = sequence["global_gap"]
                
                for packet in range(num_packets):
                    start_loop = time.time()
                    
                    payload = {
                        "packet_train": packet_train,
                        "packet_id": packet,
                        "timestamp": time.time()
                    }
                    
                    data = json.dumps(payload).encode()
                    data += b' ' * max(0, packet_size - len(data))
					
                    sock.sendto(data, addr)
                    # print(f"Sent packet {packet + 1} of packet train {packet_train} at time {timestamp}")
                    	
                    time.sleep(local_gap)
                    
                    end_loop = time.time()
                    duration = end_loop - start_loop
                    durations.append(duration)
                    
                    # gaps = [duration - local_gap for duration in durations]
                 
                # time.sleep(global_gap)
			
            '''
            with open(timings, 'a') as f:
                for send_duration in send_durations:
                    send_duration *= 1000000
                    f.write(f"{send_duration}\n")
            
            send_durations_micro = [d * 1_000_000 for d in send_durations]
            
            with open(timings, 'a') as f:
                for dur in send_durations_micro:
                    f.write(f"{dur}\n")
            
            '''
            
            intended_gap = local_gap * 1_000_000
            gaps = [(duration - local_gap) * 1_000_000 for duration in durations]
            # durations = [duration * 1_000_000 for duration in durations]
            
            with open(timings, mode="a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                for gap in gaps:
                    writer.writerow([intended_gap, gap])
                
            # send_durations.clear()
            durations.clear()
            
            time.sleep(global_gap)
		
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="UDP Server for Packet Train Transmission")
    parser.add_argument('--timings', type=str, help='Timings directory')
    parser.add_argument('--intended', type=float, help='Intended Gap')
    args = parser.parse_args()
    run_server(args.timings, args.intended)
    
    

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:


