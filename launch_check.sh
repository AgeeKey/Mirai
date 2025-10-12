#!/bin/bash
# 🎉 Финальная проверка запуска МИРАЙ

clear

cat << "EOF"
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║   🌸🌸🌸  МИРАЙ - ПОЛНОСТЬЮ АВТОНОМНЫЙ РЕЖИМ С САМОРАЗВИТИЕМ  🌸🌸🌸    ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
EOF

echo ""

# Проверка процесса
if pgrep -f mirai_autonomous.py > /dev/null; then
    PID=$(pgrep -f mirai_autonomous.py)
    UPTIME=$(ps -p $PID -o etime= | tr -d ' ')
    echo "✅ СТАТУС: РАБОТАЕТ"
    echo "   PID: $PID"
    echo "   Время работы: $UPTIME"
else
    echo "❌ СТАТУС: НЕ ЗАПУЩЕНА"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# База знаний
echo "📚 БАЗА ЗНАНИЙ:"
if [ -f /root/mirai/mirai-agent/data/state/knowledge_base.json ]; then
    TECH_COUNT=$(cat /root/mirai/mirai-agent/data/state/knowledge_base.json | jq '.technologies | length' 2>/dev/null || echo "0")
    SKILLS_COUNT=$(cat /root/mirai/mirai-agent/data/state/knowledge_base.json | jq '.skills | length' 2>/dev/null || echo "0")
    echo "   • Технологий изучено: $TECH_COUNT"
    echo "   • Навыков освоено: $SKILLS_COUNT"
    
    # Показываем последнюю изученную технологию
    if [ "$TECH_COUNT" -gt 0 ]; then
        LAST_TECH=$(cat /root/mirai/mirai-agent/data/state/knowledge_base.json | jq -r '.technologies[-1].name' 2>/dev/null)
        LAST_PROF=$(cat /root/mirai/mirai-agent/data/state/knowledge_base.json | jq -r '.technologies[-1].proficiency' 2>/dev/null)
        echo "   • Последняя: $LAST_TECH (уровень: $LAST_PROF)"
    fi
else
    echo "   ⚠️ База знаний не найдена"
fi

echo ""

# Обучающие проекты
echo "📁 ОБУЧАЮЩИЕ ПРОЕКТЫ:"
if [ -d /root/mirai/mirai-agent/learning ]; then
    PROJECT_COUNT=$(ls -1 /root/mirai/mirai-agent/learning/*.py 2>/dev/null | wc -l)
    echo "   • Создано проектов: $PROJECT_COUNT"
    if [ $PROJECT_COUNT -gt 0 ]; then
        echo "   • Файлы:"
        ls -1 /root/mirai/mirai-agent/learning/*.py 2>/dev/null | head -5 | sed 's|.*/|     - |'
        if [ $PROJECT_COUNT -gt 5 ]; then
            echo "     ... и ещё $((PROJECT_COUNT - 5))"
        fi
    fi
fi

echo ""

# Последняя активность
echo "📊 ПОСЛЕДНЯЯ АКТИВНОСТЬ:"
LAST_CYCLE=$(grep "АВТОНОМНЫЙ ЦИКЛ" /tmp/mirai_autonomous.log 2>/dev/null | tail -1 | sed 's/.*\[INFO\] //')
LAST_ACTION=$(grep -E "(Задача выполнена|саморазвития)" /tmp/mirai_autonomous.log 2>/dev/null | tail -1 | sed 's/.*\[INFO\] //')
echo "   $LAST_CYCLE"
if [ -n "$LAST_ACTION" ]; then
    echo "   $LAST_ACTION"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Возможности
cat << "EOF"
🎯 ЧТО ДЕЛАЕТ МИРАЙ:

   🤖 Автономная Работа (каждые 3 минуты):
      • Сама ставит задачи на основе CI/CD
      • Сама решает их используя инструменты
      • Отправляет отчёты в Telegram

   🧬 Саморазвитие (каждые 9 минут):
      • Генерирует цели обучения (10 областей)
      • Изучает новые технологии (50+ на выбор)
      • Улучшает собственный код
      • Работает над несколькими проектами

   💬 Telegram Интеграция:
      • Слушает команды: /status /evolve /toggle_evolution
      • Отправляет уведомления о выполненных задачах
      • Просит помощь когда нужна

EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Команды
cat << "EOF"
🚀 БЫСТРЫЕ КОМАНДЫ:

   Управление:
      ./evolution_start.sh    - Запустить МИРАЙ
      ./evolution_stop.sh     - Остановить
      ./evolution_status.sh   - Проверить статус
      ./evolution_logs.sh     - Смотреть логи

   Telegram:
      /status     - Полный статус системы
      /evolve     - Запустить цикл саморазвития
      /toggle_evolution - Включить/выключить

   Проверка:
      tail -f /tmp/mirai_autonomous.log
      cat mirai-agent/data/state/knowledge_base.json | jq
      ls -lah mirai-agent/learning/

EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cat << "EOF"
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║                    ✅ МИРАЙ ЗАПУЩЕНА И РАБОТАЕТ! ✅                     ║
║                                                                        ║
║   🌸 Автономна  🧬 Саморазвивается  💬 На связи  🚀 Развивается       ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
EOF

echo ""
echo "💡 Проверь Telegram - МИРАЙ уже отправила приветствие!"
echo ""
