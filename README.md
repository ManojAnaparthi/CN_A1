# CN_A1

This assignment demonstrates DNS resolution using a client-server setup.  

---

1. Download the sample packet capture file **`0.pcap`** from the following link:  
   [Download 0.pcap](https://drive.google.com/file/d/1Qf0yHBJSEl-UQM6AnlzOpfBtbLFPSK7J/view?usp=drive_link)

2. Run the server script:
   ```bash
   python server_side.py

3. Run the client script:
   ```bash
   python client_side.py

4. You should be able to see these resolutions:

| Custom Header | Domain      | Resolved IP  |
| ------------- | ----------- | ------------ |
| 18041600      | bing.com    | 192.168.1.6  |
| 18041601      | example.com | 192.168.1.7  |
| 18041602      | amazon.com  | 192.168.1.8  |
| 18041603      | yahoo.com   | 192.168.1.9  |
| 18041604      | google.com  | 192.168.1.10 |
| 18041605      | github.com  | 192.168.1.6  |


