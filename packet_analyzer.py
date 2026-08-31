"""
PACKET ANALYZER MODULE
Team Member: Aswini Jayakumar
"""

from datetime import datetime
from packet_capture import extract_packet_info

def analyze_packet(packet):
    """Analyze a packet and return detailed information"""
    try:
        src_ip, dst_ip, protocol, port = extract_packet_info(packet)
        
        analysis = {
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "protocol": protocol,
            "port": port,
            "size": get_packet_size(packet),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "flags": get_tcp_flags(packet) if protocol == "TCP" else None
        }
        return analysis
        
    except Exception as e:
        print(f"⚠️ Error analyzing packet: {e}")
        return {
            "src_ip": "", "dst_ip": "", "protocol": "Unknown",
            "port": "", "size": 0, "timestamp": "", "flags": None
        }

def get_packet_size(packet):
    try:
        return len(packet) if hasattr(packet, '__len__') else 64
    except:
        return 64

def get_tcp_flags(packet):
    try:
        if hasattr(packet, 'tcp') and packet.tcp is not None:
            flags = []
            if hasattr(packet.tcp, 'flags'):
                flag_value = packet.tcp.flags
                if flag_value & 0x01: flags.append("FIN")
                if flag_value & 0x02: flags.append("SYN")
                if flag_value & 0x04: flags.append("RST")
                if flag_value & 0x10: flags.append("ACK")
                return flags
    except:
        pass
    return None

def is_suspicious(analysis):
    """Check if packet shows suspicious characteristics"""
    suspicious_ports = [22, 23, 445, 3389, 5900, 8080]
    suspicious = False
    reason = ""
    
    if analysis['port'] in suspicious_ports:
        suspicious = True
        reason = f"Suspicious port: {analysis['port']}"
    
    if analysis['protocol'] == "ICMP":
        suspicious = True
        reason = "ICMP packet detected (possible ping sweep)"
    
    return suspicious, reason

if __name__ == "__main__":
    print("🧪 Testing packet analyzer...")
    print("✅ Analyzer ready!")
