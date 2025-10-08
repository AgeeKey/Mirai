// API Base URL
const API_BASE = 'http://localhost:8000';

// Auto-refresh interval (5 seconds)
let autoRefreshInterval;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Mirai Dashboard loaded');
    refreshStatus();
    startAutoRefresh();
});

// Start auto-refresh
function startAutoRefresh() {
    autoRefreshInterval = setInterval(() => {
        refreshStatus();
    }, 5000); // Refresh every 5 seconds
}

// Refresh all status information
async function refreshStatus() {
    await Promise.all([
        fetchHealthStatus(),
        fetchTasks(),
        fetchStats()
    ]);
}

// Fetch health status
async function fetchHealthStatus() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        
        updateStatusCard('agent-status', 
            data.agent_running ? '✅ Running' : '❌ Stopped',
            data.agent_running ? 'success' : 'error'
        );
        
        updateStatusCard('ai-engine',
            data.ai_engine ? '✅ Active' : '⚠️ Inactive',
            data.ai_engine ? 'success' : 'warning'
        );
        
        updateStatusCard('trader-status',
            data.trader_running ? '✅ Trading' : '❌ Stopped',
            data.trader_running ? 'success' : 'error'
        );
        
        updateStatusCard('api-status',
            '✅ Online',
            'success'
        );
    } catch (error) {
        console.error('❌ Failed to fetch health status:', error);
        updateStatusCard('api-status', '❌ Offline', 'error');
    }
}

// Fetch tasks
async function fetchTasks() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        const tasksList = document.getElementById('tasks-list');
        
        if (data.active_tasks && data.active_tasks.length > 0) {
            tasksList.innerHTML = data.active_tasks.map(task => `
                <div class="task-item">
                    <h4>📋 ${task.name || 'Unnamed Task'}</h4>
                    <p>Status: ${task.status || 'In Progress'}</p>
                    <p>Created: ${task.created || 'Unknown'}</p>
                </div>
            `).join('');
        } else {
            tasksList.innerHTML = '<p style="text-align: center; color: #666;">No active tasks</p>';
        }
    } catch (error) {
        console.error('❌ Failed to fetch tasks:', error);
        document.getElementById('tasks-list').innerHTML = 
            '<p style="color: red;">Failed to load tasks</p>';
    }
}

// Fetch statistics
async function fetchStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        
        const statsContent = document.getElementById('stats-content');
        statsContent.innerHTML = `
            <div class="stat-box">
                <h4>Total Tasks</h4>
                <p>${data.total_tasks || 0}</p>
            </div>
            <div class="stat-box">
                <h4>Completed</h4>
                <p>${data.completed_tasks || 0}</p>
            </div>
            <div class="stat-box">
                <h4>AI Requests</h4>
                <p>${data.ai_requests || 0}</p>
            </div>
            <div class="stat-box">
                <h4>Uptime</h4>
                <p>${data.uptime || 'N/A'}</p>
            </div>
            <div class="stat-box">
                <h4>Memory</h4>
                <p>${data.memory_usage || 'N/A'}</p>
            </div>
            <div class="stat-box">
                <h4>Last Update</h4>
                <p>${new Date().toLocaleTimeString()}</p>
            </div>
        `;
    } catch (error) {
        console.error('❌ Failed to fetch stats:', error);
        document.getElementById('stats-content').innerHTML = 
            '<p style="color: red;">Failed to load statistics</p>';
    }
}

// Update status card
function updateStatusCard(cardId, value, status) {
    const card = document.getElementById(cardId);
    const valueElement = card.querySelector('.status-value');
    valueElement.textContent = value;
    
    // Remove old status classes
    card.classList.remove('status-success', 'status-error', 'status-warning');
    
    // Add new status class
    if (status) {
        card.classList.add(`status-${status}`);
    }
}

// Execute new task (placeholder)
function executeTask() {
    const taskName = prompt('Enter task name:');
    if (taskName) {
        alert(`Task "${taskName}" will be executed by AI agent!`);
        // TODO: Implement actual task execution via API
    }
}

// View full logs
function viewLogs() {
    window.open('/logs', '_blank');
}

// Open Telegram
function openTelegram() {
    alert('Send /status to your Telegram bot to check agent status!');
}

// Connect to WebSocket for live logs (if available)
function connectToLiveLogs() {
    const logsContainer = document.getElementById('logs-container');
    
    try {
        const ws = new WebSocket('ws://localhost:8000/ws/trading');
        
        ws.onopen = () => {
            console.log('✅ WebSocket connected');
            logsContainer.innerHTML = '<p class="log-entry info">🟢 Connected to live logs...</p>';
        };
        
        ws.onmessage = (event) => {
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry info';
            logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${event.data}`;
            logsContainer.appendChild(logEntry);
            
            // Auto-scroll to bottom
            logsContainer.scrollTop = logsContainer.scrollHeight;
            
            // Keep only last 50 entries
            while (logsContainer.children.length > 50) {
                logsContainer.removeChild(logsContainer.firstChild);
            }
        };
        
        ws.onerror = (error) => {
            console.error('❌ WebSocket error:', error);
            logsContainer.innerHTML = '<p class="log-entry error">❌ Failed to connect to live logs</p>';
        };
        
        ws.onclose = () => {
            console.log('🔴 WebSocket disconnected');
            logsContainer.innerHTML += '<p class="log-entry warning">🟡 Live logs disconnected</p>';
            
            // Try to reconnect after 5 seconds
            setTimeout(connectToLiveLogs, 5000);
        };
    } catch (error) {
        console.error('❌ Failed to create WebSocket:', error);
        logsContainer.innerHTML = '<p class="log-entry error">❌ Live logs not available</p>';
    }
}

// Try to connect to live logs
setTimeout(connectToLiveLogs, 2000);
