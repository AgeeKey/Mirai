// ==========================================
// MIRAI AI - Full Integration Script (FIXED)
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
// ACTION BUTTONS - FIXED VERSION
// ==========================================

function initializeActionButtons() {
    // Получаем все кнопки в сайдбаре
    const actionButtons = document.querySelectorAll('.sidebar-actions button');
    
    actionButtons.forEach((btn, index) => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const text = btn.textContent.trim();
            
            console.log('Button clicked:', text);
            
            if (text.includes('Новая задача')) {
                showCreateTaskDialog();
            } else if (text.includes('Обновить')) {
                refreshData();
            } else if (text.includes('Аналитика')) {
                navigateToSection('stats');
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                document.querySelector('.nav-link[data-section="stats"]')?.classList.add('active');
            } else if (text.includes('Чат')) {
                navigateToSection('chat');
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                document.querySelector('.nav-link[data-section="chat"]')?.classList.add('active');
            } else if (text.includes('Поиск')) {
                showWebSearchDialog();
            }
        });
    });
    
    console.log(`✅ ${actionButtons.length} action buttons initialized`);
}

async function refreshData() {
    await loadAllData();
    showNotification('Данные обновлены', 'success');
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

async function createTask(description, priority = 2) {
    try {
        console.log('Creating task:', description, priority);
        
        const response = await fetch(API_ENDPOINTS.createTask, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                description: description,
                priority: priority 
            })
        });
        
        const data = await response.json();
        console.log('Task creation response:', data);
        
        if (data.status === 'created' || data.id) {
            showNotification('✅ Задача создана', 'success');
            await loadTasks();
            updateTasksList();
        } else {
            showNotification('❌ Ошибка создания задачи', 'error');
        }
    } catch (error) {
        console.error('Error creating task:', error);
        showNotification('❌ Ошибка подключения: ' + error.message, 'error');
    }
}

// ==========================================
// WEB SEARCH FUNCTIONALITY - NEW
// ==========================================

async function showWebSearchDialog() {
    const query = prompt('🔍 Что найти в интернете?');
    if (!query || query.trim() === '') return;
    
    showNotification('🌐 Выполняю поиск в интернете...', 'info');
    
    try {
        // Создаём задачу для агента на поиск в интернете
        const response = await fetch(API_ENDPOINTS.createTask, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                description: `Поиск в интернете: ${query}`,
                priority: 2,
                metadata: {
                    type: 'web_search',
                    query: query
                }
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'created' || data.id) {
            showNotification(`✅ Задача на поиск "${query}" создана`, 'success');
            
            // Переходим в раздел задач
            navigateToSection('tasks');
            await loadTasks();
            updateTasksList();
            
            // Обновляем навигацию
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            document.querySelector('.nav-link[data-section="tasks"]')?.classList.add('active');
        } else {
            showNotification('❌ Ошибка создания задачи поиска', 'error');
        }
    } catch (error) {
        console.error('Web search error:', error);
        showNotification('❌ Ошибка поиска: ' + error.message, 'error');
    }
}

// ==========================================
// CHAT FUNCTIONALITY - FIXED
// ==========================================

function initializeChat() {
    const chatInput = document.querySelector('.chat-input');
    const chatSend = document.querySelector('.chat-send');
    
    console.log('Chat elements:', { input: !!chatInput, send: !!chatSend });
    
    if (chatInput && chatSend) {
        // Обработчик кнопки отправки
        chatSend.addEventListener('click', () => {
            console.log('Chat send button clicked');
            sendChatMessage();
        });
        
        // Обработчик Enter
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                console.log('Enter pressed in chat');
                sendChatMessage();
            }
        });
        
        console.log('✅ Chat initialized successfully');
    } else {
        console.error('❌ Chat elements not found!');
    }
}

async function sendChatMessage() {
    const input = document.querySelector('.chat-input');
    const messagesContainer = document.getElementById('chatMessages');
    
    if (!input || !messagesContainer) {
        console.error('Chat elements not found!');
        return;
    }
    
    const message = input.value.trim();
    if (!message) return;
    
    console.log('Sending message:', message);
    
    // Очищаем старые сообщения-примеры
    if (messagesContainer.children.length <= 3) {
        messagesContainer.innerHTML = '';
    }
    
    addChatMessage(message, 'user');
    input.value = '';
    
    const typingId = addChatMessage('Мирай печатает...', 'mirai', true);
    
    try {
        const response = await fetch(API_ENDPOINTS.aiAsk, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                prompt: message, 
                temperature: 0.7, 
                max_tokens: 500 
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        console.log('AI response:', data);
        
        removeChatMessage(typingId);
        addChatMessage(data.answer || 'Извините, не могу ответить.', 'mirai');
        
    } catch (error) {
        console.error('Chat error:', error);
        removeChatMessage(typingId);
        addChatMessage('❌ Ошибка подключения к AI: ' + error.message, 'mirai');
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
    
    const avatarUrl = sender === 'mirai' 
        ? "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40'%3E%3Ccircle cx='20' cy='20' r='20' fill='%23a361ff'/%3E%3Ctext x='20' y='26' font-family='Arial' font-size='18' fill='white' text-anchor='middle'%3E未%3C/text%3E%3C/svg%3E"
        : "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40'%3E%3Ccircle cx='20' cy='20' r='20' fill='%236e56cf'/%3E%3Ctext x='20' y='26' font-family='Arial' font-size='18' fill='white' text-anchor='middle'%3EU%3C/text%3E%3C/svg%3E";
    
    if (sender === 'mirai') {
        messageEl.innerHTML = `
            <img src="${avatarUrl}" alt="Mirai" class="message-avatar">
            <div class="message-content">
                <div class="message-text">${text}</div>
                <div class="message-time">${timeStr}</div>
            </div>
        `;
    } else {
        messageEl.innerHTML = `
            <div class="message-content">
                <div class="message-text">${text}</div>
                <div class="message-time">${timeStr}</div>
            </div>
            <img src="${avatarUrl}" alt="User" class="message-avatar">
        `;
    }
    
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
    notification.style.cssText = 'padding:15px 20px;margin:10px;background:#1a1a2e;color:white;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.3);display:flex;align-items:center;gap:10px;animation:slideIn 0.3s ease;';
    notification.innerHTML = `<span style="font-size:20px;">${icons[type]}</span><span>${message}</span>`;
    
    let container = document.querySelector('.notifications-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'notifications-container';
        container.style.cssText = 'position:fixed;top:80px;right:20px;z-index:10000;max-width:400px;';
        document.body.appendChild(container);
    }
    
    container.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
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
        loader.innerHTML = '<div style="color:white;font-size:24px;padding:20px;background:#1a1a2e;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,0.5);">⏳ Загрузка...</div>';
        document.body.appendChild(loader);
    }
    loader.style.display = 'flex';
}

function hideLoadingIndicator() {
    const loader = document.querySelector('.global-loader');
    if (loader) loader.style.display = 'none';
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);

console.log('📝 Mirai AI Full Integration (FIXED) loaded successfully');
