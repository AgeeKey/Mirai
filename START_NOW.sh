#!/bin/bash

# 🚀 MIRAI AGENT - АВТОМАТИЧЕСКИЙ ЗАПУСК
# Этот скрипт все сделает за тебя!

set -e  # Остановить при ошибке

echo "╔═══════════════════════════════════════╗"
echo "║   🤖 MIRAI AGENT - БЫСТРЫЙ СТАРТ    ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Переход в директорию
cd /root/mirai/mirai-agent

echo "📂 Рабочая директория: $(pwd)"
echo ""

# ШАГ 1: Виртуальное окружение
echo "📦 ШАГ 1/5: Создание виртуального окружения..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
else
    echo "✅ Виртуальное окружение уже существует"
fi
echo ""

# Активация
source venv/bin/activate
echo "✅ Виртуальное окружение активировано"
echo ""

# ШАГ 2: Установка зависимостей
echo "📥 ШАГ 2/5: Установка зависимостей..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Все библиотеки установлены"
echo ""

# ШАГ 3: Проверка конфигурации
echo "⚙️  ШАГ 3/5: Проверка конфигурации..."

# Проверка API ключей
if grep -q "sk-proj-" .env && grep -q "xai-" .env; then
    echo "✅ API ключи найдены в .env"
else
    echo "⚠️  ВНИМАНИЕ: Проверь API ключи в .env файле!"
fi

# Создание директорий
mkdir -p data/logs
mkdir -p data/backups
mkdir -p state
echo "✅ Директории созданы"
echo ""

# ШАГ 4: Проверка портов
echo "🔍 ШАГ 4/5: Проверка портов..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Порт 8000 уже занят!"
    echo "   Остановите существующий процесс или измените порт"
    echo "   Текущий процесс: $(lsof -Pi :8000 -sTCP:LISTEN)"
else
    echo "✅ Порт 8000 свободен"
fi
echo ""

# ШАГ 5: Запуск
echo "🚀 ШАГ 5/5: ЗАПУСК АГЕНТА..."
echo ""
echo "╔═══════════════════════════════════════╗"
echo "║        MIRAI AGENT ЗАПУСКАЕТСЯ       ║"
echo "╚═══════════════════════════════════════╝"
echo ""
echo "📊 Мониторинг:"
echo "   - Логи агента: tail -f data/logs/ai_agent.log"
echo "   - Логи трейдера: tail -f logs/mirai_agent.log"
echo "   - API здоровье: curl http://localhost:8000/health"
echo ""
echo "⏸️  Остановка: Ctrl+C"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Запуск
python -m core.master_agent
