#!/bin/bash
###############################################################################
# MIRAI AGENT - СКРИПТ ЗАПУСКА
# Запускает Mirai Agent в автономном режиме
###############################################################################

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

MIRAI_DIR="/root/mirai/mirai-agent"
VENV_DIR="$MIRAI_DIR/venv"
ENV_FILE="$MIRAI_DIR/.env"

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}           🤖 MIRAI AUTONOMOUS AGENT - ЗАПУСК              ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

# Проверка директории
if [ ! -d "$MIRAI_DIR" ]; then
    echo -e "${RED}❌ Директория $MIRAI_DIR не найдена${NC}"
    exit 1
fi

cd "$MIRAI_DIR"

# Проверка виртуального окружения
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}⚠️  Виртуальное окружение не найдено. Создаю...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Виртуальное окружение создано${NC}"
else
    echo -e "${GREEN}✅ Виртуальное окружение найдено${NC}"
fi

# Проверка .env файла
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${RED}❌ Файл .env не найден в $MIRAI_DIR${NC}"
    echo -e "${YELLOW}💡 Создайте файл .env с необходимыми переменными${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Файл конфигурации найден${NC}"

# Загрузка переменных окружения
set -a
source "$ENV_FILE"
set +a

# Проверка обязательных переменных
REQUIRED_VARS=("OPENAI_API_KEY" "GROK_API_KEY" "TELEGRAM_BOT_TOKEN" "TELEGRAM_CHAT_ID_ADMIN")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo -e "${RED}❌ Отсутствуют обязательные переменные:${NC}"
    for var in "${MISSING_VARS[@]}"; do
        echo -e "${RED}   - $var${NC}"
    done
    exit 1
fi

echo -e "${GREEN}✅ Все обязательные переменные установлены${NC}"

# Вывод конфигурации
echo -e "${BLUE}─────────────────────────────────────────────────────────${NC}"
echo -e "${BLUE}📋 Конфигурация:${NC}"
echo -e "   • OpenAI API: ${GREEN}✅ Настроен${NC}"
echo -e "   • Grok API: ${GREEN}✅ Настроен${NC}"
echo -e "   • Telegram: ${GREEN}✅ Активен${NC}"
echo -e "   • DRY RUN: ${YELLOW}${DRY_RUN:-true}${NC}"
echo -e "   • Autonomous Mode: ${GREEN}${AUTONOMOUS_MODE:-true}${NC}"
echo -e "${BLUE}─────────────────────────────────────────────────────────${NC}"

# Создание директорий для данных
mkdir -p data/logs data/state

# Активация виртуального окружения и запуск
source "$VENV_DIR/bin/activate"

echo -e "${GREEN}🚀 Запуск Mirai Agent...${NC}"
echo -e "${YELLOW}💡 Для остановки нажмите Ctrl+C${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

# Запуск
exec python3 main.py
