// ============================================
// NIDS Dashboard - Real-time Updates
// ============================================

// State
let updateInterval = null;
let logMessages = [];

// ============================================
// Fetch and Update Dashboard
// ============================================

async function updateDashboard() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        // Update stats
        document.getElementById('packet-count').textContent = data.packet_count;
        document.getElementById('unique-ips').textContent = data.unique_ips;
        document.getElementById('alert-count').textContent = data.alerts.length;
        
        // Update alerts table
        updateAlertsTable(data.alerts);
        
    } catch (error) {
        console.error('Error updating dashboard:', error);
    }
}

// ============================================
// Update Alerts Table
// ============================================

function updateAlertsTable(alerts) {
    const tbody = document.getElementById('alerts-body');
    
    if (!alerts || alerts.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" style="text-align: center; color: #666;">
                    ✅ No alerts detected. System is secure!
                </td>
            </tr>
        `;
        return;
    }
    
    // Show latest alerts first (reverse order)
    const latestAlerts = alerts.slice().reverse();
    
    tbody.innerHTML = latestAlerts.map(alert => {
        const alertClass = alert.type.includes('Port') ? 'alert-warning' :
                          alert.type.includes('ICMP') ? 'alert-info' :
                          'alert-critical';
        
        // Format time
        const time = new Date(alert.timestamp);
        const timeStr = time.toLocaleTimeString();
        
        return `
            <tr>
                <td>${timeStr}</td>
                <td class="${alertClass}">${alert.type}</td>
                <td>${alert.src_ip}</td>
                <td>${alert.details}</td>
            </tr>
        `;
    }).join('');
    
    // Add log entry for new alerts
    if (latestAlerts.length > 0) {
        const newest = latestAlerts[0];
        addLogEntry(`🚨 ALERT: ${newest.type} from ${newest.src_ip}`, 'alert');
    }
}

// ============================================
// Add Log Entry
// ============================================

function addLogEntry(message, type = 'info') {
    const container = document.getElementById('log-container');
    const entry = document.createElement('div');
    const time = new Date().toLocaleTimeString();
    entry.className = `log-entry log-${type}`;
    entry.textContent = `[${time}] ${message}`;
    container.appendChild(entry);
    
    // Keep only last 50 entries
    while (container.children.length > 50) {
        container.removeChild(container.firstChild);
    }
    
    // Auto-scroll to bottom
    container.scrollTop = container.scrollHeight;
}

// ============================================
// Simulate Attacks (Demo Only!)
// ============================================

async function simulateAttack(type) {
    const endpoints = {
        portscan: '/api/simulate/portscan',
        icmpflood: '/api/simulate/icmpflood',
        highrate: '/api/simulate/highrate'
    };
    
    const endpoint = endpoints[type];
    if (!endpoint) return;
    
    const names = {
        portscan: 'Port Scan',
        icmpflood: 'ICMP Flood',
        highrate: 'High Rate'
    };
    
    addLogEntry(`🎬 Starting ${names[type]} simulation...`, 'info');
    
    try {
        const response = await fetch(endpoint, { method: 'POST' });
        const data = await response.json();
        addLogEntry(`✅ ${data.status}`, 'info');
    } catch (error) {
        addLogEntry(`❌ Error: ${error.message}`, 'warning');
        console.error('Simulation error:', error);
    }
}

// ============================================
// Clear Alerts
// ============================================

async function clearAlerts() {
    if (!confirm('Clear all alerts from the dashboard?')) return;
    
    try {
        await fetch('/api/clear_alerts', { method: 'POST' });
        addLogEntry('🗑️ All alerts cleared from dashboard', 'info');
        updateDashboard();
    } catch (error) {
        console.error('Error clearing alerts:', error);
    }
}

// ============================================
// Download CSV Log
// ============================================

async function downloadCSV() {
    try {
        const response = await fetch('/api/alerts_csv');
        const data = await response.text();
        
        if (data === 'No alerts logged yet.') {
            addLogEntry('📭 No alerts to download', 'warning');
            return;
        }
        
        // Create download link
        const blob = new Blob([data], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `nids_alerts_${new Date().toISOString().slice(0,10)}.csv`;
        a.click();
        URL.revokeObjectURL(url);
        
        addLogEntry('📥 Downloaded alerts CSV', 'info');
    } catch (error) {
        console.error('Error downloading CSV:', error);
        addLogEntry('❌ Failed to download CSV', 'warning');
    }
}

// ============================================
// Initialize Dashboard
// ============================================

function initDashboard() {
    addLogEntry('🟢 System started monitoring network traffic', 'info');
    addLogEntry('💡 Click simulation buttons to demonstrate attack detection', 'info');
    
    // Initial update
    updateDashboard();
    
    // Update every 2 seconds
    updateInterval = setInterval(updateDashboard, 2000);
}

// Start when page loads
document.addEventListener('DOMContentLoaded', initDashboard);