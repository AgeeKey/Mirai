#!/bin/bash
# 🌸 MIRAI Quick Start - Упрощённый запуск
# Создано после очистки проекта

echo "🌸 =========================================="
echo "   MIRAI AI Agent - Быстрый старт"
echo "   =========================================="
echo ""

# Цвета
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

cd /root/mirai/mirai-agent

echo -e "${BLUE}Выберите режим запуска:${NC}"
echo ""
echo "1) 🤖 Автономный режим (MIRAI работает сама)"
echo "2) 📊 Веб-дашборд (http://localhost:5000)"
echo "3) 💬 Интерактивный терминал (KAIZEN)"
echo "4) ❓ Задать вопрос MIRAI"
echo "5) 👔 Boss Mode (управление проектом)"
echo "6) 🧪 Тестирование системы"
echo "7) 📈 Статус запущенных процессов"
echo "0) ❌ Выход"
echo ""
read -p "Введите номер: " choice

case $choice in
    1)
        echo -e "${GREEN}🚀 Запускаю автономный режим...${NC}"
        python3 mirai_autonomous.py --interval 180
        ;;
    2)
        echo -e "${GREEN}🚀 Запускаю веб-дашборд...${NC}"
        echo -e "${YELLOW}Откройте в браузере: http://localhost:5000${NC}"
        python3 dashboard_server.py
        ;;
    3)
        echo -e "${GREEN}🚀 Запускаю терминал KAIZEN...${NC}"
        python3 kaizen_terminal.py
        ;;
    4)
        echo -e "${GREEN}💬 Задайте вопрос MIRAI:${NC}"
        python3 ask_mirai.py
        ;;
    5)
        echo -e "${GREEN}👔 Запускаю Boss Mode...${NC}"
        python3 boss_mode.py
        ;;
    6)
        echo -e "${GREEN}🧪 Запускаю тесты...${NC}"
        python3 quick_test_phase3.py
        ;;
    7)
        echo -e "${BLUE}📈 Запущенные процессы MIRAI:${NC}"
        ps aux | grep -E "(mirai|dashboard|kaizen)" | grep -v grep
        echo ""
        echo -e "${BLUE}🔍 Логи:${NC}"
        echo "  - Autonomous: /tmp/kaizen_mirai.log"
        echo "  - Metrics: /tmp/kaizen_mirai_metrics.jsonl"
        ;;
    0)
        echo -e "${YELLOW}До свидания! 👋${NC}"
        exit 0
        ;;
    *)
        echo -e "${YELLOW}⚠️  Неверный выбор${NC}"
        exit 1
        ;;
esac
