"""
System Integration Tests for CNLA IDS
Team Member 4: Jithya Suresh
"""

import unittest
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSystemIntegration(unittest.TestCase):
    """Test the complete system integration"""
    
    def setUp(self):
        """Setup before each test"""
        self.test_data = {
            'timestamp': '2024-01-15 10:30:00',
            'src_ip': '192.168.1.100',
            'dst_ip': '192.168.1.1',
            'protocol': 'TCP',
            'port': 8080,
            'severity': 'high',
            'message': 'Port scan detected from 192.168.1.100'
        }
    
    def test_alert_format(self):
        """Test that alerts have the correct format"""
        alert = self.test_data
        
        # Check all required fields exist
        required_fields = ['timestamp', 'src_ip', 'dst_ip', 'protocol', 
                          'port', 'severity', 'message']
        
        for field in required_fields:
            self.assertIn(field, alert, f"Missing field: {field}")
    
    def test_severity_values(self):
        """Test severity levels are valid"""
        valid_severities = ['high', 'medium', 'low', 'critical']
        alert_severity = self.test_data['severity']
        
        self.assertIn(alert_severity, valid_severities, 
                     f"Invalid severity: {alert_severity}")
    
    def test_ip_format(self):
        """Test IP addresses are valid format"""
        import re
        ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        
        src_ip = self.test_data['src_ip']
        dst_ip = self.test_data['dst_ip']
        
        self.assertIsNotNone(re.match(ip_pattern, src_ip), 
                           f"Invalid source IP: {src_ip}")
        self.assertIsNotNone(re.match(ip_pattern, dst_ip), 
                           f"Invalid destination IP: {dst_ip}")
    
    def test_protocol_values(self):
        """Test protocols are valid"""
        valid_protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS']
        protocol = self.test_data['protocol']
        
        self.assertIn(protocol, valid_protocols, 
                     f"Invalid protocol: {protocol}")
    
    def test_port_range(self):
        """Test port numbers are in valid range"""
        port = self.test_data['port']
        self.assertGreaterEqual(port, 1, "Port must be >= 1")
        self.assertLessEqual(port, 65535, "Port must be <= 65535")

class TestDashboardAPI(unittest.TestCase):
    """Test the Flask API endpoints"""
    
    def test_api_endpoint_exists(self):
        """Test that /alerts endpoint is configured"""
        # This will test Flask app when running
        pass
    
    def test_json_response_format(self):
        """Test that API returns JSON format"""
        # This will be implemented when Flask app is ready
        pass

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)