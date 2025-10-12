#!/bin/bash

# MIRAI - Autonomous Agent Launcher

echo "🚀 Запуск MIRAI Autonomous Agent..."
echo "======================================"

cd /root/mirai/mirai-agent

# Активируем виртуальное окружение
source venv/bin/activate

# Загружаем переменные окружения
export $(cat .env | grep -v '^#' | xargs)

# Проверяем OpenAI ключ
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY не найден в .env"
    exit 1
fi

echo "✅ OpenAI ключ загружен: ${OPENAI_API_KEY:0:20}..."
echo ""
echo "🌐 Сервер будет доступен на: http://localhost:8000"
echo "🤖 Агент готов к работе!"
echo ""
echo "======================================"

# Запускаем сервер
python3 agent_server.py
