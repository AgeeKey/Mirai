#!/bin/bash
# 🛑 Остановка МИРАЙ

echo "🛑 Останавливаю МИРАЙ..."

if pgrep -f mirai_autonomous.py > /dev/null; then
    PID=$(pgrep -f mirai_autonomous.py)
    echo "   Найден процесс: PID $PID"
    
    pkill -f mirai_autonomous.py
    sleep 2
    
    if pgrep -f mirai_autonomous.py > /dev/null; then
        echo "⚠️  Процесс не остановился, принудительное завершение..."
        pkill -9 -f mirai_autonomous.py
        sleep 1
    fi
    
    if pgrep -f mirai_autonomous.py > /dev/null; then
        echo "❌ Не удалось остановить процесс!"
    else
        echo "✅ МИРАЙ остановлена"
    fi
else
    echo "ℹ️  МИРАЙ не запущена"
fi
