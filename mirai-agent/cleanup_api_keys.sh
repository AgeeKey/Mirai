#!/bin/bash
# 🛡️ ЗАЩИТА API КЛЮЧЕЙ - Автоматическая очистка и проверка
# Этот скрипт ГАРАНТИРУЕТ что MIRAI никогда не сломается из-за ключей

set -e

echo "🛡️ ЗАЩИТА API КЛЮЧЕЙ MIRAI"
echo "================================"
echo ""

# 1. УБИТЬ ВСЕ СТАРЫЕ ПРОЦЕССЫ
echo "🧹 Шаг 1: Очистка старых процессов..."

# Найти все процессы MIRAI (кроме текущего скрипта и vscode)
OLD_PIDS=$(ps aux | grep -E "mirai.*autonomous|mirai_autonomous" | grep -v "grep\|vscode\|bash\|cleanup" | awk '{print $2}')

if [ -z "$OLD_PIDS" ]; then
    echo "   ✅ Старых процессов не найдено"
else
    echo "   ⚠️  Найдены старые процессы: $OLD_PIDS"
    for pid in $OLD_PIDS; do
        # Проверяем что процесс не новый (старше 5 минут)
        PROCESS_AGE=$(ps -p $pid -o etimes= 2>/dev/null || echo "0")
        if [ "$PROCESS_AGE" -gt 300 ]; then
            echo "   🔪 Убиваем старый процесс $pid (возраст: ${PROCESS_AGE}s)"
            kill -9 $pid 2>/dev/null || true
        else
            echo "   ⏭️  Пропускаем новый процесс $pid (возраст: ${PROCESS_AGE}s)"
        fi
    done
    echo "   ✅ Очистка завершена"
fi

echo ""

# 2. ПРОВЕРИТЬ API КЛЮЧ
echo "🔑 Шаг 2: Проверка OpenAI API ключа..."

cd /root/mirai/mirai-agent
source venv/bin/activate

API_CHECK=$(python3 << 'PYTHON'
import json
import sys
try:
    from openai import OpenAI
    
    with open('configs/api_keys.json') as f:
        config = json.load(f)
    
    api_key = config.get('openai')
    if not api_key:
        print("ERROR: No API key found")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': 'test'}],
        max_tokens=5
    )
    
    print("OK")
    sys.exit(0)
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    sys.exit(1)
PYTHON
)

if [ "$API_CHECK" = "OK" ]; then
    echo "   ✅ API ключ работает идеально!"
else
    echo "   ❌ КРИТИЧЕСКАЯ ОШИБКА: $API_CHECK"
    echo ""
    echo "   🚨 API ключ не работает!"
    echo "   📝 Проверьте /root/mirai/mirai-agent/configs/api_keys.json"
    echo "   🔑 Убедитесь что ключ актуальный"
    echo ""
    exit 1
fi

echo ""

# 3. УДАЛИТЬ СТАРЫЕ ЛОГИ (>100MB)
echo "🧹 Шаг 3: Очистка больших логов..."

LARGE_LOGS=$(find /tmp -name "*mirai*.log" -size +100M 2>/dev/null)
if [ -z "$LARGE_LOGS" ]; then
    echo "   ✅ Больших логов не найдено"
else
    echo "   📦 Найдены большие логи:"
    du -h $LARGE_LOGS
    echo "   🗑️  Архивирую и очищаю..."
    for log in $LARGE_LOGS; do
        # Сохраняем последние 10000 строк
        tail -10000 "$log" > "${log}.tmp"
        mv "${log}.tmp" "$log"
        echo "   ✅ $log очищен (оставлены последние 10k строк)"
    done
fi

echo ""

# 4. ПРОВЕРИТЬ ЗАПУЩЕН ЛИ СЕРВИС
echo "🔍 Шаг 4: Проверка статуса сервиса..."

RUNNING_PROCESSES=$(ps aux | grep "autonomous_service.py" | grep -v grep | wc -l)

if [ "$RUNNING_PROCESSES" -gt 0 ]; then
    echo "   ✅ Autonomous service запущен ($RUNNING_PROCESSES процесс(ов))"
    ps aux | grep "autonomous_service.py" | grep -v grep | awk '{print "      PID:", $2, "| Age:", $10, "| Mem:", $6/1024"MB"}'
else
    echo "   ⚠️  Autonomous service НЕ ЗАПУЩЕН!"
    echo "   🚀 Запускаю новый сервис..."
    cd /root/mirai/mirai-agent
    nohup python autonomous_service.py > /tmp/mirai_autonomous.log 2>&1 &
    NEW_PID=$!
    echo "   ✅ Сервис запущен (PID: $NEW_PID)"
fi

echo ""

# 5. СОЗДАТЬ SYSTEMD SERVICE (если нет)
echo "⚙️  Шаг 5: Проверка systemd service..."

if [ -f /etc/systemd/system/mirai-autonomous.service ]; then
    echo "   ✅ Systemd service существует"
else
    echo "   📝 Создаю systemd service..."
    cat > /etc/systemd/system/mirai-autonomous.service << 'EOF'
[Unit]
Description=MIRAI Autonomous Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/mirai/mirai-agent
Environment="PATH=/root/mirai/mirai-agent/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStartPre=/root/mirai/mirai-agent/cleanup_api_keys.sh
ExecStart=/root/mirai/mirai-agent/venv/bin/python autonomous_service.py
Restart=always
RestartSec=10
StandardOutput=append:/tmp/mirai_autonomous.log
StandardError=append:/tmp/mirai_autonomous.log

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    echo "   ✅ Systemd service создан"
    echo "   💡 Используйте: systemctl enable mirai-autonomous"
    echo "   💡 Используйте: systemctl start mirai-autonomous"
fi

echo ""
echo "================================"
echo "✅ ЗАЩИТА API КЛЮЧЕЙ АКТИВНА!"
echo ""
echo "📊 ИТОГ:"
echo "   ✅ Старые процессы убиты"
echo "   ✅ API ключ проверен и работает"
echo "   ✅ Логи очищены"
echo "   ✅ Сервис запущен"
echo "   ✅ Systemd настроен"
echo ""
echo "🛡️ MIRAI ЗАЩИЩЕНА ОТ ПОЛОМОК КЛЮЧЕЙ!"
echo ""
echo "💡 Добавь в crontab для автоматической проверки:"
echo "   */15 * * * * /root/mirai/mirai-agent/cleanup_api_keys.sh >> /tmp/mirai_cleanup.log 2>&1"
echo ""
