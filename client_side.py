# dns_q_filter.py
import socket
from scapy.all import PcapReader, DNS, DNSQR
from datetime import datetime
import csv

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9999
REPORT_FILE = "dns_report.csv"

def is_valid_domain(domain: str) -> bool:
    d = domain.lower()

    # Skip local/mDNS/service discovery
    if d.endswith(".local"):
        return False
    if d.startswith("_"):
        return False

    # Must have at least one dot (avoid single labels like "localhost")
    if "." not in d:
        return False

    return True

def generate_header(seq_id: int) -> str:
    now = datetime.now()
    header = now.strftime("%H%M%S") + f"{seq_id:02d}"
    return header

def parse_pcap_and_send(pcap_file: str):
    seq_id = 0
    results = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    with PcapReader(pcap_file) as pcap:
        for pkt in pcap:
            if pkt.haslayer(DNS) and pkt[DNS].qr == 0 and pkt.haslayer(DNSQR):
                domain = pkt[DNSQR].qname.decode().rstrip(".")
                if not is_valid_domain(domain):
                    continue
                header = generate_header(seq_id)

                # Prepare message: header + domain name
                message = f"{header}|{domain}"
                sock.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))

                # Receive response
                data, _ = sock.recvfrom(1024)
                resolved_ip = data.decode().strip()

                results.append((header, domain, resolved_ip))
                print(f"[Client] {header} {domain} -> {resolved_ip}")

                seq_id += 1

    sock.close()
    return results

def save_report(results):
    with open(REPORT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Custom Header", "Domain", "Resolved IP"])
        writer.writerows(results)

pcap_file = "0.pcap"
results = parse_pcap_and_send(pcap_file)
save_report(results)
print(f"[Client] Report saved to {REPORT_FILE}")