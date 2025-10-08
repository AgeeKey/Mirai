#!/bin/bash#!/bin/bash

###############################################################################set -e

# MIRAI AGENT - HEALTH CHECK

# Проверяет состояние всех компонентов системыAPI_URL=${API_URL:-http://127.0.0.1:8000/health}

###############################################################################MASTER_SERVICE=${MASTER_SERVICE:-mirai-master}



set -estatus_ok=true



# Цветаif systemctl list-units --type=service | grep -q "$MASTER_SERVICE"; then

RED='\033[0;31m'  if ! systemctl is-active --quiet "$MASTER_SERVICE"; then

GREEN='\033[0;32m'    echo "❌ Service $MASTER_SERVICE inactive"

YELLOW='\033[1;33m'    status_ok=false

BLUE='\033[0;34m'  fi

NC='\033[0m'fi



echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL" || echo 000)

echo -e "${BLUE}           🏥 MIRAI HEALTH CHECK                            ${NC}"if [ "$HTTP_CODE" != "200" ]; then

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"  echo "❌ API health check failed (status $HTTP_CODE)"

  status_ok=false

PASSED=0else

FAILED=0  echo "✅ API health check passed"

fi

# Функция проверки

check() {if [ "$status_ok" = true ]; then

    local name="$1"  echo "✅ Mirai Agent healthy"

    local test_cmd="$2"  exit 0

    else

    echo -en "${BLUE}Проверка: ${name}...${NC} "  echo "⚠️ Issues detected"

      exit 1

    if eval "$test_cmd" > /dev/null 2>&1; thenfi

        echo -e "${GREEN}✅ OK${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        ((FAILED++))
        return 1
    fi
}

echo ""
echo -e "${YELLOW}🔍 Проверка системных компонентов...${NC}"
echo ""

# 1. Процесс работает
check "Процесс Mirai запущен" "pgrep -f 'python3.*main.py' || systemctl is-active mirai-agent"

# 2. API сервер отвечает
check "API сервер (порт 8000)" "curl -sf http://localhost:8000/health"

# 3. База данных существует
check "База данных SQLite" "test -f /root/mirai/mirai-agent/data/state/mirai.db"

# 4. Логи пишутся
check "Директория логов" "test -d /root/mirai/mirai-agent/data/logs"

# 5. Переменные окружения
check "Файл .env" "test -f /root/mirai/mirai-agent/.env"

# 6. Виртуальное окружение
check "Виртуальное окружение" "test -d /root/mirai/mirai-agent/venv"

# 7. Python зависимости
check "OpenAI библиотека" "/root/mirai/mirai-agent/venv/bin/python3 -c 'import openai'"
check "FastAPI библиотека" "/root/mirai/mirai-agent/venv/bin/python3 -c 'import fastapi'"
check "Telegram библиотека" "/root/mirai/mirai-agent/venv/bin/python3 -c 'import telegram'"

echo ""
echo -e "${BLUE}─────────────────────────────────────────────────────────${NC}"
echo -e "${YELLOW}📊 Статистика API сервера:${NC}"
echo ""

# Проверка эндпоинтов API
API_BASE="http://localhost:8000"

if curl -sf "$API_BASE/health" > /dev/null 2>&1; then
    echo -e "${GREEN}• Health endpoint:${NC}"
    curl -s "$API_BASE/health" | python3 -m json.tool || echo "  (JSON parse error)"
    
    echo ""
    echo -e "${GREEN}• Status endpoint:${NC}"
    curl -s "$API_BASE/status" | python3 -m json.tool 2>/dev/null || echo "  (нет данных)"
else
    echo -e "${RED}❌ API сервер недоступен${NC}"
fi

echo ""
echo -e "${BLUE}─────────────────────────────────────────────────────────${NC}"
echo -e "${YELLOW}📝 Последние логи (10 строк):${NC}"
echo ""

if [ -f /root/mirai/mirai-agent/data/logs/mirai_agent.log ]; then
    tail -10 /root/mirai/mirai-agent/data/logs/mirai_agent.log
else
    echo -e "${YELLOW}  (логи не найдены)${NC}"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}           РЕЗУЛЬТАТЫ ПРОВЕРКИ                             ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Успешно: $PASSED${NC}"
echo -e "${RED}Ошибок: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ Все проверки пройдены! Mirai работает нормально.${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Обнаружены проблемы. Проверьте логи.${NC}"
    exit 1
fi
