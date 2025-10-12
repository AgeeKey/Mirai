#!/bin/bash
# 🛑 Остановка МИРАЙ

echo "🛑 Останавливаю МИРАЙ..."

if pgrep -f mirai_autonomous.py > /dev/null; then
    PID=$(pgrep -f mirai_autonomous.py)
    echo "   Найден процесс: PID $PID"
    
    # Отправляем SIGTERM
    kill $PID
    sleep 3
    
    # Проверяем
    if pgrep -f mirai_autonomous.py > /dev/null; then
        echo "⚠️  Процесс не остановился, принудительное завершение..."
        kill -9 $PID
        sleep 1
    fi
    
    # Финальная проверка
    if pgrep -f mirai_autonomous.py > /dev/null; then
        echo "❌ Не удалось остановить процесс!"
    else
        echo "✅ МИРАЙ остановлена"
        # Удаляем PID файл
        rm -f /tmp/mirai_autonomous.pid
    fi
else
    echo "ℹ️  МИРАЙ не запущена"
    rm -f /tmp/mirai_autonomous.pid
fi
