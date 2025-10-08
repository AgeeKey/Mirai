const API_BASE = 'http://localhost:8000';

// Theme management
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.querySelector('.theme-icon');
    
    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        themeIcon.textContent = '☀️';
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        themeIcon.textContent = '🌙';
        localStorage.setItem('theme', 'dark');
    }
}

// Load saved theme on page load
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const body = document.body;
    const themeIcon = document.querySelector('.theme-icon');
    
    if (savedTheme === 'light') {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        themeIcon.textContent = '☀️';
    } else {
        body.classList.add('dark-theme');
        themeIcon.textContent = '🌙';
    }
}

function scrollToDashboard() {
    document.getElementById('dashboard').scrollIntoView({ behavior: 'smooth' });
}

async function refreshStatus() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        
        updateStatusCard('agent-status', 
            data.agent_running ? '✅ Работает' : '⚠️ Остановлен',
            data.agent_running ? 'success' : 'warning'
        );
        
        updateStatusCard('ai-engine-status',
            data.agent_running ? '✅ Активен' : '⚠️ Неактивен',
            data.agent_running ? 'success' : 'warning'
        );
        
        updateStatusCard('trader-status',
            data.components?.trader ? '✅ Торгует' : '⚠️ Ожидание',
            data.components?.trader ? 'success' : 'warning'
        );
        
        updateStatusCard('api-status',
            data.status === 'healthy' ? '✅ Онлайн' : '❌ Оффлайн',
            data.status === 'healthy' ? 'success' : 'error'
        );
        
    } catch (error) {
        console.error('Ошибка получения статуса:', error);
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
    cards.forEach(id => updateStatusCard(id, '❌ Ошибка', 'error'));
}

async function refreshStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        
        // Update tasks
        const tasksContainer = document.getElementById('tasks-container');
        const tasks = data.tasks || [];
        if (tasks.length === 0) {
            tasksContainer.innerHTML = '<p>Нет активных задач</p>';
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
                <h4>Всего Задач</h4>
                <p>${agentData.tasks_total || 0}</p>
            </div>
            <div class="stat-box">
                <h4>Завершено</h4>
                <p>${agentData.tasks_completed || 0}</p>
            </div>
            <div class="stat-box">
                <h4>В Ожидании</h4>
                <p>${agentData.tasks_pending || 0}</p>
            </div>
            <div class="stat-box">
                <h4>Прогресс Обучения</h4>
                <p>${agentData.learning_progress || 0}%</p>
            </div>
            <div class="stat-box">
                <h4>Баланс</h4>
                <p>$${agentData.balance || 10000}</p>
            </div>
            <div class="stat-box">
                <h4>Время Работы</h4>
                <p>${agentData.uptime || 'N/A'}</p>
            </div>
        `;
        
        // Update logs
        updateLogs(data.logs || []);
        
    } catch (error) {
        console.error('Ошибка получения статистики:', error);
    }
}

function updateLogs(logs) {
    const logsContainer = document.getElementById('logs-container');
    if (!logs || logs.length === 0) {
        logsContainer.innerHTML = '<p>Нет последних логов</p>';
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
    const taskName = prompt('Введите название задачи:');
    if (taskName) {
        alert(`✅ Задача "${taskName}" поставлена в очередь!`);
        setTimeout(refreshStatus, 2000);
    }
}

function viewLogs() {
    window.open('/logs', '_blank');
}

function openTelegram() {
    alert('📱 Информация о Telegram боте:\n\nОтправьте /status боту для получения обновлений в реальном времени!\n\nКоманды:\n/status - Статус системы\n/tasks - Активные задачи\n/stats - Статистика');
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    refreshStatus();
    setInterval(refreshStatus, 5000);
});
