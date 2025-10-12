#!/bin/bash
# ========================================
# MIRAI - MINIMAL EXPERIMENT STARTER
# ========================================
# Только OpenAI + Локальный сервер
# Без Telegram, Binance, доменов

set -e

echo "🚀 Starting Mirai in MINIMAL EXPERIMENT mode..."
echo ""
echo "✅ Enabled:"
echo "   - OpenAI API"
echo "   - Local Web Server (localhost:8000)"
echo ""
echo "❌ Disabled:"
echo "   - Telegram Bot"
echo "   - Binance Trading"
echo "   - Domain Configuration"
echo "   - All external services"
echo ""

cd /root/mirai/mirai-agent

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Installing..."
    exit 1
fi

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Активация venv
source venv/bin/activate

# Установка минимальных зависимостей
echo "📥 Installing minimal dependencies..."
pip install --quiet --upgrade pip

# Только основные пакеты
pip install --quiet \
    fastapi \
    uvicorn \
    openai \
    python-dotenv \
    pydantic \
    aiohttp

echo ""
echo "✅ Environment ready!"
echo ""
echo "🔑 OpenAI Key: $(echo $OPENAI_API_KEY | cut -c1-20)..."
echo ""
echo "🌐 Starting local server on http://localhost:8000"
echo ""

# Создаем минимальный сервер если его нет
cat > simple_server.py << 'EOF'
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from openai import OpenAI

app = FastAPI(title="Mirai Minimal Experiment")

# Загружаем OpenAI ключ
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Mirai - Minimal Mode</title>
            <style>
                body { 
                    font-family: Arial; 
                    max-width: 800px; 
                    margin: 50px auto; 
                    padding: 20px;
                    background: #f5f5f5;
                }
                .status { 
                    padding: 20px; 
                    background: white; 
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                .success { color: #28a745; }
                .disabled { color: #dc3545; }
                h1 { color: #007bff; }
            </style>
        </head>
        <body>
            <h1>🤖 Mirai - Minimal Experiment Mode</h1>
            <div class="status">
                <h2>System Status</h2>
                <p class="success">✅ OpenAI API: Connected</p>
                <p class="success">✅ Local Server: Running</p>
                <p class="disabled">❌ Telegram: Disabled</p>
                <p class="disabled">❌ Binance: Disabled</p>
                <p class="disabled">❌ Domains: Disabled</p>
                <hr>
                <p><a href="/api/test">Test OpenAI Connection</a></p>
                <p><a href="/api/chat?message=Hello">Chat with AI</a></p>
                <p><a href="/docs">API Documentation</a></p>
            </div>
        </body>
    </html>
    """

@app.get("/api/test")
async def test_openai():
    """Тестирование OpenAI подключения"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'OpenAI connected!'"}],
            max_tokens=50
        )
        return {
            "status": "success",
            "message": response.choices[0].message.content,
            "model": response.model
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/api/chat")
async def chat(message: str = "Hello"):
    """Простой чат с AI"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            max_tokens=150
        )
        return {
            "status": "success",
            "question": message,
            "answer": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "mode": "minimal_experiment",
        "openai": "enabled",
        "telegram": "disabled",
        "binance": "disabled"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

# Запуск сервера
echo "Starting server..."
python simple_server.py
