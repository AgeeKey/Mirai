#!/usr/bin/env bash
set -euo pipefail

SERVICE=mirai-agent
API="http://127.0.0.1:8000"
DB="/root/mirai/mirai-agent/data/state/mirai.db"
LOGUNIT="mirai-agent"

divider() { printf "\n%s\n" "════════════════════════════════════════════════════════════"; }
section() { printf "\n🔍 %s\n" "$1"; printf "%s\n" "────────────────────────────────────────────────────────"; }

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     🤖 MIRAI FULL DIAGNOSTICS - $(date -u +"%Y-%m-%d %H:%M:%S UTC")     ║"
echo "╚════════════════════════════════════════════════════════════╝"

# ═══════════════════════════════════════════════════════════
section "1️⃣  24/7 АВТОНОМНОСТЬ"
# ═══════════════════════════════════════════════════════════

echo "📦 Systemd статус:"
systemctl is-enabled "$SERVICE" 2>/dev/null && echo "  ✅ Enabled (автозапуск)" || echo "  ❌ Disabled"
systemctl is-active  "$SERVICE" 2>/dev/null && echo "  ✅ Active (работает)" || echo "  ❌ Inactive"

echo ""
echo "🔄 Restart настройки:"
systemctl show "$SERVICE" -p Restart -p RestartSec 2>/dev/null || echo "  ❌ Service not found"

# ═══════════════════════════════════════════════════════════
section "2️⃣  AI РЕАЛЬНО РАБОТАЕТ (OpenAI/Grok)"
# ═══════════════════════════════════════════════════════════

echo "🧠 LLM запросы за последнюю минуту:"
LLM_COUNT=$(journalctl -u "$LOGUNIT" --since "1 min ago" 2>/dev/null | \
  grep -E "api\.openai\.com|api\.x\.ai|/api/generate" | wc -l || echo 0)

if [ "$LLM_COUNT" -gt 0 ]; then
  echo "  ✅ $LLM_COUNT запросов к AI (работает!)"
  journalctl -u "$LOGUNIT" --since "1 min ago" 2>/dev/null | \
    grep -E "api\.openai\.com|api\.x\.ai" | tail -3
else
  echo "  ⚠️  0 запросов за последнюю минуту"
  echo "  Проверяю за 5 минут..."
  LLM_COUNT_5=$(journalctl -u "$LOGUNIT" --since "5 min ago" 2>/dev/null | \
    grep -E "api\.openai\.com|api\.x\.ai" | wc -l || echo 0)
  echo "  📊 За 5 минут: $LLM_COUNT_5 запросов"
fi

# ═══════════════════════════════════════════════════════════
section "3️⃣  API СЕРВЕР"
# ═══════════════════════════════════════════════════════════

echo "🌐 Проверка эндпоинтов:"

check_endpoint() {
  local endpoint="$1"
  if curl -sf "$API$endpoint" > /dev/null 2>&1; then
    echo "  ✅ $endpoint"
  else
    echo "  ❌ $endpoint"
  fi
}

check_endpoint "/health"
check_endpoint "/status"
check_endpoint "/tasks"

echo ""
echo "📊 Данные /health:"
curl -s "$API/health" 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "  ❌ Не доступен"

# ═══════════════════════════════════════════════════════════
section "4️⃣  АВТОНОМНЫЕ ЗАДАЧИ"
# ═══════════════════════════════════════════════════════════

echo "📝 Статистика задач за последние 5 минут:"

CREATED=$(journalctl -u "$LOGUNIT" --since "5 min ago" 2>/dev/null | grep -c "Task created" || echo 0)
COMPLETED=$(journalctl -u "$LOGUNIT" --since "5 min ago" 2>/dev/null | grep -c "Task completed" || echo 0)

echo "  Создано:    $CREATED"
echo "  Выполнено:  $COMPLETED"

if [ "$CREATED" -gt 0 ] && [ "$COMPLETED" -gt 0 ]; then
  echo "  ✅ Агент активно работает с задачами!"
else
  echo "  ⚠️  Низкая активность задач"
fi

echo ""
echo "🎯 Последние созданные задачи:"
journalctl -u "$LOGUNIT" --since "10 min ago" 2>/dev/null | \
  grep "Task created" | tail -3 | sed 's/^/  /'

# ═══════════════════════════════════════════════════════════
section "5️⃣  TELEGRAM БОТ"
# ═══════════════════════════════════════════════════════════

echo "📱 Telegram активность за последнюю минуту:"

TG_GET=$(journalctl -u "$LOGUNIT" --since "1 min ago" 2>/dev/null | grep -c "api.telegram.org.*getUpdates" || echo 0)
TG_SEND=$(journalctl -u "$LOGUNIT" --since "5 min ago" 2>/dev/null | grep -c "sendMessage" || echo 0)

echo "  getUpdates:  $TG_GET запросов (polling)"
echo "  sendMessage: $TG_SEND сообщений (ответы)"

if [ "$TG_GET" -gt 0 ]; then
  echo "  ✅ Бот активно слушает Telegram"
else
  echo "  ❌ Бот не опрашивает Telegram"
fi

# ═══════════════════════════════════════════════════════════
section "6️⃣  БАЗА ДАННЫХ"
# ═══════════════════════════════════════════════════════════

if [ -f "$DB" ]; then
  echo "💾 База данных найдена: $DB"
  echo "  Размер: $(du -h "$DB" | cut -f1)"
  
  echo ""
  echo "📊 Таблицы в БД:"
  sqlite3 "$DB" "SELECT name FROM sqlite_master WHERE type='table';" 2>/dev/null | sed 's/^/  /'
  
  echo ""
  echo "🧠 Последние 3 записи памяти:"
  sqlite3 "$DB" "SELECT id, type, substr(content,1,50) as content, timestamp FROM memories ORDER BY id DESC LIMIT 3;" 2>/dev/null | sed 's/^/  /' || echo "  (таблица пуста или не существует)"
  
  echo ""
  echo "📋 Последние 3 торговых решения:"
  sqlite3 "$DB" "SELECT id, symbol, action, substr(reasoning,1,40) as reasoning FROM trading_decisions ORDER BY id DESC LIMIT 3;" 2>/dev/null | sed 's/^/  /' || echo "  (таблица пуста или не существует)"
else
  echo "❌ База данных НЕ найдена: $DB"
fi

# ═══════════════════════════════════════════════════════════
section "7️⃣  ЛОГИ"
# ═══════════════════════════════════════════════════════════

echo "📝 Размер логов:"
if [ -d "/root/mirai/mirai-agent/data/logs" ]; then
  du -sh /root/mirai/mirai-agent/data/logs 2>/dev/null || echo "  ❌ Директория недоступна"
  echo ""
  echo "📁 Файлы логов:"
  ls -lh /root/mirai/mirai-agent/data/logs/*.log 2>/dev/null | awk '{print "  " $9 " - " $5}' || echo "  (нет файлов)"
else
  echo "  ❌ Директория логов не найдена"
fi

# ═══════════════════════════════════════════════════════════
section "8️⃣  ОШИБКИ"
# ═══════════════════════════════════════════════════════════

echo "❌ Ошибки за последние 5 минут:"
ERROR_COUNT=$(journalctl -u "$LOGUNIT" --since "5 min ago" 2>/dev/null | grep -i "error" | grep -v "error.log" | wc -l || echo 0)

echo "  Всего ошибок: $ERROR_COUNT"

if [ "$ERROR_COUNT" -gt 0 ]; then
  echo ""
  echo "  Последние 5 ошибок:"
  journalctl -u "$LOGUNIT" --since "5 min ago" 2>/dev/null | \
    grep -i "error" | grep -v "error.log" | tail -5 | sed 's/^/  /'
else
  echo "  ✅ Ошибок не обнаружено"
fi

# ═══════════════════════════════════════════════════════════
section "9️⃣  РЕСУРСЫ"
# ═══════════════════════════════════════════════════════════

echo "💻 Использование ресурсов:"

PID=$(pgrep -f 'python3.*main.py' 2>/dev/null || true)
if [ -n "$PID" ]; then
  echo "  ✅ Процесс найден (PID: $PID)"
  echo ""
  ps -p "$PID" -o pid,etime,rss,pmem,pcpu,cmd 2>/dev/null | sed 's/^/  /'
else
  echo "  ❌ Процесс Mirai не найден"
fi

# ═══════════════════════════════════════════════════════════
section "🔟 ИТОГОВАЯ ОЦЕНКА"
# ═══════════════════════════════════════════════════════════

SCORE=0
MAX_SCORE=10

# Подсчёт баллов
systemctl is-active "$SERVICE" >/dev/null 2>&1 && ((SCORE++)) || true
systemctl is-enabled "$SERVICE" >/dev/null 2>&1 && ((SCORE++)) || true
[ "$LLM_COUNT" -gt 0 ] || [ "$LLM_COUNT_5" -gt 0 ] && ((SCORE++)) || true
curl -sf "$API/health" >/dev/null 2>&1 && ((SCORE++)) || true
[ "$CREATED" -gt 0 ] && ((SCORE++)) || true
[ "$COMPLETED" -gt 0 ] && ((SCORE++)) || true
[ "$TG_GET" -gt 0 ] && ((SCORE++)) || true
[ -f "$DB" ] && ((SCORE++)) || true
[ "$ERROR_COUNT" -eq 0 ] && ((SCORE++)) || true
[ -n "$PID" ] && ((SCORE++)) || true

echo ""
echo "📊 Оценка работоспособности: $SCORE/$MAX_SCORE"
echo ""

if [ "$SCORE" -ge 9 ]; then
  echo "🟢 ✅ ОТЛИЧНО! Mirai работает полностью автономно!"
elif [ "$SCORE" -ge 7 ]; then
  echo "🟡 ⚠️  ХОРОШО. Есть небольшие проблемы."
elif [ "$SCORE" -ge 5 ]; then
  echo "🟠 ⚠️  УДОВЛЕТВОРИТЕЛЬНО. Требуется внимание."
else
  echo "🔴 ❌ КРИТИЧНО! Много проблем, требуется исправление."
fi

divider
echo ""
echo "💡 Для детальной проверки выполни:"
echo "   sudo journalctl -u mirai-agent -f          # Real-time логи"
echo "   curl http://localhost:8000/health          # Проверка API"
echo "   curl http://localhost:8000/status          # Статус агента"
echo ""
echo "📖 Документация: /root/mirai/MIRAI_READY_REPORT.md"
echo ""
