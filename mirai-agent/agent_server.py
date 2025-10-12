#!/usr/bin/env python3
"""
MIRAI Agent Server
Веб-интерфейс для управления автономным агентом
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.dirname(__file__))
from core.autonomous_agent import AutonomousAgent

load_dotenv()

app = FastAPI(title="MIRAI Autonomous Agent", version="2.0.0")

# CORS для доступа из браузера
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Глобальный агент
agent = AutonomousAgent()
current_task = None


class TaskRequest(BaseModel):
    prompt: str
    max_iterations: int = 5


@app.get("/", response_class=HTMLResponse)
async def home():
    """Главная страница с интерфейсом агента"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>MIRAI - Autonomous Agent</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
            min-height: 100vh;
            padding: 20px;
            color: #fff;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3.5em;
            margin-bottom: 10px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
            background: linear-gradient(45deg, #fff, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .header .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .status-badge {
            display: inline-block;
            padding: 8px 20px;
            background: #10b981;
            border-radius: 20px;
            font-weight: bold;
            margin-top: 15px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .card h2 {
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #a78bfa;
        }
        
        .capabilities {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        
        .capability {
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            border-left: 4px solid #10b981;
        }
        
        .capability-icon {
            font-size: 1.5em;
            margin-bottom: 5px;
        }
        
        .task-input {
            width: 100%;
            min-height: 150px;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            font-size: 16px;
            resize: vertical;
        }
        
        .task-input::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }
        
        .button {
            padding: 15px 40px;
            font-size: 18px;
            background: linear-gradient(45deg, #10b981, #059669);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
            margin-top: 15px;
        }
        
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(16, 185, 129, 0.4);
        }
        
        .button:disabled {
            background: #666;
            cursor: not-allowed;
            transform: none;
        }
        
        .output {
            background: #1a1a2e;
            padding: 20px;
            border-radius: 10px;
            min-height: 300px;
            max-height: 500px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .output.working {
            border: 2px solid #10b981;
            animation: borderPulse 1s infinite;
        }
        
        @keyframes borderPulse {
            0%, 100% { border-color: #10b981; }
            50% { border-color: #059669; }
        }
        
        .examples {
            display: grid;
            gap: 10px;
        }
        
        .example {
            padding: 10px 15px;
            background: rgba(167, 139, 250, 0.2);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            border: 1px solid rgba(167, 139, 250, 0.3);
        }
        
        .example:hover {
            background: rgba(167, 139, 250, 0.3);
            transform: translateX(5px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 MIRAI</h1>
            <div class="subtitle">Autonomous AI Agent</div>
            <div class="status-badge">🟢 ONLINE & READY</div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>⚡ Возможности агента</h2>
                <div class="capabilities">
                    <div class="capability">
                        <div class="capability-icon">🐍</div>
                        <strong>Выполнение кода</strong>
                        <div>Python, команды shell</div>
                    </div>
                    <div class="capability">
                        <div class="capability-icon">🌐</div>
                        <strong>Поиск в сети</strong>
                        <div>Актуальная информация</div>
                    </div>
                    <div class="capability">
                        <div class="capability-icon">📁</div>
                        <strong>Работа с файлами</strong>
                        <div>Чтение, создание, изменение</div>
                    </div>
                    <div class="capability">
                        <div class="capability-icon">🔧</div>
                        <strong>Самомодификация</strong>
                        <div>Улучшение себя</div>
                    </div>
                    <div class="capability">
                        <div class="capability-icon">🎯</div>
                        <strong>Автономность</strong>
                        <div>Сам создает задачи</div>
                    </div>
                    <div class="capability">
                        <div class="capability-icon">🧠</div>
                        <strong>GPT-4 мозг</strong>
                        <div>Умные решения</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>📋 Примеры задач</h2>
                <div class="examples">
                    <div class="example" onclick="setExample('Создай веб-скрапер для получения курса биткоина и сохрани результат в файл')">
                        💰 Скрапер курса Bitcoin
                    </div>
                    <div class="example" onclick="setExample('Найди последние новости по AI и создай краткий отчет в markdown')">
                        📰 Новости по AI
                    </div>
                    <div class="example" onclick="setExample('Напиши скрипт для анализа логов и автоматического поиска ошибок')">
                        🔍 Анализатор логов
                    </div>
                    <div class="example" onclick="setExample('Создай простую игру на Python с GUI')">
                        🎮 Простая игра
                    </div>
                    <div class="example" onclick="setExample('Проанализируй структуру проекта и предложи улучшения')">
                        🏗️ Улучшение проекта
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>💬 Дай задачу агенту</h2>
            <textarea id="taskInput" class="task-input" placeholder="Опиши что должен сделать агент...

Например:
- Создай REST API для управления задачами
- Найди информацию о последних трендах в ML
- Напиши скрипт для автоматизации резервного копирования
- Улучши существующий код в проекте"></textarea>
            <button class="button" id="startBtn" onclick="startTask()">🚀 Запустить агента</button>
        </div>
        
        <div class="card">
            <h2>📊 Вывод агента</h2>
            <div id="output" class="output">Ожидание задачи...</div>
        </div>
    </div>
    
    <script>
        function setExample(text) {
            document.getElementById('taskInput').value = text;
        }
        
        async function startTask() {
            const taskInput = document.getElementById('taskInput');
            const output = document.getElementById('output');
            const startBtn = document.getElementById('startBtn');
            
            const prompt = taskInput.value.trim();
            
            if (!prompt) {
                alert('Введите задачу для агента!');
                return;
            }
            
            // Блокируем кнопку
            startBtn.disabled = true;
            startBtn.textContent = '⏳ Агент работает...';
            
            // Визуализация работы
            output.classList.add('working');
            output.textContent = '🤖 Агент начал выполнение задачи...\\n\\nЭто может занять некоторое время.\\n';
            
            try {
                const response = await fetch('/api/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        prompt: prompt,
                        max_iterations: 10
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    output.textContent = '✅ ЗАДАЧА ВЫПОЛНЕНА\\n\\n' + data.result;
                } else {
                    output.textContent = '❌ ОШИБКА\\n\\n' + data.error;
                }
                
            } catch (error) {
                output.textContent = '❌ Ошибка соединения: ' + error.message;
            } finally {
                output.classList.remove('working');
                startBtn.disabled = false;
                startBtn.textContent = '🚀 Запустить агента';
            }
        }
        
        // Enter для отправки
        document.getElementById('taskInput').addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                startTask();
            }
        });
    </script>
</body>
</html>
    """


@app.post("/api/execute")
async def execute_task(task: TaskRequest):
    """Выполнить задачу агентом"""
    try:
        print(f"\n🎯 Получена задача: {task.prompt[:100]}...")

        # Выполняем задачу
        result = agent.think(task.prompt, max_iterations=task.max_iterations)

        return JSONResponse({"success": True, "result": result, "tasks": agent.tasks})

    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.get("/api/status")
async def get_status():
    """Получить статус агента"""
    return {
        "status": "online",
        "model": agent.model,
        "tasks_completed": len(agent.tasks),
        "memory_size": len(agent.memory),
    }


@app.get("/api/tasks")
async def get_tasks():
    """Получить список задач"""
    return {"tasks": agent.tasks}


@app.get("/health")
async def health_check():
    """Проверка здоровья сервера"""
    return {"status": "healthy", "agent": "online"}


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 MIRAI Autonomous Agent Server")
    print("=" * 60)
    print(f"🌐 Интерфейс: http://localhost:8000")
    print(f"📚 API Docs: http://localhost:8000/docs")
    print(f"🤖 Модель: {agent.model}")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
