import socket, json, time
import hmac
import hashlib
import uuid
import argparse

BUFFER_SIZE = 4096

def generate_hmac(key, username, timestamp, payload_dict):
    message = f"{username}|{timestamp}|{json.dumps(payload_dict, sort_keys=True)}"
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

def load_config(path):
    with open(path, 'r') as f:
        config = json.load(f)
    return config

def run_client(host, port, config, pattern):
    username = config.pop("username")
    key = config.pop("key")
    timestamp = str(int(time.time()))
    signature = generate_hmac(key, username, timestamp, config)
    nonce = str(uuid.uuid4())
    
    request = {
        "username": username,
        "timestamp": timestamp,
        "nonce": nonce,
        "signature": signature,
        "payload": config
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    json_string = json.dumps(request)
    json_bytes = json_string.encode('utf-8')

    message = b'\x01' + json_bytes
    
    sock.sendto(message, (host, port))
 
    with open('packet_trains.json', 'r') as f:
        patterns = json.load(f)
    
    json_string = json.dumps(patterns)
    json_bytes = json_string.encode('utf-8')
    
    message = b'\x02' + json_bytes
    
    sock.sendto(message, (host, port))

    while True:
        response, addr = sock.recvfrom(BUFFER_SIZE)
        data = json.loads(response.decode())
        
        packet_train = data["packet_train"]
        packet_id = data["packet_id"]
        timestamp = data["timestamp"]
        print(f"Received packet {packet_id + 1} of packet train {packet_train} at time {timestamp}")

        with open("client_log.txt", "a") as log_file:
            log_file.write(f"Received packet {packet_id + 1} of packet train {packet_train} at time {timestamp}\n")

def main():
    parser = argparse.ArgumentParser(description="UDP Client for Packet Train Transmission")
    
    parser.add_argument('--host', type=str, help='Server IP address')
    parser.add_argument('--port', type=int, help='Server port')
    parser.add_argument('--config', type=str, help='Config file to send')
    parser.add_argument('--pattern', type=str, help='Pattern file to send')
    
    args = parser.parse_args()
    
    config = load_config(args.config)
    run_client(args.host, args.port, config, args.pattern)
    
if __name__ == '__main__':
    main()
