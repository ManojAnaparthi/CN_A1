# server_side.py
import socket
import json

IP_POOL = [
    "192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5",
    "192.168.1.6", "192.168.1.7", "192.168.1.8", "192.168.1.9", "192.168.1.10",
    "192.168.1.11", "192.168.1.12", "192.168.1.13", "192.168.1.14", "192.168.1.15"
]

with open("dns_rules.json", "r") as f:
    RULES = json.load(f)["timestamp_rules"]["time_based_routing"]

def get_time_slot(hour: int) -> str:
    if 4 <= hour <= 11:
        return "morning"
    elif 12 <= hour <= 19:
        return "afternoon"
    else:
        return "night"

def resolve_ip(custom_header: str) -> str:
    hour = int(custom_header[:2])
    seq_id = int(custom_header[-2:])
    slot = get_time_slot(hour)
    rule = RULES[slot]

    pool_start = rule["ip_pool_start"]
    hash_mod = rule["hash_mod"]
    index = pool_start + (seq_id % hash_mod)

    return IP_POOL[index]

def run_server(host="127.0.0.1", port=9999):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"[Server] Listening on {host}:{port}")

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode().strip()

        if "|" not in message:
            continue

        header, domain = message.split("|", 1)
        resolved_ip = resolve_ip(header)

        print(f"[Server] {header} {domain} -> {resolved_ip}")
        sock.sendto(resolved_ip.encode(), addr)

run_server()
