#!/bin/bash
# MIRAI - Остановка автономного режима

echo "🛑 Остановка MIRAI..."

if [ -f /tmp/mirai.pid ]; then
    PID=$(cat /tmp/mirai.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "   Останавливаю процесс (PID: $PID)..."
        kill $PID
        sleep 2
        
        # Проверяем что процесс остановлен
        if ps -p $PID > /dev/null 2>&1; then
            echo "   Принудительная остановка..."
            kill -9 $PID
        fi
        
        echo "✅ MIRAI остановлен"
        rm -f /tmp/mirai.pid
    else
        echo "⚠️  Процесс с PID $PID не найден"
        rm -f /tmp/mirai.pid
    fi
else
    echo "⚠️  PID файл не найден"
    echo "   Попытка найти процесс вручную..."
    
    PIDS=$(pgrep -f "autonomous_mode.py")
    if [ ! -z "$PIDS" ]; then
        echo "   Найдены процессы: $PIDS"
        kill $PIDS
        echo "✅ Процессы остановлены"
    else
        echo "❌ MIRAI процессы не найдены"
    fi
fi

echo ""
echo "📊 Последние записи лога:"
echo "--------------------------------"
if [ -f /tmp/mirai_autonomous.log ]; then
    tail -30 /tmp/mirai_autonomous.log
fi
