#!/bin/bash
#
# 🚀 NASA-Level Learning System - Service Installation Script
# Устанавливает systemd сервисы для автоматического запуска
#

set -e

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║  🚀 NASA-Level Learning System - Установка Systemd Services         ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Этот скрипт требует права root. Запустите: sudo $0"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📁 Рабочая директория: $SCRIPT_DIR"
echo ""

# 1. Копируем service файлы
echo "📋 Шаг 1/5: Копируем service файлы в /etc/systemd/system/..."
cp "$SCRIPT_DIR/nasa-learning.service" /etc/systemd/system/
cp "$SCRIPT_DIR/nasa-dashboard.service" /etc/systemd/system/
echo "✅ Service файлы скопированы"
echo ""

# 2. Reload systemd
echo "🔄 Шаг 2/5: Перезагружаем systemd daemon..."
systemctl daemon-reload
echo "✅ Systemd daemon перезагружен"
echo ""

# 3. Enable services (автозапуск при загрузке)
echo "🔧 Шаг 3/5: Включаем автозапуск сервисов..."
systemctl enable nasa-learning.service
systemctl enable nasa-dashboard.service
echo "✅ Автозапуск включен"
echo ""

# 4. Start services
echo "🚀 Шаг 4/5: Запускаем сервисы..."
systemctl start nasa-learning.service
sleep 2
systemctl start nasa-dashboard.service
echo "✅ Сервисы запущены"
echo ""

# 5. Check status
echo "📊 Шаг 5/5: Проверяем статус сервисов..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🤖 NASA Learning Service:"
systemctl status nasa-learning.service --no-pager -l | head -15
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Dashboard Service:"
systemctl status nasa-dashboard.service --no-pager -l | head -15
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║  ✅ УСТАНОВКА ЗАВЕРШЕНА!                                            ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 ПОЛЕЗНЫЕ КОМАНДЫ:"
echo ""
echo "🔍 Проверить статус:"
echo "   sudo systemctl status nasa-learning"
echo "   sudo systemctl status nasa-dashboard"
echo ""
echo "📜 Просмотр логов:"
echo "   sudo journalctl -u nasa-learning -f"
echo "   sudo journalctl -u nasa-dashboard -f"
echo "   tail -f /tmp/kaizen_mirai.log"
echo ""
echo "🛑 Остановить сервисы:"
echo "   sudo systemctl stop nasa-learning"
echo "   sudo systemctl stop nasa-dashboard"
echo ""
echo "🔄 Перезапустить сервисы:"
echo "   sudo systemctl restart nasa-learning"
echo "   sudo systemctl restart nasa-dashboard"
echo ""
echo "❌ Отключить автозапуск:"
echo "   sudo systemctl disable nasa-learning"
echo "   sudo systemctl disable nasa-dashboard"
echo ""
echo "🌐 Dashboard доступен на:"
echo "   http://localhost:5000"
echo "   http://localhost:5000/api/nasa/status"
echo ""
echo "🎯 Autonomous Learning работает в фоне!"
echo "   Логи: /tmp/kaizen_mirai.log"
echo "   Метрики: /tmp/kaizen_mirai_metrics.jsonl"
echo ""
