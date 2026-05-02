# Network Traffic Monitoring and Analysis Platform

## Project Overview

A real-time network traffic monitoring platform that captures, logs, and analyzes network packets. The system provides a web-based interface to start/stop monitoring, view packet details, apply filters, and export captured data. This project demonstrates fundamental concepts of network monitoring, packet analysis, and web-based visualization.

## Features

### Core Functionality
- **Real-time Packet Capture** - Captures live network traffic using Scapy (not simulated CSV data)
- **Start/Stop Monitoring** - Control packet capture with dedicated buttons
- **Live Statistics Display** - Shows total packets, TCP/UDP/ICMP counts, and average packet size
- **Packet Logging** - Displays captured packets with timestamps in a sortable table
- **Port-to-Service Mapping** - Maps common ports to services (HTTP, DNS, HTTPS, FTP, SSH, etc.)

### Filtering Capabilities
- **Protocol Filter** - Filter by TCP, UDP, or ICMP
- **Source IP Filter** - Filter packets by source IP address (partial matching supported)
- **Destination IP Filter** - Filter packets by destination IP address (partial matching supported)
- **Reset Filter** - Clear all filters and show all packets

### Data Export
- **CSV Export** - Export captured packet data to CSV format for offline analysis

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.x | Backend programming language |
| Flask | Web framework for REST API and serving HTML |
| Scapy | Packet sniffing and parsing library |
| HTML5 | Web interface structure |
| CSS3 | Styling and responsive design |
| JavaScript | Client-side interactions and AJAX polling |

## Project Structure

```
network_monitoring_project/
│
├── app.py                  # Main Flask application with API routes
├── sniffer.py              # Real-time packet sniffing with threading
├── packet_processor.py     # Packet parsing and port-to-service mapping
├── statistics.py           # Statistics tracking and calculation
├── logger.py               # Packet logging and filtering logic
├── filters.py              # IP validation helper functions
│
├── templates/
│   └── index.html          # Web interface
│
├── static/
│   └── style.css           # CSS styling
│
├── README.md               # This file
└── network_dataset.csv     # Sample dataset (exports also available)
```

## Installation

### Prerequisites

- Python 3.7 or higher
- Administrator/root privileges (required for packet sniffing)
- Internet connection (for library installation)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/network-traffic-monitor.git
cd network-traffic-monitor
```

### Step 2: Install Python Dependencies

```bash
pip install flask
pip install scapy
```

### Step 3: Install Packet Capture Library

**For Windows:**
- Download and install [Npcap](https://npcap.com/)
- During installation, check "Install in WinPcap API-compatible Mode"

**For Linux:**
```bash
sudo apt-get install libpcap-dev
```

**For macOS:**
```bash
brew install libpcap
```

## How to Run

### Windows (Administrator Mode)

1. Open Command Prompt as Administrator
2. Navigate to project directory
3. Run:

```bash
python app.py
```

### Linux/macOS (sudo)

```bash
sudo python3 app.py
```

### Access the Web Interface

Open your browser and navigate to: `http://localhost:5000`

## Usage Guide

### 1. Start Monitoring
Click the **"Start Monitoring"** button. The system will begin capturing live network traffic from your active network interface.

### 2. Generate Test Traffic
To see packets in action, generate some network activity:
- Open websites in your browser (generates TCP packets on ports 80/443)
- Run ping commands: `ping google.com -t` (generates ICMP packets)
- Stream video or download files

### 3. View Statistics
The statistics panel shows:
- **Total Packets** - Overall packet count since monitoring started
- **TCP/UDP/ICMP Counts** - Protocol-specific breakdown
- **Average Packet Size** - Mean packet size in bytes

### 4. Apply Filters
- Select a **Protocol** from the dropdown (TCP/UDP/ICMP/All)
- Enter **Source IP** or **Destination IP** (partial matches work, e.g., "192.168")
- Click **"Apply Filter"** to see filtered results
- Click **"Reset Filter"** to clear all filters

### 5. Export Data
Click **"Export as CSV"** to download all captured packets as a CSV file for offline analysis.

### 6. Stop Monitoring
Click **"Stop Monitoring"** to halt packet capture. Statistics and logs remain visible.

### 7. Clear Data
- **Clear Logs** - Removes all packet records from the table
- **Reset Stats** - Resets all statistics counters

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the web interface |
| `/start` | POST | Starts packet sniffing |
| `/stop` | POST | Stops packet sniffing |
| `/get_data` | GET | Returns logs, statistics, and filtered results |
| `/export_csv` | GET | Exports packet logs as CSV |
| `/clear_logs` | POST | Clears all packet logs |
| `/reset_stats` | POST | Resets all statistics counters |

## Port-to-Service Mapping

| Port | Service |
|------|---------|
| 80 | HTTP |
| 443 | HTTPS |
| 53 | DNS |
| 21 | FTP |
| 22 | SSH |
| 23 | TELNET |
| 25 | SMTP |
| 110 | POP3 |
| 143 | IMAP |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 8080 | HTTP-ALT |
| 3389 | RDP |
| 445 | SMB |

## Troubleshooting

### "No module named scapy"
```bash
pip install scapy
```

### "Permission denied" (Linux/macOS)
Run with sudo: `sudo python3 app.py`

### "Template not found"
Ensure folder is named `templates` (with 's') and contains `index.html`

### No packets appearing
- Verify you're running as Administrator/sudo
- Check Npcap is installed (Windows)
- Generate network traffic (ping, browse web)

### Scapy import error on Windows
Install Npcap from https://npcap.com and restart your computer

## Learning Outcomes

Through this project, I learned:

1. **Network Fundamentals** - Understanding TCP, UDP, ICMP protocols and port numbers
2. **Packet Analysis** - Using Scapy to parse network packets in real-time
3. **Web Development** - Building a Flask backend with HTML/CSS frontend
4. **Multithreading** - Running packet sniffer in background thread while serving web requests
5. **Data Visualization** - Displaying live statistics and logs in a user-friendly interface
6. **System Programming** - Working with administrator privileges and network interfaces

## Extensions Implemented (Bonus)

- ✅ **Real-time packet sniffing** (not simulated CSV data)
- ✅ **CSV export functionality**
- ✅ **Port-to-service mapping** for 15+ common services

## Future Improvements

- Add packet details view (headers, payload)
- Implement live bandwidth usage graph
- Add option to select network interface
- Support for IPv6 packets
- Save packet captures to PCAP format
- Implement packet capture filters (BPF filters)

## License

This project is submitted for academic purposes as part of the Computer Networks course.

## Acknowledgments

- Scapy documentation for packet manipulation
- Flask documentation for web framework
```