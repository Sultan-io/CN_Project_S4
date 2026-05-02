# packet_processor.py
# Maps ports to services and processes raw packet data


def get_service(port, protocol):
    """Map port number to service name"""
    service_map = {
        80: "HTTP",
        443: "HTTPS",
        53: "DNS",
        21: "FTP",
        22: "SSH",
        23: "TELNET",
        25: "SMTP",
        110: "POP3",
        143: "IMAP",
        3306: "MySQL",
        5432: "PostgreSQL",
        27017: "MongoDB",
        8080: "HTTP-ALT",
        3389: "RDP",
        445: "SMB",
    }

    if port in service_map:
        return service_map[port]
    else:
        return "Unknown" if port == 0 else f"Port-{port}"


def parse_packet(packet):
    """
    Extract relevant fields from a Scapy packet
    Returns a dictionary or None if not IP packet
    """
    try:
        from scapy.all import IP, TCP, UDP, ICMP

        if IP not in packet:
            return None

        ip_layer = packet[IP]
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        protocol_num = ip_layer.proto
        packet_size = len(packet)

        # Protocol type mapping
        protocol_map = {6: "TCP", 17: "UDP", 1: "ICMP"}
        protocol = protocol_map.get(protocol_num, f"Other({protocol_num})")

        # Port and service extraction
        src_port = None
        dst_port = None
        service = "N/A"

        if TCP in packet:
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            # Use destination port for service mapping
            service = get_service(dst_port, "TCP")
        elif UDP in packet:
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
            service = get_service(dst_port, "UDP")
        elif ICMP in packet:
            service = "ICMP-Ping"

        # For non-TCP/UDP packets, still return valid data
        if src_port is None:
            src_port = 0
        if dst_port is None:
            dst_port = 0

        return {
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "protocol": protocol,
            "packet_size": packet_size,
            "src_port": src_port,
            "dst_port": dst_port,
            "service": service,
        }

    except Exception as e:
        # Silently ignore malformed packets
        return None
