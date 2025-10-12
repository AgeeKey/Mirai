#!/bin/bash
# MIRAI - Запуск в полностью автономном режиме 24/7

echo "🤖 MIRAI - АВТОНОМНЫЙ РЕЖИМ 24/7"
echo "================================"

cd /root/mirai/mirai-agent

# Активируем виртуальное окружение
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Ошибка: venv не найден"
    exit 1
fi

# Загружаем переменные окружения
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ Ошибка: .env не найден"
    exit 1
fi

echo "✅ Окружение настроено"
echo ""
echo "🚀 Запуск MIRAI в фоновом режиме..."
echo "📝 Логи: /tmp/mirai_autonomous.log"
echo "📝 PID будет сохранен в: /tmp/mirai.pid"
echo ""

# Останавливаем старый процесс если есть
if [ -f /tmp/mirai.pid ]; then
    OLD_PID=$(cat /tmp/mirai.pid)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "⚠️  Останавливаю старый процесс (PID: $OLD_PID)..."
        kill $OLD_PID 2>/dev/null
        sleep 2
    fi
    rm -f /tmp/mirai.pid
fi

# Запускаем в фоне с nohup
nohup python3 autonomous_mode.py > /tmp/mirai_console.log 2>&1 &

# Сохраняем PID
MIRAI_PID=$!
echo $MIRAI_PID > /tmp/mirai.pid

echo "✅ MIRAI запущен в фоне!"
echo "   PID: $MIRAI_PID"
echo ""
echo "📊 Команды управления:"
echo "   • Просмотр логов:   tail -f /tmp/mirai_autonomous.log"
echo "   • Статус процесса:  ps aux | grep autonomous_mode"
echo "   • Остановка:        ./stop_autonomous.sh"
echo ""
echo "🎯 Агент работает автономно 24/7!"
echo "   Он будет:"
echo "   - Писать код"
echo "   - Искать информацию в интернете"
echo "   - Улучшать проект"
echo "   - Создавать полезные утилиты"
echo ""
echo "================================"

# Показываем первые несколько строк лога
sleep 3
echo ""
echo "📋 Первые записи лога:"
echo "--------------------------------"
tail -20 /tmp/mirai_autonomous.log
