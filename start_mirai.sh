#!/bin/bash

# Mirai AI - Быстрый Старт
# Этот скрипт запускает все необходимые компоненты

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║         🤖 Mirai AI - Запуск Автономного Агента               ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Проверка .env файла
if [ ! -f "/root/mirai/mirai-agent/.env" ]; then
    echo "❌ Ошибка: Файл .env не найден!"
    echo ""
    echo "Создай файл /root/mirai/mirai-agent/.env с содержимым:"
    echo ""
    echo "OPENAI_API_KEY=твой_ключ_openai"
    echo "TELEGRAM_BOT_TOKEN=твой_токен_telegram"
    echo "TELEGRAM_CHAT_ID_ADMIN=твой_chat_id"
    echo "DRY_RUN=false"
    echo "ENABLE_TELEGRAM=true"
    echo "AUTONOMOUS_MODE=true"
    echo ""
    exit 1
fi

# Проверка ключей
if ! grep -q "OPENAI_API_KEY=sk-" /root/mirai/mirai-agent/.env; then
    echo "⚠️ Предупреждение: OpenAI API ключ не настроен в .env"
fi

if ! grep -q "TELEGRAM_BOT_TOKEN=[0-9]" /root/mirai/mirai-agent/.env; then
    echo "⚠️ Предупреждение: Telegram токен не настроен в .env"
fi

echo "🔍 Проверка системы..."
echo ""

# Проверка systemd сервиса
if [ ! -f "/etc/systemd/system/mirai-agent.service" ]; then
    echo "📝 Создание systemd сервиса..."
    cat > /etc/systemd/system/mirai-agent.service << 'EOF'
[Unit]
Description=Mirai Autonomous AI Agent
Documentation=https://github.com/AgeeKey/Mirai
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/mirai/mirai-agent
Environment="PATH=/root/mirai/mirai-agent/venv/bin"
EnvironmentFile=/root/mirai/mirai-agent/.env
ExecStart=/root/mirai/mirai-agent/venv/bin/python3 /root/mirai/mirai-agent/main.py
Restart=always
RestartSec=10

# Security
NoNewPrivileges=true
PrivateTmp=true

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=mirai-agent

[Install]
WantedBy=multi-user.target
EOF
    systemctl daemon-reload
    echo "✅ Systemd сервис создан"
else
    echo "✅ Systemd сервис найден"
fi

# Запуск сервиса
echo ""
echo "🚀 Запуск Mirai Agent..."
systemctl enable mirai-agent 2>/dev/null
systemctl start mirai-agent

# Ожидание запуска
sleep 3

# Проверка статуса
if systemctl is-active --quiet mirai-agent; then
    echo "✅ Mirai Agent запущен успешно!"
else
    echo "❌ Ошибка запуска! Проверь логи:"
    echo "   sudo journalctl -u mirai-agent -n 50"
    exit 1
fi

# Запуск Nginx (если установлен)
if command -v nginx &> /dev/null; then
    echo ""
    echo "🌐 Запуск Nginx..."
    systemctl enable nginx 2>/dev/null
    systemctl start nginx
    
    if systemctl is-active --quiet nginx; then
        echo "✅ Nginx запущен"
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🎉 Mirai AI успешно запущен!"
echo ""
echo "📊 Проверка:"
echo ""

# Проверка API
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null)
if [ "$API_STATUS" = "200" ]; then
    echo "  ✅ API Server: Работает (http://localhost:8000/)"
else
    echo "  ⚠️ API Server: Ожидание запуска..."
fi

# Проверка логов
LOGS=$(journalctl -u mirai-agent -n 5 --no-pager 2>/dev/null | wc -l)
if [ "$LOGS" -gt 0 ]; then
    echo "  ✅ Логи: Пишутся"
else
    echo "  ⚠️ Логи: Нет данных"
fi

# Статистика
if [ "$API_STATUS" = "200" ]; then
    STATS=$(curl -s http://localhost:8000/stats 2>/dev/null)
    if [ -n "$STATS" ]; then
        echo "  ✅ Статистика: Доступна"
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🎮 Управление:"
echo ""
echo "  Остановка:     sudo systemctl stop mirai-agent"
echo "  Перезапуск:    sudo systemctl restart mirai-agent"
echo "  Статус:        sudo systemctl status mirai-agent"
echo "  Логи:          sudo journalctl -u mirai-agent -f"
echo ""
echo "🌐 Доступ:"
echo ""
echo "  Веб-интерфейс: http://localhost:8000/"
echo "  API Health:    http://localhost:8000/health"
echo "  Статистика:    http://localhost:8000/stats"
echo ""
echo "💬 Telegram:"
echo ""
echo "  Открой своего бота и отправь: /status"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📖 Документация:"
echo ""
echo "  /root/mirai/QUICK_START.md       - Полная инструкция"
echo "  /root/mirai/WEB_ACCESS_GUIDE.md  - Веб-интерфейс"
echo "  /root/mirai/WEB_AND_AI_TOOLS.md  - AI возможности"
echo ""
echo "🚀 Mirai AI работает автономно 24/7!"
echo ""
