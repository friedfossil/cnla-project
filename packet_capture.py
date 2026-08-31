"""
PACKET CAPTURE MODULE
Team Member: Aswini Jayakumar
"""

import scapy.all as scapy
import time
import random
import threading

SIMULATION_MODE = False
SIMULATION_RUNNING = True
PACKET_LIMIT = 15

def capture_packets(callback):
    global SIMULATION_MODE
    
    print("🛡️ Starting packet capture...")
    
    try:
        print("📡 Attempting real packet capture...")
        scapy.sniff(prn=callback, store=False, count=PACKET_LIMIT) 
        print("✅ Captured 15 packets! Capture complete.")
    except Exception as e:
        print(f"⚠️ Real capture failed: {e}")
        print("🔄 Switching to SIMULATION mode...")
        SIMULATION_MODE = True
        simulate_packets(callback)

def simulate_packets(callback):
    global SIMULATION_RUNNING
    
    fake_ips = [
        "192.168.1.10", "192.168.1.20", "10.0.0.5", 
        "172.16.0.100", "8.8.8.8", "192.168.1.1",
        "10.0.0.1", "172.16.1.50", "192.168.2.15"
    ]
    fake_ports = [80, 443, 22, 21, 8080, 53, 3306, 25, 110]
    protocols = ["TCP", "UDP", "ICMP"]
    
    print("🔄 Generating simulated network traffic...")
    packet_count = 0
    
    while SIMULATION_RUNNING and packet_count < PACKET_LIMIT:
        try:
            src_ip = random.choice(fake_ips)
            dst_ip = random.choice(fake_ips)
            protocol = random.choice(protocols)
            port = random.choice(fake_ports) if protocol != "ICMP" else ""
            
            packet = create_mock_packet(src_ip, dst_ip, protocol, port)
            callback(packet)
            packet_count += 1
            
            if packet_count % 10 == 0:
                print(f"📊 Simulated {packet_count} packets...")
            
            time.sleep(random.uniform(0.3, 1.5))
            
        except KeyboardInterrupt:
            print("⏹️ Stopping packet simulation...")
            break
        except Exception as e:
            print(f"⚠️ Simulation error: {e}")
            time.sleep(1)
    print("✅ Simulation complete!")

def create_mock_packet(src_ip, dst_ip, protocol, port):
    class MockPacket:
        def __init__(self, src, dst, proto, port_num):
            self.src_ip = src
            self.dst_ip = dst
            self.protocol = proto
            self.port = port_num
            
            class IP:
                def __init__(self, s, d):
                    self.src = s
                    self.dst = d
            self.ip = IP(src, dst)
            
            if proto in ["TCP", "UDP"]:
                class PortLayer:
                    def __init__(self, p):
                        self.sport = p
                        self.dport = p
                self.tcp = PortLayer(port_num) if proto == "TCP" else None
                self.udp = PortLayer(port_num) if proto == "UDP" else None
            else:
                self.tcp = None
                self.udp = None
                class ICMP:
                    def __init__(self):
                        self.type = 8
                self.icmp = ICMP()
        
        def haslayer(self, layer):
            layer_name = layer.__name__
            if layer_name == "IP":
                return True
            if layer_name == "TCP" and self.tcp is not None:
                return True
            if layer_name == "UDP" and self.udp is not None:
                return True
            if layer_name == "ICMP" and self.protocol == "ICMP":
                return True
            return False
        
        def __getitem__(self, key):
            layer_name = key.__name__
            if layer_name == "IP":
                return self.ip
            if layer_name == "TCP":
                return self.tcp
            if layer_name == "UDP":
                return self.udp
            if layer_name == "ICMP":
                return self.icmp if self.protocol == "ICMP" else None
            return None
    
    return MockPacket(src_ip, dst_ip, protocol, port)

def extract_packet_info(packet):
    try:
        src_ip = ""
        dst_ip = ""
        protocol = "Unknown"
        port = ""
        
        if hasattr(packet, 'ip'):
            src_ip = getattr(packet.ip, 'src', '')
            dst_ip = getattr(packet.ip, 'dst', '')
        elif hasattr(packet, 'src_ip'):
            src_ip = getattr(packet, 'src_ip', '')
            dst_ip = getattr(packet, 'dst_ip', '')
        
        if hasattr(packet, 'tcp') and packet.tcp is not None:
            protocol = "TCP"
            port = getattr(packet.tcp, 'sport', '')
        elif hasattr(packet, 'udp') and packet.udp is not None:
            protocol = "UDP"
            port = getattr(packet.udp, 'sport', '')
        elif hasattr(packet, 'icmp') and packet.icmp is not None:
            protocol = "ICMP"
        elif hasattr(packet, 'protocol'):
            protocol = str(packet.protocol)
        
        return (src_ip, dst_ip, protocol, str(port))
        
    except Exception as e:
        print(f"⚠️ Error extracting packet info: {e}")
        return ("", "", "Unknown", "")

def stop_simulation():
    global SIMULATION_RUNNING
    SIMULATION_RUNNING = False
    print("⏹️ Simulation stopped")

if __name__ == "__main__":
    print("🚀 Starting live packet capture...")
    
    def display_packet(packet):
        src, dst, proto, port = extract_packet_info(packet)
        if src:  # Only print if it has a valid IP
            print(f"[{time.strftime('%H:%M:%S')}] {src} -> {dst} [{proto.lower()}:{port}]")
    
    capture_packets(display_packet)
