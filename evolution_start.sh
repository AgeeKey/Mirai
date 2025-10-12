#!/bin/bash
# 🚀 Запуск МИРАЙ с системой саморазвития

echo "🌸 Запускаю МИРАЙ с саморазвитием..."

# Проверяем не запущена ли уже
if pgrep -f mirai_autonomous.py > /dev/null; then
    echo "⚠️  МИРАЙ уже запущена! Останавливаю старый процесс..."
    pkill -9 -f mirai_autonomous.py
    sleep 3
fi

# Переходим в директорию
cd /root/mirai/mirai-agent

# Активируем venv если есть
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Запускаем В ФОНЕ с nohup и отключением вывода
echo "🚀 Запуск в фоновом режиме..."
nohup python3 mirai_autonomous.py --interval 180 > /tmp/mirai_autonomous.log 2>&1 &

# Запоминаем PID
MIRAI_PID=$!
echo $MIRAI_PID > /tmp/mirai_autonomous.pid

sleep 3

# Проверяем
if pgrep -f mirai_autonomous.py > /dev/null; then
    PID=$(pgrep -f mirai_autonomous.py)
    echo ""
    echo "✅ МИРАЙ запущена успешно!"
    echo "   PID: $PID (сохранён в /tmp/mirai_autonomous.pid)"
    echo "   Интервал: 180 секунд"
    echo "   Саморазвитие: Каждые 3 цикла"
    echo "   Режим: ФОНОВЫЙ (можно закрыть терминал)"
    echo ""
    echo "📝 Логи: tail -f /tmp/mirai_autonomous.log"
    echo "🧠 База знаний: cat data/state/knowledge_base.json"
    echo "💬 Telegram: Проверь сообщения от бота!"
    echo ""
    echo "🎯 Используй команды Telegram:"
    echo "   /status - проверить статус"
    echo "   /evolve - запустить саморазвитие"
    echo ""
    echo "🛑 Для остановки: ./evolution_stop.sh"
else
    echo "❌ Ошибка запуска! Смотри логи:"
    echo "   tail -50 /tmp/mirai_autonomous.log"
fi
