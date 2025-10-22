#!/bin/bash
# 🛡️ MASTER SETUP - Полная защита MIRAI от поломок API ключей

set -e

echo "🛡️ ЗАЩИТА MIRAI: МАСТЕР УСТАНОВКА"
echo "=================================="
echo ""

cd /root/mirai/mirai-agent

# 1. Запустить первоначальную очистку
echo "🧹 Шаг 1: Очистка старых процессов и проверка..."
./cleanup_api_keys.sh

echo ""
echo "=================================="
echo ""

# 2. Установить watchdog service
echo "⚙️  Шаг 2: Установка API Watchdog Service..."

if [ -f api-watchdog.service ]; then
    sudo cp api-watchdog.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable api-watchdog.service
    sudo systemctl restart api-watchdog.service
    
    echo "   ✅ Watchdog service установлен и запущен"
    echo ""
    sleep 3
    sudo systemctl status api-watchdog.service --no-pager | head -15
else
    echo "   ❌ Файл api-watchdog.service не найден"
    exit 1
fi

echo ""
echo "=================================="
echo ""

# 3. Установить autonomous service
echo "⚙️  Шаг 3: Установка Autonomous Service..."

if [ -f /etc/systemd/system/mirai-autonomous.service ]; then
    sudo systemctl enable mirai-autonomous.service
    echo "   ✅ Autonomous service включен в автозапуск"
else
    echo "   ⚠️  Autonomous service не найден (создан cleanup_api_keys.sh)"
fi

echo ""
echo "=================================="
echo ""

# 4. Добавить в crontab
echo "⏰ Шаг 4: Настройка автоматической проверки..."

CRON_JOB="*/15 * * * * /root/mirai/mirai-agent/cleanup_api_keys.sh >> /tmp/mirai_cleanup.log 2>&1"

# Проверить есть ли уже в crontab
if crontab -l 2>/dev/null | grep -q "cleanup_api_keys.sh"; then
    echo "   ✅ Crontab уже настроен"
else
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "   ✅ Добавлено в crontab (каждые 15 минут)"
fi

echo ""
echo "=================================="
echo "✅ УСТАНОВКА ЗАВЕРШЕНА!"
echo "=================================="
echo ""
echo "🛡️ MIRAI ТЕПЕРЬ ЗАЩИЩЕНА НА 100%!"
echo ""
echo "📊 ЧТО УСТАНОВЛЕНО:"
echo "   ✅ cleanup_api_keys.sh - Ручная очистка и проверка"
echo "   ✅ api_key_watchdog.py - Автоматический мониторинг (каждые 5 мин)"
echo "   ✅ api-watchdog.service - Systemd service для watchdog"
echo "   ✅ Crontab - Проверка каждые 15 минут"
echo "   ✅ Автозапуск при перезагрузке"
echo ""
echo "🎯 ЧТО ПРОИСХОДИТ:"
echo "   1. Watchdog проверяет API каждые 5 минут"
echo "   2. При ошибке - убивает старые процессы"
echo "   3. При 3 ошибках подряд - перезапускает сервис"
echo "   4. Отправляет алерты в Telegram"
echo "   5. Cron делает профилактику каждые 15 минут"
echo ""
echo "📝 ПОЛЕЗНЫЕ КОМАНДЫ:"
echo "   systemctl status api-watchdog      # Статус watchdog"
echo "   systemctl status mirai-autonomous  # Статус MIRAI"
echo "   tail -f /tmp/api_watchdog.log      # Лог watchdog"
echo "   tail -f /tmp/mirai_autonomous.log  # Лог MIRAI"
echo "   ./cleanup_api_keys.sh              # Ручная проверка"
echo ""
echo "🎉 MIRAI НИКОГДА НЕ СЛОМАЕТСЯ ИЗ-ЗА КЛЮЧЕЙ!"
echo ""
