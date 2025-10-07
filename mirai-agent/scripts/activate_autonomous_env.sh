#!/bin/bash
# Activate environment variables and aliases for Mirai Agent on Linux VPS

PROJECT_ROOT=${PROJECT_ROOT:-/home/mirai/mirai-agent}
VENV_PATH=${VENV_PATH:-$PROJECT_ROOT/venv}

export VSCODE_SKIP_GETTING_STARTED=true
export VSCODE_SKIP_RELEASE_NOTES=true
export NODE_OPTIONS="--max-old-space-size=2048"
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export MIRAI_AUTONOMOUS_MODE=true
export MIRAI_AGENT_ROOT="$PROJECT_ROOT"
export MIRAI_VENV="$VENV_PATH"
export PYTHONPATH="$MIRAI_AGENT_ROOT:$MIRAI_AGENT_ROOT/modules:$PYTHONPATH"

mi-activate() {
  if [ -d "$MIRAI_VENV" ]; then
    # shellcheck disable=SC1090
    source "$MIRAI_VENV/bin/activate"
  else
    echo "venv not found at $MIRAI_VENV" >&2
  fi
}

mi-start() { cd "$MIRAI_AGENT_ROOT" && python3 core/master_agent.py "$@"; }
mi-api() { cd "$MIRAI_AGENT_ROOT" && uvicorn modules.api.mirai_api.main:app --host 0.0.0.0 --port 8000 "$@"; }
mi-web() { cd "$MIRAI_AGENT_ROOT" && uvicorn modules.api.web.api:app --host 0.0.0.0 --port 8080 "$@"; }
mi-shell() { cd "$MIRAI_AGENT_ROOT" && python3 -i core/master_agent.py; }
mi-status() { cd "$MIRAI_AGENT_ROOT" && git status && echo '---' && ps -eo pid,cmd | grep uvicorn; }

cat <<'INFO'
✅ Окружение Mirai Agent активировано. Доступные команды:
  mi-activate  – активировать виртуальное окружение
  mi-start     – запустить MasterAgent
  mi-api       – запустить основной API (FastAPI)
  mi-web       – веб-интерфейс (если нужен)
INFO
