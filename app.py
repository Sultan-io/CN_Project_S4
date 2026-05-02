# app.py
# Main Flask application with routes for start/stop monitoring

from flask import Flask, render_template, request, jsonify
from sniffer import PacketSniffer
from logger import PacketLogger
from statistics import Statistics
import threading

app = Flask(__name__)

# Global objects
packet_logger = PacketLogger(max_logs=500)
stats = Statistics()
sniffer = None
sniffer_lock = threading.Lock()


def packet_callback(packet_info):
    """Called by sniffer for each packet - adds to logger"""
    packet_logger.add_packet(packet_info)


def stats_callback(packet_info):
    """Called by sniffer for each packet - updates statistics"""
    stats.update(packet_info)


@app.route("/")
def index():
    """Serve the main HTML interface"""
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_monitoring():
    """Start real-time packet sniffing"""
    global sniffer

    with sniffer_lock:
        if sniffer is not None and sniffer.is_sniffing():
            return jsonify({"status": "error", "message": "Already monitoring!"})

        # Create and start new sniffer
        sniffer = PacketSniffer(packet_callback, stats_callback)
        result = sniffer.start_sniffing()
        return jsonify({"status": "success", "message": result})


@app.route("/stop", methods=["POST"])
def stop_monitoring():
    """Stop packet sniffing"""
    global sniffer

    with sniffer_lock:
        if sniffer is None or not sniffer.is_sniffing():
            return jsonify({"status": "error", "message": "Not currently monitoring!"})

        result = sniffer.stop_sniffing()
        return jsonify({"status": "success", "message": result})


@app.route("/get_data", methods=["GET"])
def get_data():
    """Get current packet logs, statistics, and filter options"""

    # Get filter parameters from request
    protocol = request.args.get("protocol", "ALL")
    src_ip = request.args.get("src_ip", "")
    dst_ip = request.args.get("dst_ip", "")

    # Apply filters to get filtered logs
    filtered_logs = packet_logger.filter_logs(protocol, src_ip, dst_ip)

    # Get current statistics
    current_stats = stats.get_stats()

    return jsonify(
        {
            "logs": filtered_logs,
            "statistics": current_stats,
            "total_logs": len(packet_logger.get_all_logs()),
            "filtered_count": len(filtered_logs),
        }
    )


@app.route("/clear_logs", methods=["POST"])
def clear_logs():
    """Clear all packet logs"""
    packet_logger.clear_logs()
    return jsonify({"status": "success", "message": "Logs cleared!"})


@app.route("/reset_stats", methods=["POST"])
def reset_stats():
    """Reset all statistics"""
    stats.reset()
    return jsonify({"status": "success", "message": "Statistics reset!"})


@app.route("/export_csv", methods=["GET"])
def export_csv():
    """Export all packet logs to CSV format"""
    import csv
    from io import StringIO
    from flask import Response

    # Get all logs (without filters for full export)
    all_logs = packet_logger.get_all_logs()

    # Create CSV in memory
    output = StringIO()
    writer = csv.writer(output)

    # Write header row
    writer.writerow(
        [
            "Timestamp",
            "Source IP",
            "Destination IP",
            "Protocol",
            "Packet Size (bytes)",
            "Source Port",
            "Destination Port",
            "Service",
        ]
    )

    # Write data rows
    for log in all_logs:
        writer.writerow(
            [
                log["timestamp"],
                log["src_ip"],
                log["dst_ip"],
                log["protocol"],
                log["packet_size"],
                log["src_port"],
                log["dst_port"],
                log["service"],
            ]
        )

    # Prepare response
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=network_traffic_export.csv"
        },
    )


if __name__ == "__main__":
    print("=" * 50)
    print("Network Traffic Monitoring Platform")
    print("=" * 50)
    print("\n⚠️  IMPORTANT NOTES:")
    print("1. Run this script with ADMIN/SUDO privileges!")
    print("2. On Windows: Run as Administrator")
    print("3. On Linux/Mac: sudo python app.py")
    print("\n🌐 Starting web server at: http://localhost:5000")
    print("=" * 50)

    # Run Flask app
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
