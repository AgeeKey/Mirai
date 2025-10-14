// NASA-Level Learning Dashboard - JavaScript Client
// Real-time updates, API integration, charts

const API_BASE = window.location.origin;
let proficiencyChart = null;
let qualityChart = null;
let updateInterval = null;

// Утилиты
function formatTime(seconds) {
    if (seconds < 60) return `${seconds.toFixed(1)}s`;
    return `${(seconds / 60).toFixed(1)}m`;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('ru-RU');
}

// API Calls
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'API Error');
        }
        
        return data.data;
    } catch (error) {
        console.error('API Error:', error);
        showError(error.message);
        return null;
    }
}

// Status Updates
async function updateSystemStatus() {
    const status = await apiCall('/api/nasa/status');
    if (!status) return;
    
    // Update stats
    const knowledge = status.knowledge || {};
    const metrics = status.metrics || {};
    
    document.getElementById('total-learned').textContent = knowledge.total_entries || 0;
    document.getElementById('success-rate').textContent = 
        (metrics.success_rate || 0).toFixed(1) + '%';
    document.getElementById('avg-proficiency').textContent = 
        (knowledge.average_proficiency || 0).toFixed(1) + '%';
    
    // System status indicator
    const statusIndicator = document.getElementById('system-status');
    const statusText = document.getElementById('system-status-text');
    
    if (metrics.success_rate >= 80) {
        statusIndicator.className = 'status-indicator status-healthy';
        statusText.textContent = 'Отлично';
    } else if (metrics.success_rate >= 50) {
        statusIndicator.className = 'status-indicator status-warning';
        statusText.textContent = 'Норма';
    } else {
        statusIndicator.className = 'status-indicator status-error';
        statusText.textContent = 'Проблемы';
    }
    
    // Update last update time
    document.getElementById('last-update').textContent = 
        'Обновлено: ' + new Date().toLocaleTimeString('ru-RU');
}

// Tasks Management
async function updateActiveTasks() {
    const tasks = await apiCall('/api/nasa/tasks');
    if (!tasks) return;
    
    const container = document.getElementById('tasks-container');
    const activeTasks = tasks.filter(t => t.status === 'RUNNING' || t.status === 'PENDING');
    
    document.getElementById('active-tasks').textContent = activeTasks.length;
    
    if (activeTasks.length === 0) {
        container.innerHTML = '<p class="text-muted text-center py-3">Нет активных задач</p>';
        return;
    }
    
    container.innerHTML = activeTasks.map(task => `
        <div class="mb-3">
            <div class="d-flex justify-content-between align-items-center mb-2">
                <strong>${task.technology}</strong>
                <span class="badge bg-${getStatusColor(task.status)}">
                    ${task.status}
                </span>
            </div>
            <div class="progress progress-custom">
                <div class="progress-bar progress-bar-striped progress-bar-animated" 
                     role="progressbar" 
                     style="width: ${task.progress}%">
                    ${task.progress}%
                </div>
            </div>
            <small class="text-muted">ID: ${task.task_id.substring(0, 8)}...</small>
        </div>
    `).join('');
}

function getStatusColor(status) {
    const colors = {
        'PENDING': 'secondary',
        'RUNNING': 'primary',
        'COMPLETED': 'success',
        'FAILED': 'danger',
        'CANCELLED': 'warning'
    };
    return colors[status] || 'secondary';
}

// Knowledge Browser
async function updateKnowledgeList() {
    const knowledge = await apiCall('/api/nasa/knowledge');
    if (!knowledge) return;
    
    const container = document.getElementById('knowledge-list');
    
    if (knowledge.length === 0) {
        container.innerHTML = '<p class="text-muted text-center py-3">База знаний пуста</p>';
        return;
    }
    
    container.innerHTML = knowledge.map(tech => `
        <div class="tech-item">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <h6 class="mb-1">${tech.technology}</h6>
                    <small class="text-muted">
                        Версия: ${tech.version} | 
                        Изучено: ${formatDate(tech.learned_at)}
                    </small>
                </div>
                <div class="text-end">
                    <span class="badge badge-custom bg-${getGradeColor(tech.quality_grade)}">
                        ${tech.quality_grade}
                    </span>
                    <div class="mt-1">
                        <small class="text-muted">${tech.proficiency.toFixed(1)}%</small>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function getGradeColor(grade) {
    const colors = {
        'A': 'success',
        'B': 'primary',
        'C': 'warning',
        'D': 'danger',
        'F': 'dark'
    };
    return colors[grade] || 'secondary';
}

// Charts
async function updateCharts() {
    const knowledge = await apiCall('/api/nasa/knowledge');
    if (!knowledge || knowledge.length === 0) return;
    
    // Proficiency Chart
    updateProficiencyChart(knowledge);
    
    // Quality Distribution Chart
    updateQualityChart(knowledge);
}

function updateProficiencyChart(knowledge) {
    const ctx = document.getElementById('proficiency-chart');
    
    if (proficiencyChart) {
        proficiencyChart.destroy();
    }
    
    const sorted = knowledge.sort((a, b) => b.proficiency - a.proficiency).slice(0, 10);
    
    proficiencyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sorted.map(t => t.technology),
            datasets: [{
                label: 'Профессиональность (%)',
                data: sorted.map(t => t.proficiency),
                backgroundColor: 'rgba(99, 102, 241, 0.8)',
                borderColor: 'rgba(99, 102, 241, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

function updateQualityChart(knowledge) {
    const ctx = document.getElementById('quality-chart');
    
    if (qualityChart) {
        qualityChart.destroy();
    }
    
    const gradeCounts = knowledge.reduce((acc, tech) => {
        acc[tech.quality_grade] = (acc[tech.quality_grade] || 0) + 1;
        return acc;
    }, {});
    
    qualityChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(gradeCounts),
            datasets: [{
                data: Object.values(gradeCounts),
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',  // A - green
                    'rgba(99, 102, 241, 0.8)',   // B - blue
                    'rgba(245, 158, 11, 0.8)',   // C - yellow
                    'rgba(239, 68, 68, 0.8)',    // D - red
                    'rgba(107, 114, 128, 0.8)'   // F - gray
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Form Handlers
document.getElementById('learn-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const technology = document.getElementById('tech-input').value.trim();
    const depth = document.getElementById('depth-select').value;
    const priority = document.getElementById('priority-select').value;
    
    if (!technology) {
        showError('Введите название технологии');
        return;
    }
    
    const result = await apiCall('/api/nasa/learn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ technology, depth, priority })
    });
    
    if (result) {
        showSuccess(`Задача создана: ${result.task_id.substring(0, 8)}...`);
        document.getElementById('learn-form').reset();
        setTimeout(updateActiveTasks, 500);
    }
});

// Search
document.getElementById('search-input').addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    const items = document.querySelectorAll('.tech-item');
    
    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(query) ? 'block' : 'none';
    });
});

// Logs (mock for now)
function updateLogs() {
    const logViewer = document.getElementById('log-viewer');
    const timestamp = new Date().toLocaleTimeString();
    
    // In real implementation, fetch from /api/nasa/logs
    const newLog = `[${timestamp}] System status: OK\n`;
    
    if (logViewer.children.length > 50) {
        logViewer.removeChild(logViewer.firstChild);
    }
    
    const logLine = document.createElement('div');
    logLine.textContent = newLog;
    logViewer.appendChild(logLine);
    logViewer.scrollTop = logViewer.scrollHeight;
}

// Refresh Functions
async function refreshAll() {
    await Promise.all([
        updateSystemStatus(),
        updateActiveTasks(),
        updateKnowledgeList(),
        updateCharts()
    ]);
    updateLogs();
}

async function refreshTasks() {
    await updateActiveTasks();
}

// Notifications
function showSuccess(message) {
    // Simple alert for now, can be replaced with toast notifications
    console.log('Success:', message);
}

function showError(message) {
    console.error('Error:', message);
    alert('Ошибка: ' + message);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('NASA-Level Dashboard initialized');
    
    // Initial load
    refreshAll();
    
    // Auto-refresh every 5 seconds
    updateInterval = setInterval(refreshAll, 5000);
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        if (updateInterval) {
            clearInterval(updateInterval);
        }
    });
});
