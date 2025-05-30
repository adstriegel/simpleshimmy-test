import socket, time, json, threading
import hmac
import hashlib

PORT = 9999
BUFFER_SIZE = 4096
LOG_FILE = "server_log.txt"

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
        request = json.loads(data.decode())
        print(f"Received from {addr}: {data.deocde()}")

        username = request["username"]
        timestamp = request["timestamp"]
        signature = request["signature"]
        payload = request["payload"]

        payload = {
            "status": "OK",
            "train_id": 42
        }

        timestamp = str(int(time.time()))

        message = f"{timestamp}{json.dumps(payload, sort_keys=True)}".encode()

        signature = 

        if username not in AUTHORIZED_USERS:
            print("[-] Unknown user")
            continue
        
        if not verify_hmac(AUTHORIZED_USERS[username], username, timestamp, payload, signature):
            print("[-] Invalid signature")
            continue
        
        sock.sendto("Authenticated", addr) 
        print(f"[+] Authenticated request from {username}")

if __name__ == '__main__':
    run_server()


