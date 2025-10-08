// ==========================================
// MIRAI AI - Full Integration Script
// ==========================================

// API Configuration
const API_BASE = '';
const API_ENDPOINTS = {
    health: '/health',
    stats: '/stats',
    agentStats: '/agent/stats',
    tasks: '/agent/tasks',
    createTask: '/agent/tasks',
    memory: '/agent/memory',
    createMemory: '/agent/memory',
    aiAsk: '/ai/ask',
    tradingStatus: '/trading/status',
    traderDecide: '/trader/decide',
    status: '/status',
    setMode: '/mode',
    pause: '/pause'
};

// Global State
const state = {
    currentSection: 'dashboard',
    theme: localStorage.getItem('theme') || 'dark',
    agentStartTime: Date.now(),
    user: {
        name: 'Командир',
        tokensUsed: 0,
        tasksCompleted: 0,
        activeTime: '0ч 0м',
        memoryUsage: '0 МБ'
    },
    health: {},
    stats: {},
    tasks: [],
    memory: [],
    isLoading: false
};

// ==========================================
// INITIALIZATION
// ==========================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Initializing Mirai AI Interface...');
    
    // Apply saved theme
    document.body.classList.toggle('dark-theme', state.theme === 'dark');
    document.body.classList.toggle('light-theme', state.theme === 'light');
    
    initializeNavigation();
    initializeThemeToggle();
    initializeDateTime();
    initializeActionButtons();
    initializeChat();
    initializeSettings();
    
    // Load initial data
    await loadAllData();
    
    // Start auto-update
    startAutoUpdate();
    
    console.log('✅ Mirai AI Interface ready!');
});

// ==========================================
// DATA LOADING
// ==========================================

async function loadAllData() {
    try {
        state.isLoading = true;
        showLoadingIndicator();
        
        await Promise.all([
            loadHealth(),
            loadStats(),
            loadTasks()
        ]);
        
        updateAllUI();
        
    } catch (error) {
        console.error('❌ Error loading data:', error);
        showNotification('Ошибка загрузки данных', 'error');
    } finally {
        state.isLoading = false;
        hideLoadingIndicator();
    }
}

async function loadHealth() {
    try {
        const response = await fetch(API_ENDPOINTS.health);
        const data = await response.json();
        state.health = data;
        
        const statusIndicator = document.querySelector('.status-indicator');
        const statusText = document.querySelector('.status-text');
        
        if (data.agent_running) {
            statusIndicator?.classList.add('active');
            statusIndicator?.classList.remove('inactive');
            if (statusText) statusText.textContent = 'AI Активен';
        } else {
            statusIndicator?.classList.remove('active');
            statusIndicator?.classList.add('inactive');
            if (statusText) statusText.textContent = 'AI Остановлен';
        }
        
        console.log('✅ Health loaded');
    } catch (error) {
        console.error('❌ Error loading health:', error);
    }
}

async function loadStats() {
    try {
        const response = await fetch(API_ENDPOINTS.stats);
        const data = await response.json();
        state.stats = data;
        
        if (data.agent) {
            state.user.tasksCompleted = data.agent.tasks_completed || 0;
            const tokensEstimate = Math.floor(
                (data.agent.tasks_completed || 0) * 150 + 
                (data.agent.learning_sessions || 0) * 800
            );
            state.user.tokensUsed = tokensEstimate;
        }
        
        console.log('✅ Stats loaded');
    } catch (error) {
        console.error('❌ Error loading stats:', error);
    }
}

async function loadTasks() {
    try {
        const response = await fetch(API_ENDPOINTS.tasks);
        const data = await response.json();
        state.tasks = Array.isArray(data) ? data : [];
        console.log(`✅ Tasks loaded: ${state.tasks.length} tasks`);
    } catch (error) {
        console.error('❌ Error loading tasks:', error);
        state.tasks = [];
    }
}

// ==========================================
// UI UPDATES
// ==========================================

function updateAllUI() {
    updateStatistics();
    updateDashboardCards();
    updateTasksList();
    updateUptime();
}

function updateStatistics() {
    const tokensEl = document.getElementById('tokensUsed');
    const tasksEl = document.getElementById('tasksCompleted');
    const activeTimeEl = document.getElementById('activeTime');
    const memoryEl = document.getElementById('memoryUsage');
    
    if (tokensEl) {
        const tokens = state.user.tokensUsed;
        tokensEl.textContent = tokens > 1000 
            ? `${(tokens / 1000).toFixed(1)}K` 
            : tokens.toString();
    }
    
    if (tasksEl) tasksEl.textContent = state.user.tasksCompleted.toString();
    if (activeTimeEl) activeTimeEl.textContent = state.user.activeTime;
    
    if (memoryEl) {
        const memoryCount = state.stats.agent?.tasks_completed || 0;
        const memoryMB = Math.floor(memoryCount * 0.5);
        memoryEl.textContent = memoryMB > 1024 
            ? `${(memoryMB / 1024).toFixed(1)} GB` 
            : `${memoryMB} МБ`;
    }
}

function updateDashboardCards() {
    const cards = {
        'agent-status': state.health.agent_running ? 'Активен' : 'Остановлен',
        'tasks-total': state.stats.agent?.tasks_total || 0,
        'tasks-pending': state.stats.agent?.tasks_pending || 0,
        'tasks-completed': state.stats.agent?.tasks_completed || 0,
        'learning-sessions': state.stats.agent?.learning_sessions || 0,
        'ai-tokens': state.user.tokensUsed
    };
    
    Object.entries(cards).forEach(([id, value]) => {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    });
}

function updateTasksList() {
    const container = document.querySelector('#tasks-list');
    if (!container) return;
    
    if (state.tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>Нет активных задач</h3>
                <button class="btn-primary" onclick="showCreateTaskDialog()">➕ Создать задачу</button>
            </div>
        `;
        return;
    }
    
    const priorityMap = { 3: 'high', 2: 'medium', 1: 'low' };
    
    container.innerHTML = state.tasks.map(task => `
        <div class="task-card ${task.status || 'pending'}">
            <div class="task-header">
                <span class="task-priority priority-${priorityMap[task.priority] || 'medium'}">
                    Приоритет: ${task.priority || 2}
                </span>
                <span class="task-status">${task.status || 'pending'}</span>
            </div>
            <div class="task-body">
                <h3>${task.description || 'Без названия'}</h3>
                <p>ID: ${task.id.substring(0, 8)}</p>
            </div>
        </div>
    `).join('');
}

function updateUptime() {
    const diff = Date.now() - state.agentStartTime;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    
    const uptimeStr = `${hours}ч ${minutes}м`;
    state.user.activeTime = uptimeStr;
    
    const el = document.getElementById('uptime');
    if (el) el.textContent = uptimeStr;
}

// ==========================================
// NAVIGATION
// ==========================================

function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.dataset.section;
            navigateToSection(section);
            
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
}

function navigateToSection(sectionId) {
    state.currentSection = sectionId;
    
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
        loadSectionData(sectionId);
    }
}

async function loadSectionData(sectionId) {
    if (sectionId === 'tasks') {
        await loadTasks();
        updateTasksList();
    }
}

// ==========================================
// ACTION BUTTONS
// ==========================================

function initializeActionButtons() {
    document.addEventListener('click', (e) => {
        const target = e.target;
        
        if (target.closest('[data-action="new-task"]') || 
            (target.textContent && target.textContent.includes('Новая задача'))) {
            showCreateTaskDialog();
        }
        
        if (target.closest('[data-action="refresh"]') || 
            (target.textContent && target.textContent.includes('Обновить'))) {
            loadAllData();
            showNotification('Данные обновлены', 'success');
        }
        
        if (target.closest('[data-action="analytics"]') ||
            (target.textContent && target.textContent.includes('Аналитика'))) {
            navigateToSection('stats');
        }
    });
}

// ==========================================
// TASK MANAGEMENT
// ==========================================

function showCreateTaskDialog() {
    const title = prompt('📝 Введите описание задачи:');
    if (!title || title.trim() === '') return;
    
    const priority = prompt('Приоритет (1-3):', '2');
    createTask(title.trim(), parseInt(priority) || 2);
}

async function createTask(title, priority = 2) {
    try {
        const response = await fetch(API_ENDPOINTS.createTask, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, priority })
        });
        
        const data = await response.json();
        
        if (data.status === 'created') {
            showNotification('✅ Задача создана', 'success');
            await loadTasks();
            updateTasksList();
        } else {
            showNotification('❌ Ошибка создания задачи', 'error');
        }
    } catch (error) {
        console.error('Error creating task:', error);
        showNotification('❌ Ошибка подключения', 'error');
    }
}

// ==========================================
// CHAT FUNCTIONALITY
// ==========================================

function initializeChat() {
    const chatInput = document.querySelector('.chat-input');
    const chatSend = document.querySelector('.chat-send');
    
    if (chatInput && chatSend) {
        chatSend.addEventListener('click', sendChatMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendChatMessage();
            }
        });
    }
}

async function sendChatMessage() {
    const input = document.querySelector('.chat-input');
    const messagesContainer = document.getElementById('chatMessages');
    
    if (!input || !messagesContainer) return;
    
    const message = input.value.trim();
    if (!message) return;
    
    addChatMessage(message, 'user');
    input.value = '';
    
    const typingId = addChatMessage('Мирай печатает...', 'mirai', true);
    
    try {
        const response = await fetch(API_ENDPOINTS.aiAsk, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: message, temperature: 0.7, max_tokens: 500 })
        });
        
        const data = await response.json();
        
        removeChatMessage(typingId);
        addChatMessage(data.answer || 'Извините, не могу ответить.', 'mirai');
        
    } catch (error) {
        console.error('Chat error:', error);
        removeChatMessage(typingId);
        addChatMessage('❌ Ошибка подключения к AI', 'mirai');
    }
}

function addChatMessage(text, sender, isTemporary = false) {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return null;
    
    const messageId = `msg-${Date.now()}-${Math.random()}`;
    const messageEl = document.createElement('div');
    messageEl.className = `message ${sender}`;
    messageEl.id = messageId;
    
    if (isTemporary) messageEl.classList.add('typing');
    
    const now = new Date();
    const timeStr = now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
    
    messageEl.innerHTML = `
        <div class="message-content">
            <div class="message-text">${text}</div>
            <div class="message-time">${timeStr}</div>
        </div>
    `;
    
    messagesContainer.appendChild(messageEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return messageId;
}

function removeChatMessage(messageId) {
    const messageEl = document.getElementById(messageId);
    if (messageEl) messageEl.remove();
}

// ==========================================
// THEME TOGGLE
// ==========================================

function initializeThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.querySelector('.theme-icon');
    
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            state.theme = state.theme === 'dark' ? 'light' : 'dark';
            
            document.body.classList.toggle('dark-theme', state.theme === 'dark');
            document.body.classList.toggle('light-theme', state.theme === 'light');
            
            if (themeIcon) {
                themeIcon.textContent = state.theme === 'dark' ? '🌙' : '☀️';
            }
            
            localStorage.setItem('theme', state.theme);
            showNotification(`Тема: ${state.theme === 'dark' ? 'тёмная' : 'светлая'}`, 'info');
        });
    }
}

// ==========================================
// DATE & TIME
// ==========================================

function initializeDateTime() {
    updateDateTime();
    setInterval(updateDateTime, 1000);
}

function updateDateTime() {
    const datetimeEl = document.querySelector('.datetime');
    if (!datetimeEl) return;
    
    const now = new Date();
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    
    datetimeEl.textContent = now.toLocaleString('ru-RU', options);
}

// ==========================================
// SETTINGS
// ==========================================

function initializeSettings() {
    // Settings initialization
}

// ==========================================
// AUTO UPDATE
// ==========================================

function startAutoUpdate() {
    setInterval(async () => {
        if (!state.isLoading) {
            await loadHealth();
            await loadStats();
            updateStatistics();
            updateDashboardCards();
            updateUptime();
        }
    }, 5000);
    
    setInterval(async () => {
        if (!state.isLoading && state.currentSection === 'tasks') {
            await loadTasks();
            updateTasksList();
        }
    }, 10000);
}

// ==========================================
// NOTIFICATIONS
// ==========================================

function showNotification(message, type = 'info') {
    const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${icons[type]} ${message}</span>
    `;
    
    let container = document.querySelector('.notifications-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'notifications-container';
        container.style.cssText = 'position:fixed;top:20px;right:20px;z-index:10000;';
        document.body.appendChild(container);
    }
    
    container.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ==========================================
// LOADING INDICATOR
// ==========================================

function showLoadingIndicator() {
    let loader = document.querySelector('.global-loader');
    if (!loader) {
        loader = document.createElement('div');
        loader.className = 'global-loader';
        loader.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:9999;';
        loader.innerHTML = '<div style="color:white;font-size:24px;">Загрузка...</div>';
        document.body.appendChild(loader);
    }
    loader.style.display = 'flex';
}

function hideLoadingIndicator() {
    const loader = document.querySelector('.global-loader');
    if (loader) loader.style.display = 'none';
}

console.log('📝 Mirai AI Full Integration loaded successfully');
