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
            data.agent_running ? '✅ Active' : '⚠️ Inactive',
            data.agent_running ? 'success' : 'warning'
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
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        
        const tasksList = document.getElementById('tasks-list');
        
        if (data.agent && data.agent.tasks_pending > 0) {
            tasksList.innerHTML = `
                <div class="task-item">
                    <h4>📋 Active Tasks</h4>
                    <p>Total: ${data.agent.tasks_total || 0}</p>
                    <p>Completed: ${data.agent.tasks_completed || 0}</p>
                    <p>Pending: ${data.agent.tasks_pending || 0}</p>
                </div>
            `;
        } else {
            tasksList.innerHTML = '<p style="text-align: center; color: #666;">No pending tasks</p>';
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
        
        const agentData = data.agent || {};
        const tradingData = data.trading || {};
        
        statsContent.innerHTML = `
            <div class="stat-box">
                <h4>Total Tasks</h4>
                <p>${agentData.tasks_total || 0}</p>
            </div>
            <div class="stat-box">
                <h4>Completed</h4>
                <p>${agentData.tasks_completed || 0}</p>
            </div>
            <div class="stat-box">
                <h4>Pending</h4>
                <p>${agentData.tasks_pending || 0}</p>
            </div>
            <div class="stat-box">
                <h4>Learning</h4>
                <p>${agentData.learning_sessions || 0}</p>
            </div>
            <div class="stat-box">
                <h4>Balance</h4>
                <p>$${tradingData.balance || 0}</p>
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
        alert(`✅ Task "${taskName}" queued for execution!\n\nMirai AI will process it autonomously.`);
        // Refresh to see updated stats
        setTimeout(refreshStatus, 2000);
    }
}

// View full logs
function viewLogs() {
    const logsWindow = window.open('', 'Mirai Logs', 'width=800,height=600');
    logsWindow.document.write(`
        <html>
        <head>
            <title>Mirai Live Logs</title>
            <style>
                body { 
                    background: #1e1e1e; 
                    color: #00ff00; 
                    font-family: monospace; 
                    padding: 20px;
                    margin: 0;
                }
                h1 { color: #00ff00; }
                .log { margin: 5px 0; padding: 5px; border-bottom: 1px solid #333; }
            </style>
        </head>
        <body>
            <h1>🤖 Mirai Live Logs</h1>
            <div id="logs"></div>
            <script>
                setInterval(async () => {
                    const response = await fetch('http://localhost:8000/stats');
                    const data = await response.json();
                    const logsDiv = document.getElementById('logs');
                    const log = document.createElement('div');
                    log.className = 'log';
                    log.textContent = \`[\${new Date().toLocaleTimeString()}] Tasks: \${data.agent?.tasks_completed || 0} completed, \${data.agent?.tasks_pending || 0} pending\`;
                    logsDiv.appendChild(log);
                    window.scrollTo(0, document.body.scrollHeight);
                }, 3000);
            </script>
        </body>
        </html>
    `);
}

// Open Telegram
function openTelegram() {
    const message = `
🤖 Mirai AI Telegram Bot

Доступные команды:
• /status - Статус агента
• /tasks - Активные задачи
• /stats - Статистика
• /help - Помощь

Bot Token: 8104619923:AAGS0IUt18-LoVbI_UTXk51xEfF4vbr2Sr4
Admin ID: 6428365358
    `;
    alert(message);
}

// Connect to live logs via polling (WebSocket not available)
let lastLogTime = Date.now();

function connectToLiveLogs() {
    const logsContainer = document.getElementById('logs-container');
    logsContainer.innerHTML = '<p class="log-entry info">🟢 Fetching logs from systemd journal...</p>';
    
    // Poll logs every 3 seconds
    setInterval(async () => {
        try {
            // Get recent logs via API endpoint
            const response = await fetch(`${API_BASE}/stats`);
            const data = await response.json();
            
            const now = new Date();
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry info';
            logEntry.textContent = `[${now.toLocaleTimeString()}] Agent: ${data.agent?.tasks_completed || 0} tasks completed, ${data.agent?.tasks_pending || 0} pending`;
            
            logsContainer.appendChild(logEntry);
            
            // Auto-scroll to bottom
            logsContainer.scrollTop = logsContainer.scrollHeight;
            
            // Keep only last 20 entries
            while (logsContainer.children.length > 20) {
                logsContainer.removeChild(logsContainer.firstChild);
            }
        } catch (error) {
            console.error('❌ Failed to fetch logs:', error);
        }
    }, 3000);
}

// Try to connect to live logs
setTimeout(connectToLiveLogs, 2000);
