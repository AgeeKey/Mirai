#!/bin/bash
# 🧬 МИРАЙ Саморазвитие - Быстрые Команды

echo "🌸 МИРАЙ - Система Саморазвития"
echo "================================"
echo ""

# Проверка статуса
if pgrep -f mirai_autonomous.py > /dev/null; then
    PID=$(pgrep -f mirai_autonomous.py)
    echo "✅ МИРАЙ запущена (PID: $PID)"
else
    echo "❌ МИРАЙ не запущена"
fi

echo ""
echo "📊 База Знаний:"
if [ -f /root/mirai/mirai-agent/data/state/knowledge_base.json ]; then
    TECH_COUNT=$(cat /root/mirai/mirai-agent/data/state/knowledge_base.json | grep -c '"name":')
    echo "   Технологий изучено: $TECH_COUNT"
else
    echo "   База знаний не найдена"
fi

echo ""
echo "📁 Обучающие проекты:"
if [ -d /root/mirai/mirai-agent/learning ]; then
    PROJECT_COUNT=$(ls -1 /root/mirai/mirai-agent/learning/*.py 2>/dev/null | wc -l)
    echo "   Создано проектов: $PROJECT_COUNT"
    if [ $PROJECT_COUNT -gt 0 ]; then
        echo "   Файлы:"
        ls -1 /root/mirai/mirai-agent/learning/*.py 2>/dev/null | sed 's/^/     - /'
    fi
else
    echo "   Директория не найдена"
fi

echo ""
echo "🎯 Быстрые команды:"
echo ""
echo "  Управление:"
echo "    ./evolution_start.sh     - Запустить МИРАЙ с саморазвитием"
echo "    ./evolution_stop.sh      - Остановить МИРАЙ"
echo "    ./evolution_status.sh    - Этот скрипт"
echo "    ./evolution_logs.sh      - Смотреть логи в реальном времени"
echo ""
echo "  Тестирование:"
echo "    cd /root/mirai/mirai-agent && python3 test_self_evolution.py"
echo ""
echo "  Telegram команды:"
echo "    /status или /статус          - Полный статус"
echo "    /evolve или /развивайся      - Запустить цикл саморазвития"
echo "    /toggle_evolution            - Включить/выключить"
echo ""
echo "  Файлы:"
echo "    📝 Логи: /tmp/mirai_autonomous.log"
echo "    🧠 База знаний: data/state/knowledge_base.json"
echo "    📚 Проекты: learning/"
echo "    📖 Документация: SELF_EVOLUTION_GUIDE.md"
echo ""
