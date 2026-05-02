# logger.py
# Stores packet logs with timestamps

from datetime import datetime


class PacketLogger:
    def __init__(self, max_logs=500):
        self.logs = []  # List of packet records
        self.max_logs = max_logs

    def add_packet(self, packet_info):
        """Add a packet to the log with timestamp"""
        if not packet_info:
            return

        log_entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "src_ip": packet_info["src_ip"],
            "dst_ip": packet_info["dst_ip"],
            "protocol": packet_info["protocol"],
            "packet_size": packet_info["packet_size"],
            "src_port": packet_info["src_port"],
            "dst_port": packet_info["dst_port"],
            "service": packet_info["service"],
        }

        self.logs.insert(0, log_entry)  # Newest first

        # Keep only last max_logs entries
        if len(self.logs) > self.max_logs:
            self.logs = self.logs[: self.max_logs]

    def get_all_logs(self):
        """Return all logs"""
        return self.logs

    def clear_logs(self):
        """Clear all logs"""
        self.logs = []

    def filter_logs(self, protocol=None, src_ip=None, dst_ip=None):
        """Return filtered logs based on criteria"""
        filtered = self.logs

        if protocol and protocol != "ALL":
            filtered = [log for log in filtered if log["protocol"] == protocol]

        if src_ip and src_ip.strip():
            filtered = [log for log in filtered if src_ip in log["src_ip"]]

        if dst_ip and dst_ip.strip():
            filtered = [log for log in filtered if dst_ip in log["dst_ip"]]

        return filtered
