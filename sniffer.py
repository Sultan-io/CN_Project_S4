# sniffer.py
# Real-time packet sniffing using Scapy

import threading
from scapy.all import sniff
from packet_processor import parse_packet


class PacketSniffer:
    def __init__(self, packet_callback, stats_callback):
        """
        packet_callback: function called for each packet (adds to logger)
        stats_callback: function called to update statistics
        """
        self.sniffing = False
        self.sniffer_thread = None
        self.packet_callback = packet_callback
        self.stats_callback = stats_callback

    def packet_handler(self, packet):
        """Process each captured packet"""
        if not self.sniffing:
            return

        # Parse the packet
        packet_info = parse_packet(packet)

        if packet_info:
            # Update statistics
            self.stats_callback(packet_info)
            # Add to log
            self.packet_callback(packet_info)

    def start_sniffing(self):
        """Start packet capture in background thread"""
        if self.sniffing:
            return "Already sniffing"

        self.sniffing = True
        # run the _sniff_loop method in this thread, thread will exit automatically when main program exits
        self.sniffer_thread = threading.Thread(target=self._sniff_loop, daemon=True)
        self.sniffer_thread.start()
        return "Sniffing started"

    def _sniff_loop(self):
        """The actual sniffing loop (runs in background)"""
        # Sniff packets (prn is callback for each packet)
        # store=False to not store packets in memory
        sniff(prn=self.packet_handler, store=False, stop_filter=self._should_stop)

    def _should_stop(self, packet):
        """Stop condition for sniffing"""
        return not self.sniffing

    def stop_sniffing(self):
        """Stop packet capture"""
        self.sniffing = False
        if self.sniffer_thread:
            self.sniffer_thread.join(timeout=1)
        return "Sniffing stopped"

    def is_sniffing(self):
        """Check if sniffer is active"""
        return self.sniffing
