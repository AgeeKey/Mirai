#!/bin/bash

# 🎮 MIRAI AGENT - ПАНЕЛЬ УПРАВЛЕНИЯ
# Удобные команды для работы с агентом

# Цвета для красоты
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║      🤖 MIRAI AGENT - ПАНЕЛЬ УПРАВЛЕНИЯ          ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════╝${NC}"
echo ""

show_menu() {
    echo -e "${GREEN}Что хочешь сделать?${NC}"
    echo ""
    echo "  1) 🚀 Запустить агента"
    echo "  2) 📊 Показать статус"
    echo "  3) 📝 Показать логи (live)"
    echo "  4) 🔍 Проверить API"
    echo "  5) 💰 Статистика торговли"
    echo "  6) 🧠 Спросить AI"
    echo "  7) 🛑 Остановить агента"
    echo "  8) 🔄 Перезапустить"
    echo "  9) 📚 База данных агента"
    echo "  0) ❌ Выход"
    echo ""
    echo -n "Выбери номер: "
}

# Функция 1: Запуск
start_agent() {
    echo -e "${GREEN}🚀 Запуск агента...${NC}"
    cd /root/mirai/mirai-agent
    source venv/bin/activate
    python -m core.master_agent
}

# Функция 2: Статус
show_status() {
    echo -e "${BLUE}📊 Проверка статуса...${NC}"
    
    # Проверка процесса
    if pgrep -f "master_agent" > /dev/null; then
        echo -e "${GREEN}✅ Агент работает${NC}"
        echo -e "   PID: $(pgrep -f master_agent)"
    else
        echo -e "${RED}❌ Агент не запущен${NC}"
    fi
    
    # Проверка API
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API сервер работает${NC}"
        curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "   http://localhost:8000/health"
    else
        echo -e "${RED}❌ API сервер не отвечает${NC}"
    fi
}

# Функция 3: Логи
show_logs() {
    echo -e "${BLUE}📝 Логи агента (Ctrl+C для выхода)...${NC}"
    tail -f /root/mirai/mirai-agent/logs/mirai_agent.log 2>/dev/null || \
    tail -f /root/mirai/mirai-agent/data/logs/ai_agent.log 2>/dev/null || \
    echo "Логи не найдены"
}

# Функция 4: API тест
test_api() {
    echo -e "${BLUE}🔍 Проверка API...${NC}"
    echo ""
    
    echo -e "${YELLOW}1. Health check:${NC}"
    curl -s http://localhost:8000/health | python3 -m json.tool
    echo ""
    
    echo -e "${YELLOW}2. Stats:${NC}"
    curl -s http://localhost:8000/stats | python3 -m json.tool
    echo ""
}

# Функция 5: Торговля
trading_stats() {
    echo -e "${BLUE}💰 Статистика торговли...${NC}"
    curl -s http://localhost:8000/trading/status | python3 -m json.tool
}

# Функция 6: AI вопрос
ask_ai() {
    echo -e "${BLUE}🧠 Спроси что-нибудь у AI...${NC}"
    echo -n "Вопрос: "
    read question
    
    curl -s -X POST http://localhost:8000/ai/ask \
      -H "Content-Type: application/json" \
      -d "{\"question\": \"$question\"}" | python3 -m json.tool
}

# Функция 7: Остановка
stop_agent() {
    echo -e "${YELLOW}🛑 Остановка агента...${NC}"
    pkill -f "master_agent"
    sleep 2
    if pgrep -f "master_agent" > /dev/null; then
        echo -e "${RED}❌ Не удалось остановить. Пробую SIGKILL...${NC}"
        pkill -9 -f "master_agent"
    else
        echo -e "${GREEN}✅ Агент остановлен${NC}"
    fi
}

# Функция 8: Перезапуск
restart_agent() {
    stop_agent
    sleep 2
    start_agent
}

# Функция 9: База данных
show_db() {
    echo -e "${BLUE}📚 База данных агента...${NC}"
    echo ""
    
    DB="/root/mirai/mirai-agent/state/agent_memory.db"
    
    if [ -f "$DB" ]; then
        echo -e "${YELLOW}Задачи:${NC}"
        sqlite3 "$DB" "SELECT COUNT(*) FROM tasks;" 2>/dev/null || echo "0"
        
        echo ""
        echo -e "${YELLOW}Последние 5 задач:${NC}"
        sqlite3 "$DB" "SELECT * FROM tasks ORDER BY created_at DESC LIMIT 5;" 2>/dev/null || echo "Нет данных"
    else
        echo -e "${RED}База данных не найдена${NC}"
    fi
}

# Главный цикл
while true; do
    show_menu
    read choice
    echo ""
    
    case $choice in
        1) start_agent ;;
        2) show_status ;;
        3) show_logs ;;
        4) test_api ;;
        5) trading_stats ;;
        6) ask_ai ;;
        7) stop_agent ;;
        8) restart_agent ;;
        9) show_db ;;
        0) echo -e "${GREEN}Пока! 👋${NC}"; exit 0 ;;
        *) echo -e "${RED}Неверный выбор!${NC}" ;;
    esac
    
    echo ""
    echo -e "${YELLOW}Нажми Enter для продолжения...${NC}"
    read
    clear
done
