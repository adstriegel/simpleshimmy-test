import socket, time, json, threading
import hmac
import hashlib

PORT = 9999
BUFFER_SIZE = 4096
LOG_FILE = "server_log.txt"

NUM_PACKET_TRAINS = 0

AUTHORIZED_USERS = {
    "bertram": "fightingirish"
}

def verify_hmac(key, username, timestamp, payload, received_signature):
    message = f"{username}|{timestamp}|{json.dumps(payload, sort_keys=True)}"
    expected_signature = hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(received_signature, expected_signature)

def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', PORT))
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
            signature = json_data["signature"]
            payload = json_data["payload"]
            
            if username not in AUTHORIZED_USERS:
                print("[-] Unknown user")
                continue
            
            if not verify_hmac(AUTHORIZED_USERS[username], username, timestamp, payload, signature):
                print("[-] Invalid signature")
                continue
            
            print(f"[+] Authenticated request from {username}")
            
            NUM_PACKET_TRAINS = json_data["payload"]["count"]
        
        elif type_byte == 0x02:
            print("Received pattern file from client!")
            
            for packet_train in range(1, NUM_PACKET_TRAINS + 1, 1):
                sequence = json_data[f"{packet_train}"]
                
                num_packets = sequence["num_packets"]
                packet_size = sequence["packets_size"]
                local_gap = sequence["local_gap"] / 1000
                global_gap = sequence["global_gap"] / 1000
                
                for packet in range(num_packets):
                    payload = {
                        "packet_train": packet_train,
                        "packet_id": packet,
                        "timestamp": time.time()
                    }
                    
                    data = json.dumps(payload).encode()
                    data += b' ' * max(0, packet_size - len(data))
                    sock.sendto(data, addr)
                    print(f"Sent packet {packet + 1} of packet train {packet_train} at time {timestamp}")
                    
                    with open("server_log.txt", "a") as log_file:
                        log_file.write(f"Sent packet {packet + 1} of packet train {packet_train} at time {timestamp}\n")
                    time.sleep(local_gap)
            
                time.sleep(global_gap)
            
        
if __name__ == '__main__':
    run_server()


