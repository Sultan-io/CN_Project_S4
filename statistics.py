# statistics.py
# Maintains all statistical information


class Statistics:
    def __init__(self):
        self.total_packets = 0
        self.protocol_counts = {"TCP": 0, "UDP": 0, "ICMP": 0}
        self.total_bytes = 0
        self.packet_sizes = []

    def update(self, packet_info):
        """Update statistics with a new packet"""
        if not packet_info:
            return

        self.total_packets += 1
        protocol = packet_info["protocol"]
        packet_size = packet_info["packet_size"]

        # Update protocol counts
        if protocol in self.protocol_counts:
            self.protocol_counts[protocol] += 1
        else:
            self.protocol_counts[protocol] = 1

        # Update bytes and sizes for avg calculation
        self.total_bytes += packet_size
        self.packet_sizes.append(packet_size)
        # Keep only last 1000 sizes for memory efficiency
        if len(self.packet_sizes) > 1000:
            self.packet_sizes.pop(0)

    def get_average_packet_size(self):
        """Calculate average packet size"""
        if len(self.packet_sizes) == 0:
            return 0
        return round(sum(self.packet_sizes) / len(self.packet_sizes), 2)

    def get_stats(self):
        """Return all statistics as a dictionary"""
        return {
            "total_packets": self.total_packets,
            "tcp_count": self.protocol_counts.get("TCP", 0),
            "udp_count": self.protocol_counts.get("UDP", 0),
            "icmp_count": self.protocol_counts.get("ICMP", 0),
            "avg_packet_size": self.get_average_packet_size(),
        }

    def reset(self):
        """Reset all statistics"""
        self.total_packets = 0
        self.protocol_counts = {"TCP": 0, "UDP": 0, "ICMP": 0}
        self.total_bytes = 0
        self.packet_sizes = []
