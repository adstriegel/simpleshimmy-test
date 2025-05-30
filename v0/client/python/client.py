import socket, json, time
import hmac
import hashlib

SERVER = '127.0.0.1'
PORT = 9999
BUFFER_SIZE = 4096

def generate_hmac(key, username, timestamp, payload_dict):
    message = f"{username}|{timestamp}|{json.dumps(payload_dict, sort_keys=True)}"
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

def load_config(path):
    with open(path, 'r') as f:
        config = json.load(f)
    return config

def run_client(config):
    username = config.pop("username")
    key = config.pop("key")
    timestamp = str(int(time.time()))
    signature = generate_hmac(key, username, timestamp, config)

    request = {
        "username": username,
        "timestamp": timestamp,
        "signature": signature,
        "payload": config
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5.0)

    sock.sendto(json.dumps(request).encode(), (SERVER, PORT))
    response, addr = sock.recvfrom(BUFFER_SIZE)

    print(response)
    if response == "Authenticated":
        print(f"[+] Sent authenticated request as {username}")
    else:
        print(f"[-] Username {username} is not authenticated")

if __name__ == '__main__':
    config = load_config("config.json")
    run_client(config)



