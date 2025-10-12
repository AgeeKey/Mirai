#!/bin/bash
# MIRAI - Простой запуск автономного агента

echo "🤖 MIRAI - Автономный AI Агент"
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

# Запускаем агента
echo "🚀 Запуск агента..."
python3 run_mirai.py
