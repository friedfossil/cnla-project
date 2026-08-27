// Configuration
const API_URL = '/alerts';
const REFRESH_INTERVAL = 2000; // 2 seconds

// DOM Elements
const alertsList = document.getElementById('alerts-list');
const totalAlertsEl = document.getElementById('total-alerts');
const highSeverityEl = document.getElementById('high-severity');
const lastAlertEl = document.getElementById('last-alert');

// State
let alertCount = 0;
let highSeverityCount = 0;

// Fetch alerts from the backend
async function fetchAlerts() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();
        
        if (data.length === 0) {
            alertsList.innerHTML = `
                <div class="alert-placeholder">✅ No threats detected. System is secure.</div>
            `;
            return;
        }
        
        // Update stats
        alertCount = data.length;
        totalAlertsEl.textContent = alertCount;
        
        // Count high severity alerts
        highSeverityCount = data.filter(a => 
            a.severity && a.severity.toLowerCase() === 'high'
        ).length;
        highSeverityEl.textContent = highSeverityCount;
        
        // Last alert timestamp
        if (data.length > 0) {
            const last = data[data.length - 1];
            lastAlertEl.textContent = last.timestamp || 'N/A';
        }
        
        // Display alerts (newest first)
        displayAlerts(data.reverse());
        
    } catch (error) {
        console.error('Error fetching alerts:', error);
        alertsList.innerHTML = `
            <div class="alert-placeholder" style="color: #ff4444;">
                ⚠️ Error connecting to server. Make sure Flask is running.
            </div>
        `;
    }
}

// Display alerts in the UI
function displayAlerts(alerts) {
    if (alerts.length === 0) {
        alertsList.innerHTML = `
            <div class="alert-placeholder">✅ No threats detected. System is secure.</div>
        `;
        return;
    }
    
    let html = '';
    alerts.forEach(alert => {
        const severityClass = getSeverityClass(alert.severity);
        html += `
            <div class="alert-item">
                <span class="timestamp">${alert.timestamp || 'N/A'}</span>
                <span class="message">${alert.message || 'Unknown alert'}</span>
                <span class="severity ${severityClass}">${alert.severity || 'Unknown'}</span>
            </div>
        `;
    });
    
    alertsList.innerHTML = html;
}

// Helper: Get CSS class for severity
function getSeverityClass(severity) {
    if (!severity) return 'severity-low';
    const s = severity.toLowerCase();
    if (s === 'high' || s === 'critical') return 'severity-high';
    if (s === 'medium') return 'severity-medium';
    return 'severity-low';
}

// Fetch alerts immediately
fetchAlerts();

// Then fetch every X seconds
setInterval(fetchAlerts, REFRESH_INTERVAL);

// Log to console
console.log('🛡️ CNLA IDS Dashboard loaded');
console.log(`📡 Fetching alerts from ${API_URL} every ${REFRESH_INTERVAL/1000}s`);