#!/bin/bash
# MIRAI - Проверка статуса автономного режима

echo "📊 СТАТУС MIRAI AUTONOMOUS MODE"
echo "================================"

# Проверка PID файла
if [ -f /tmp/mirai.pid ]; then
    PID=$(cat /tmp/mirai.pid)
    echo "📝 PID файл найден: $PID"
    
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ MIRAI работает (PID: $PID)"
        echo ""
        
        # Информация о процессе
        echo "📈 Информация о процессе:"
        ps -p $PID -o pid,ppid,cmd,%mem,%cpu,etime
        
        echo ""
        echo "💾 Использование ресурсов:"
        ps -p $PID -o %mem,%cpu,rss | tail -1
    else
        echo "❌ MIRAI не запущен (PID из файла не активен)"
        rm -f /tmp/mirai.pid
    fi
else
    echo "❌ PID файл не найден - MIRAI не запущен"
    
    # Проверяем вручную
    PIDS=$(pgrep -f "autonomous_mode.py")
    if [ ! -z "$PIDS" ]; then
        echo "⚠️  Найдены процессы autonomous_mode: $PIDS"
    fi
fi

echo ""
echo "================================"
echo "📋 Последние 30 строк лога:"
echo "================================"

if [ -f /tmp/mirai_autonomous.log ]; then
    tail -30 /tmp/mirai_autonomous.log
else
    echo "⚠️  Лог файл не найден"
fi

echo ""
echo "================================"
echo "📊 Размер лог файла:"
if [ -f /tmp/mirai_autonomous.log ]; then
    ls -lh /tmp/mirai_autonomous.log
fi

echo ""
echo "💡 Команды управления:"
echo "   • Запуск:     ./start_autonomous.sh"
echo "   • Остановка:  ./stop_autonomous.sh"
echo "   • Логи live:  tail -f /tmp/mirai_autonomous.log"
