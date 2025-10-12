#!/bin/bash
# MIRAI - Запуск веб-интерфейса агента

echo "🌐 MIRAI - Веб-интерфейс"
echo "================================"

cd /root/mirai/mirai-agent

# Активируем виртуальное окружение
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Виртуальное окружение активировано"
else
    echo "❌ Ошибка: venv не найден"
    exit 1
fi

# Проверяем .env
if [ ! -f ".env" ]; then
    echo "❌ Ошибка: .env файл не найден"
    exit 1
fi

# Загружаем переменные окружения
export $(cat .env | grep -v '^#' | xargs)

echo "🚀 Запуск веб-сервера на http://localhost:8000"
echo "📝 Для остановки нажмите Ctrl+C"
echo ""

# Запускаем сервер
python3 agent_server.py
