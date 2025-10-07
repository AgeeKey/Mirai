#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-http://localhost:8000}

echo "[SMOKE] Safe flags: DRY_RUN=${DRY_RUN:-unset} ENABLE_BINANCE=${ENABLE_BINANCE:-unset} ENABLE_TELEGRAM=${ENABLE_TELEGRAM:-unset}"

pass=true

req() {
  local method=$1; shift
  local url=$1; shift
  curl -s -X "$method" "$url" "$@"
}

check_200() {
  local method=$1; shift
  local url=$1; shift
  local code
  code=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "$url" "$@")
  [[ "$code" == "200" ]]
}

echo "[1] LLM ping: OpenAI"
if check_200 POST "$BASE_URL/ai/ask" -H 'Content-Type: application/json' -d '{"provider":"openai","prompt":"Say \"pong\" in one word.","system":"test"}'; then
  ans=$(req POST "$BASE_URL/ai/ask" -H 'Content-Type: application/json' -d '{"provider":"openai","prompt":"Say \"pong\" in one word.","system":"test"}' | jq -r '.answer // empty')
  echo "    -> ${ans:-no-answer}"
else
  echo "    ERROR: OpenAI ask failed"; pass=false
fi

echo "[1] LLM ping: Grok"
if check_200 POST "$BASE_URL/ai/ask" -H 'Content-Type: application/json' -d '{"provider":"grok","prompt":"Say \"pong\" in one word.","system":"test"}'; then
  ans=$(req POST "$BASE_URL/ai/ask" -H 'Content-Type: application/json' -d '{"provider":"grok","prompt":"Say \"pong\" in one word.","system":"test"}' | jq -r '.answer // empty')
  echo "    -> ${ans:-no-answer}"
else
  echo "    WARN: Grok ask failed"; pass=false
fi

echo "[2] Health & Stats"
req GET "$BASE_URL/health" | jq '.' || { echo "    ERROR: health"; pass=false; }
req GET "$BASE_URL/stats" | jq '.' || echo "    note: /stats not found"
req GET "$BASE_URL/agent/stats" | jq '.' || { echo "    ERROR: /agent/stats"; pass=false; }
req GET "$BASE_URL/trader/stats" | jq '.' || { echo "    ERROR: /trader/stats"; pass=false; }

echo "[3] Create task"
req POST "$BASE_URL/agent/tasks" -H 'Content-Type: application/json' -d '{"title":"Audit project structure","priority":"high","meta":{"scope":"repo"}}' | jq '.'
echo "    List tasks"
req GET "$BASE_URL/agent/tasks" | jq '.'

echo "[4] Memory store/read"
req POST "$BASE_URL/agent/memory" -H 'Content-Type: application/json' -d '{"type":"note","text":"Mirai knows that DRY_RUN is enabled during tests."}' | jq '.'
req GET "$BASE_URL/agent/memory?limit=5" | jq '.'

echo "[5] Trader decide (dry-run)"
req POST "$BASE_URL/trader/decide" -H 'Content-Type: application/json' -d '{"symbol":"BTCUSDT","budget":25,"leverage":10,"dry_run":true}' | jq '.'

echo "\n[RESULT] $( $pass && echo PASS || echo FAIL )"

