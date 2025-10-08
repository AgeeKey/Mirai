#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# 🤖 MIRAI QUICK DIAGNOSTICS
# Быстрая проверка работоспособности всех компонентов
# ═══════════════════════════════════════════════════════════

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🤖 MIRAI DIAGNOSTICS - $(date +"%Y-%m-%d %H:%M:%S")    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

SCORE=0
MAX_SCORE=9

# 1. Systemd
echo -e "${YELLOW}1️⃣  Systemd (24/7):${NC}"
if systemctl is-active mirai-agent >/dev/null 2>&1; then
    echo -e "  ${GREEN}✅ Active${NC}"
    ((SCORE++))
else
    echo -e "  ${RED}❌ Inactive${NC}"
fi

if systemctl is-enabled mirai-agent >/dev/null 2>&1; then
    echo -e "  ${GREEN}✅ Enabled (автозапуск)${NC}"
    ((SCORE++))
else
    echo -e "  ${RED}❌ Disabled${NC}"
fi

# 2. AI запросы
echo ""
echo -e "${YELLOW}2️⃣  AI активность:${NC}"
AI_COUNT=$(sudo journalctl -u mirai-agent --since "5 min ago" 2>/dev/null | grep -c "api.openai.com" || echo 0)
if [ "$AI_COUNT" -gt 0 ]; then
    echo -e "  ${GREEN}✅ $AI_COUNT запросов к GPT-4${NC}"
    ((SCORE++))
else
    echo -e "  ${RED}❌ Нет запросов к AI${NC}"
fi

# 3. API сервер
echo ""
echo -e "${YELLOW}3️⃣  API сервер:${NC}"
if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
    echo -e "  ${GREEN}✅ /health OK${NC}"
    ((SCORE++))
else
    echo -e "  ${RED}❌ API недоступен${NC}"
fi

# 4. Задачи создаются
echo ""
echo -e "${YELLOW}4️⃣  Автономные задачи:${NC}"
CREATED=$(sudo journalctl -u mirai-agent --since "10 min ago" 2>/dev/null | grep -c "Task created" || echo 0)
if [ "$CREATED" -gt 0 ]; then
    echo -e "  ${GREEN}✅ Создано: $CREATED${NC}"
    ((SCORE++))
else
    echo -e "  ${RED}❌ Задачи не создаются${NC}"
fi

# 5. Задачи выполняются
COMPLETED=$(sudo journalctl -u mirai-agent --since "10 min ago" 2>/dev/null | grep -c "Task completed" || echo 0)
if [ "$COMPLETED" -gt 0 ]; then
    echo -e "  ${GREEN}✅ Выполнено: $COMPLETED${NC}"
    ((SCORE++))
else
    echo -e "  ${RED}❌ Задачи не выполняются${NC}"
fi

# 6. Telegram
echo ""
echo -e "${YELLOW}5️⃣  Telegram бот:${NC}"
TG_COUNT=$(sudo journalctl -u mirai-agent --since "2 min ago" 2>/dev/null | grep -c "telegram.org" || echo 0)
if [ "$TG_COUNT" -gt 0 ]; then
    echo -e "  ${GREEN}✅ Активен ($TG_COUNT запросов)${NC}"
    ((SCORE++))
else
    echo -e "  ${RED}❌ Не активен${NC}"
fi

# 7. База данных
echo ""
echo -e "${YELLOW}6️⃣  База данных:${NC}"
if [ -f /root/mirai/mirai-agent/data/state/mirai.db ]; then
    SIZE=$(du -h /root/mirai/mirai-agent/data/state/mirai.db | cut -f1)
    echo -e "  ${GREEN}✅ Существует ($SIZE)${NC}"
    ((SCORE++))
else
    echo -e "  ${RED}❌ Не найдена${NC}"
fi

# 8. Процесс
echo ""
echo -e "${YELLOW}7️⃣  Процесс:${NC}"
PID=$(pgrep -f 'python3.*main.py' || true)
if [ -n "$PID" ]; then
    MEM=$(ps -p "$PID" -o rss= | awk '{print int($1/1024)}')
    echo -e "  ${GREEN}✅ PID: $PID (Memory: ${MEM}MB)${NC}"
    ((SCORE++))
else
    echo -e "  ${RED}❌ Процесс не найден${NC}"
fi

# 9. Ошибки
echo ""
echo -e "${YELLOW}8️⃣  Ошибки:${NC}"
ERROR_COUNT=$(sudo journalctl -u mirai-agent --since "5 min ago" 2>/dev/null | grep -i "ERROR" | wc -l)
if [ "$ERROR_COUNT" -eq 0 ]; then
    echo -e "  ${GREEN}✅ Нет ошибок${NC}"
fi

# Итог
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}ОЦЕНКА: $SCORE/$MAX_SCORE${NC}"

if [ "$SCORE" -ge 8 ]; then
    echo -e "${GREEN}🟢 ОТЛИЧНО! Всё работает!${NC}"
elif [ "$SCORE" -ge 6 ]; then
    echo -e "${YELLOW}🟡 ХОРОШО. Есть мелкие проблемы.${NC}"
else
    echo -e "${RED}🔴 КРИТИЧНО! Требуется внимание.${NC}"
fi

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}💡 Полезные команды:${NC}"
echo "  sudo journalctl -u mirai-agent -f    # Логи real-time"
echo "  curl http://localhost:8000/health    # Проверка API"
echo "  curl http://localhost:8000/stats     # Статистика"
echo ""
