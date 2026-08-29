from scapy.all import sniff, IP, TCP, UDP, ICMP
import time
from datetime import datetime

def extract_packet_info(packet):
    """Extract packet information"""
    if not packet.haslayer(IP):
        return None
    
    ip_layer = packet[IP]
    src_ip = ip_layer.src
    dst_ip = ip_layer.dst
    
    if packet.haslayer(TCP):
        protocol = 'tcp'
        port = packet[TCP].dport
    elif packet.haslayer(UDP):
        protocol = 'udp'
        port = packet[UDP].dport
    elif packet.haslayer(ICMP):
        protocol = 'icmp'
        port = None
    else:
        protocol = 'other'
        port = None
    
    return {
        'src_ip': src_ip,
        'dst_ip': dst_ip,
        'protocol': protocol,
        'port': port,
        'timestamp': time.time()
    }

def display_packet(info):
    """Display packet in readable format"""
    timestamp = datetime.fromtimestamp(info['timestamp']).strftime('%H:%M:%S')
    port_str = f":{info['port']}" if info['port'] else ""
    print(f"[{timestamp}] {info['src_ip']} → {info['dst_ip']} [{info['protocol']}{port_str}]")

def capture_live_packets(count=15):
    """Capture REAL packets from your network"""
    print("=" * 60)
    print("🔴 LIVE PACKET CAPTURE")
    print("📦 Capturing", count, "packets from your network...")
    print("💡 Open a browser or ping a website to generate traffic!")
    print("=" * 60)
    print()
    
    packet_count = 0
    
    def packet_handler(packet):
        nonlocal packet_count
        info = extract_packet_info(packet)
        if info:
            display_packet(info)
            packet_count += 1
            if packet_count >= count:
                return True
    
    try:
        sniff(
            prn=packet_handler,
            store=False,
            count=count,
            timeout=30
        )
        print()
        print("=" * 60)
        print("✅ Live capture complete!")
        print("📊 Captured", packet_count, "packets")
        print("=" * 60)
    except PermissionError:
        print()
        print("❌ PERMISSION DENIED!")
        print("Please run with sudo: sudo python3 live_capture.py")
    except Exception as e:
        print("❌ Error:", e)

# ================================================================
# RUN LIVE CAPTURE
# ================================================================
if __name__ == "__main__":
    capture_live_packets(count=15)
