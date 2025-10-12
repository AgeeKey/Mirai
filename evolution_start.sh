#!/bin/bash
# 🚀 Запуск МИРАЙ с системой саморазвития

echo "🌸 Запускаю МИРАЙ с саморазвитием..."

# Проверяем не запущена ли уже
if pgrep -f mirai_autonomous.py > /dev/null; then
    echo "⚠️  МИРАЙ уже запущена! Останавливаю старый процесс..."
    pkill -f mirai_autonomous.py
    sleep 2
fi

# Переходим в директорию
cd /root/mirai/mirai-agent

# Активируем venv если есть
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Запускаем
echo "🚀 Запуск..."
nohup python3 mirai_autonomous.py --interval 180 > /tmp/mirai_autonomous.log 2>&1 &

sleep 3

# Проверяем
if pgrep -f mirai_autonomous.py > /dev/null; then
    PID=$(pgrep -f mirai_autonomous.py)
    echo ""
    echo "✅ МИРАЙ запущена успешно!"
    echo "   PID: $PID"
    echo "   Интервал: 180 секунд"
    echo "   Саморазвитие: Каждые 3 цикла"
    echo ""
    echo "📝 Логи: tail -f /tmp/mirai_autonomous.log"
    echo "🧠 База знаний: cat data/state/knowledge_base.json"
    echo "💬 Telegram: Проверь сообщения от бота!"
    echo ""
    echo "🎯 Используй команды Telegram:"
    echo "   /status - проверить статус"
    echo "   /evolve - запустить саморазвитие"
else
    echo "❌ Ошибка запуска! Смотри логи:"
    echo "   tail -50 /tmp/mirai_autonomous.log"
fi
