#!/usr/bin/env python3
"""
Mirai - Minimal Experiment Server
Только OpenAI + Локальный веб-интерфейс
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import os
from openai import OpenAI
from datetime import datetime

app = FastAPI(title="Mirai Minimal Experiment", version="1.0.0")

# Загружаем OpenAI ключ из переменной окружения
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables!")

client = OpenAI(api_key=api_key)

# История чата (в памяти)
chat_history = []


@app.get("/", response_class=HTMLResponse)
async def home():
    """Главная страница"""
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Mirai - Minimal Mode</title>
            <meta charset="UTF-8">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                .header {
                    text-align: center;
                    color: white;
                    margin-bottom: 30px;
                }
                .header h1 {
                    font-size: 3em;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                .status-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }
                .card {
                    background: white;
                    border-radius: 15px;
                    padding: 25px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    transition: transform 0.3s;
                }
                .card:hover {
                    transform: translateY(-5px);
                }
                .card h2 {
                    color: #667eea;
                    margin-bottom: 15px;
                    font-size: 1.5em;
                }
                .status-item {
                    padding: 10px 0;
                    border-bottom: 1px solid #eee;
                }
                .status-item:last-child {
                    border-bottom: none;
                }
                .success { color: #28a745; font-weight: bold; }
                .disabled { color: #dc3545; font-weight: bold; }
                .info { color: #17a2b8; }
                .chat-container {
                    background: white;
                    border-radius: 15px;
                    padding: 25px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    margin-bottom: 20px;
                }
                .chat-input {
                    width: 100%;
                    padding: 15px;
                    border: 2px solid #667eea;
                    border-radius: 10px;
                    font-size: 16px;
                    margin-bottom: 10px;
                }
                .chat-btn {
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 10px;
                    font-size: 16px;
                    cursor: pointer;
                    transition: background 0.3s;
                }
                .chat-btn:hover {
                    background: #5568d3;
                }
                .chat-output {
                    margin-top: 20px;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 10px;
                    min-height: 100px;
                    white-space: pre-wrap;
                }
                .links {
                    display: flex;
                    gap: 15px;
                    flex-wrap: wrap;
                }
                .link-btn {
                    background: #667eea;
                    color: white;
                    padding: 12px 24px;
                    border-radius: 8px;
                    text-decoration: none;
                    transition: background 0.3s;
                    display: inline-block;
                }
                .link-btn:hover {
                    background: #5568d3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 MIRAI</h1>
                    <p>Minimal Experiment Mode - OpenAI Only</p>
                </div>

                <div class="status-grid">
                    <div class="card">
                        <h2>⚡ System Status</h2>
                        <div class="status-item">
                            <span class="success">✅ Server: Running</span>
                        </div>
                        <div class="status-item">
                            <span class="success">✅ OpenAI: Connected</span>
                        </div>
                        <div class="status-item">
                            <span class="info">🌐 Host: localhost:8000</span>
                        </div>
                    </div>

                    <div class="card">
                        <h2>🔧 Configuration</h2>
                        <div class="status-item">
                            <span class="info">Mode: Development</span>
                        </div>
                        <div class="status-item">
                            <span class="info">Debug: Enabled</span>
                        </div>
                        <div class="status-item">
                            <span class="info">AI Model: GPT-3.5-turbo</span>
                        </div>
                    </div>

                    <div class="card">
                        <h2>❌ Disabled Services</h2>
                        <div class="status-item">
                            <span class="disabled">❌ Telegram Bot</span>
                        </div>
                        <div class="status-item">
                            <span class="disabled">❌ Binance Trading</span>
                        </div>
                        <div class="status-item">
                            <span class="disabled">❌ Domain Config</span>
                        </div>
                    </div>
                </div>

                <div class="chat-container">
                    <h2 style="color: #667eea; margin-bottom: 15px;">💬 Chat with AI</h2>
                    <input type="text" id="chatInput" class="chat-input" placeholder="Type your message here..." />
                    <button onclick="sendMessage()" class="chat-btn">Send Message</button>
                    <div id="chatOutput" class="chat-output">Ready to chat...</div>
                </div>

                <div class="card">
                    <h2>🔗 Quick Links</h2>
                    <div class="links">
                        <a href="/api/test" class="link-btn">Test OpenAI</a>
                        <a href="/api/health" class="link-btn">Health Check</a>
                        <a href="/docs" class="link-btn">API Docs</a>
                        <a href="/api/chat?message=Hello" class="link-btn">Quick Test</a>
                    </div>
                </div>
            </div>

            <script>
                async function sendMessage() {
                    const input = document.getElementById('chatInput');
                    const output = document.getElementById('chatOutput');
                    const message = input.value.trim();
                    
                    if (!message) return;
                    
                    output.textContent = '🤔 Thinking...';
                    
                    try {
                        const response = await fetch(`/api/chat?message=${encodeURIComponent(message)}`);
                        const data = await response.json();
                        
                        if (data.status === 'success') {
                            output.textContent = `You: ${data.question}\n\nAI: ${data.answer}`;
                        } else {
                            output.textContent = `Error: ${data.error}`;
                        }
                    } catch (error) {
                        output.textContent = `Error: ${error.message}`;
                    }
                }
                
                document.getElementById('chatInput').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
            </script>
        </body>
    </html>
    """


@app.get("/api/test")
async def test_openai():
    """Тестирование OpenAI подключения"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "Say 'OpenAI connected successfully!' in Russian",
                }
            ],
            max_tokens=50,
        )
        return {
            "status": "success",
            "message": response.choices[0].message.content,
            "model": response.model,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chat")
async def chat(message: str = "Hello"):
    """Простой чат с AI"""
    try:
        # Добавляем в историю
        chat_history.append(
            {"role": "user", "content": message, "time": datetime.now().isoformat()}
        )

        # Ограничиваем историю последними 10 сообщениями
        recent_history = chat_history[-10:]
        messages = [
            {"role": msg["role"], "content": msg["content"]} for msg in recent_history
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages, max_tokens=200
        )

        answer = response.choices[0].message.content
        chat_history.append(
            {"role": "assistant", "content": answer, "time": datetime.now().isoformat()}
        )

        return {
            "status": "success",
            "question": message,
            "answer": answer,
            "model": response.model,
            "tokens_used": response.usage.total_tokens,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def get_history():
    """Получить историю чата"""
    return {
        "status": "success",
        "history": chat_history,
        "total_messages": len(chat_history),
    }


@app.delete("/api/history")
async def clear_history():
    """Очистить историю чата"""
    chat_history.clear()
    return {"status": "success", "message": "Chat history cleared"}


@app.get("/health")
async def health():
    """Проверка здоровья системы"""
    return {
        "status": "healthy",
        "mode": "minimal_experiment",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "openai": "enabled",
            "telegram": "disabled",
            "binance": "disabled",
            "domains": "disabled",
        },
        "stats": {"chat_messages": len(chat_history), "uptime": "running"},
    }


if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting Mirai Minimal Server...")
    print("🔑 OpenAI API Key loaded")
    print("🌐 Server will run on http://localhost:8000")
    print("📝 API docs available at http://localhost:8000/docs")
    print()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
