from collections import defaultdict
from scapy.all import sniff, IP, TCP

class TrafficAnalyzer:
    def __init__(self):
        self.connections = defaultdict(list)
        self.flow_stats = defaultdict(lambda: {
            'packet_count':0,
            'byte_count':0,
            'start_time':None,
            'last_time':None
        })
        
    def analyze_packet(self,packet):
        if IP in packet and TCP in packet:
            ip_src = packet[IP].src
            ip_dist = packet[IP].dst
            port_src = packet[TCP].sport
            port_dst = packet[TCP].dport
            
            flow_key = (ip_src,ip_dist,port_src,port_dst)
            
            stats = self.flow_stats[flow_key]
            stats['packet_count'] += 1
            stats['byte_count'] += len(packet)
            current_time = packet.time
            
            if not stats['start_time']:
                stats['start_time'] = current_time
            stats['last_time'] = current_time
            
            return self.extract_features(packet,stats)
    
    def extract_features(self, packet, stats):
        duration = stats['last_time'] - stats['start_time']
        duration = duration if duration > 0 else 1e-6  # avoid zero division
        
        return {
            'packet_size': len(packet),
            'flow_duration': duration,
            'packet_rate': stats['packet_count'] / duration,
            'byte_rate': stats['byte_count'] / duration,
            'tcp_flags': packet[TCP].flags,
            'window_size': packet[TCP].window
        }
