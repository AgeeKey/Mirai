#!/bin/bash
set -e

PROJECT_ROOT=${PROJECT_ROOT:-/home/mirai/mirai-agent}
VENV_PATH=${VENV_PATH:-$PROJECT_ROOT/venv}

cat <<'INFO'
🚀 Настраиваю автономные алиасы и окружение для Mirai Agent (Linux VPS).
INFO

if [ ! -d "$PROJECT_ROOT" ]; then
  echo "\n❌ Каталог проекта $PROJECT_ROOT не найден. Установите PROJECT_ROOT и повторите." >&2
  exit 1
fi

touch ~/.bashrc

cat >> ~/.bashrc <<'BRC'
# === Mirai Agent Autonomous Environment ===
export MIRAI_AGENT_ROOT="$PROJECT_ROOT"
export MIRAI_VENV="$VENV_PATH"
export PYTHONPATH="\$MIRAI_AGENT_ROOT:\$MIRAI_AGENT_ROOT/modules:\$PYTHONPATH"

mi-activate() {
  if [ -d "\$MIRAI_VENV" ]; then
    # shellcheck disable=SC1090
    source "\$MIRAI_VENV/bin/activate"
  else
    echo "venv not found at \$MIRAI_VENV" >&2
  fi
}

alias mi-cd="cd \$MIRAI_AGENT_ROOT"
alias mi-start="cd \$MIRAI_AGENT_ROOT && python3 core/master_agent.py"
alias mi-api="cd \$MIRAI_AGENT_ROOT && uvicorn modules.api.mirai_api.main:app --host 0.0.0.0 --port 8000"
alias mi-web="cd \$MIRAI_AGENT_ROOT && uvicorn modules.api.web.api:app --host 0.0.0.0 --port 8080"
alias mi-shell="cd \$MIRAI_AGENT_ROOT && python3 -i core/master_agent.py"
BRC

cat <<'INFO'
✅ Алиасы и переменные окружения добавлены в ~/.bashrc.
Перезапустите shell или выполните `source ~/.bashrc`.
INFO
