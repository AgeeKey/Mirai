#!/bin/bash
# Quick Start Script для Mirai Minimal Mode

set -e

echo "╔══════════════════════════════════════╗"
echo "║   🤖 MIRAI - MINIMAL MODE START     ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Цвета
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Проверка что мы в правильной директории
cd /root/mirai/mirai-agent

# Проверка venv
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install --quiet openai fastapi uvicorn python-dotenv aiohttp pydantic
else
    source venv/bin/activate
fi

# Экспорт OpenAI ключа
export OPENAI_API_KEY="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"

# Проверка что порт свободен
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}Port 8000 is busy. Stopping old server...${NC}"
    pkill -f simple_server.py || true
    sleep 2
fi

# Проверка файла сервера
if [ ! -f "simple_server.py" ]; then
    echo -e "${RED}Error: simple_server.py not found!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All checks passed${NC}"
echo ""
echo -e "${BLUE}Starting server...${NC}"
echo ""

# Запуск сервера
python3 simple_server.py

# Если скрипт прерван
echo ""
echo -e "${YELLOW}Server stopped${NC}"
