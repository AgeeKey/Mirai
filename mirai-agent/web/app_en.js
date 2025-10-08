const API_BASE = 'http://localhost:8000';

function scrollToDashboard() {
    document.getElementById('dashboard').scrollIntoView({ behavior: 'smooth' });
}

async function refreshStatus() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        
        updateStatusCard('agent-status', 
            data.agent_running ? '✅ Running' : '⚠️ Stopped',
            data.agent_running ? 'success' : 'warning'
        );
        
        updateStatusCard('ai-engine-status',
            data.agent_running ? '✅ Active' : '⚠️ Inactive',
            data.agent_running ? 'success' : 'warning'
        );
        
        updateStatusCard('trader-status',
            data.components?.trader ? '✅ Trading' : '⚠️ Idle',
            data.components?.trader ? 'success' : 'warning'
        );
        
        updateStatusCard('api-status',
            data.status === 'healthy' ? '✅ Online' : '❌ Offline',
            data.status === 'healthy' ? 'success' : 'error'
        );
        
    } catch (error) {
        console.error('Error fetching status:', error);
        updateAllCardsError();
    }
    
    await refreshStats();
}

function updateStatusCard(id, text, status) {
    const card = document.getElementById(id);
    if (!card) return;
    
    const indicator = card.querySelector('.status-indicator');
    if (indicator) {
        indicator.textContent = text;
        indicator.className = 'status-indicator status-' + status;
    }
}

function updateAllCardsError() {
    const cards = ['agent-status', 'ai-engine-status', 'trader-status', 'api-status'];
    cards.forEach(id => updateStatusCard(id, '❌ Error', 'error'));
}

async function refreshStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        
        // Update tasks
        const tasksContainer = document.getElementById('tasks-container');
        const tasks = data.tasks || [];
        if (tasks.length === 0) {
            tasksContainer.innerHTML = '<p>No active tasks</p>';
        } else {
            tasksContainer.innerHTML = tasks.map(task => 
                `<div class="task-item">📌 ${task.name || task}</div>`
            ).join('');
        }
        
        // Update statistics
        const statsContainer = document.getElementById('stats-container');
        const agentData = data.agent || {};
        statsContainer.innerHTML = `
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
                <h4>Learning Progress</h4>
                <p>${agentData.learning_progress || 0}%</p>
            </div>
            <div class="stat-box">
                <h4>Balance</h4>
                <p>$${agentData.balance || 10000}</p>
            </div>
            <div class="stat-box">
                <h4>Uptime</h4>
                <p>${agentData.uptime || 'N/A'}</p>
            </div>
        `;
        
        // Update logs
        updateLogs(data.logs || []);
        
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

function updateLogs(logs) {
    const logsContainer = document.getElementById('logs-container');
    if (!logs || logs.length === 0) {
        logsContainer.innerHTML = '<p>No recent logs</p>';
        return;
    }
    
    logsContainer.innerHTML = logs.slice(-10).map(log => 
        `<div class="log-entry">${log.timestamp || ''} ${log.message || log}</div>`
    ).join('');
}

// Live log updates
setInterval(async () => {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        if (data.logs) {
            updateLogs(data.logs);
        }
    } catch (error) {
        // Silently fail for live updates
    }
}, 3000);

function executeTask() {
    const taskName = prompt('Enter task name:');
    if (taskName) {
        alert(`✅ Task "${taskName}" queued for execution!`);
        setTimeout(refreshStatus, 2000);
    }
}

function viewLogs() {
    window.open('/logs', '_blank');
}

function openTelegram() {
    alert('📱 Telegram Bot Info:\n\nSend /status to your bot to get real-time updates!\n\nCommands:\n/status - System status\n/tasks - Active tasks\n/stats - Statistics');
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    refreshStatus();
    setInterval(refreshStatus, 5000);
});
