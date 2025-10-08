#!/usr/bin/env bash
# toggle_yolo.sh - Переключатель EXTREME / SAFE режимов для Copilot Auto / Chat Tools
# Использование:
#   ./scripts/toggle_yolo.sh on   # включить экстремальный режим
#   ./scripts/toggle_yolo.sh off  # откатить к безопасным настройкам
# Создает резервную копию настроек при первом запуске.
set -euo pipefail

WS_SETTINGS=".vscode/settings.json"
BACKUP=".vscode/settings.safe.backup.json"

if [[ ! -f "$WS_SETTINGS" ]]; then
  echo "[ERR] Workspace settings file not found: $WS_SETTINGS" >&2
  exit 1
fi

cmd=${1:-}
if [[ -z "$cmd" ]]; then
  echo "Usage: $0 <on|off>" >&2
  exit 1
fi

if [[ ! -f "$BACKUP" ]]; then
  cp "$WS_SETTINGS" "$BACKUP"
  echo "[INFO] Backup created at $BACKUP"
fi

if [[ "$cmd" == "on" ]]; then
  echo "[YOLO] Enabling MAX EXTREME mode"
  # Встраиваем или заменяем ключи
  # Используем jq если установлен, иначе грубая подстановка sed
  if command -v jq >/dev/null 2>&1; then
    tmp=$(mktemp)
    jq '. + {
      "copilotAutoAccept.enable": true,
      "copilotAutoAccept.strategy": "first",
      "copilotAutoAccept.idleMs": 25,
      "copilotAutoAccept.maxFileSizeKB": 4096,
      "copilotAutoAccept.excludePatterns": [],
      "copilotAutoAccept.smartGuards": false,
      "chat.tools.global.autoApprove": true,
      "chat.tools.autoApprove": true,
      "chat.experimental.agent.autoApprove": true,
      "chat.tools.terminal.autoApprove": {"/.*/": true},
      "chat.tools.edits.autoApprove": {"**/*": true}
    }' "$WS_SETTINGS" > "$tmp" && mv "$tmp" "$WS_SETTINGS"
  else
    echo "[WARN] jq not installed; performing raw append" >&2
    echo "// YOLO PATCH $(date)" >> "$WS_SETTINGS"
    {
      echo '"copilotAutoAccept.enable": true,'
      echo '"copilotAutoAccept.strategy": "first",'
      echo '"copilotAutoAccept.idleMs": 25,'
      echo '"copilotAutoAccept.maxFileSizeKB": 4096,'
      echo '"copilotAutoAccept.excludePatterns": [],'
      echo '"copilotAutoAccept.smartGuards": false,'
      echo '"chat.tools.global.autoApprove": true,'
      echo '"chat.tools.autoApprove": true,'
      echo '"chat.experimental.agent.autoApprove": true,'
      echo '"chat.tools.terminal.autoApprove": {"/.*/": true},'
      echo '"chat.tools.edits.autoApprove": {"**/*": true}'
    } >> "$WS_SETTINGS"
  fi
  echo "[YOLO] EXTREME mode applied"
elif [[ "$cmd" == "off" ]]; then
  echo "[SAFE] Restoring backup"
  if [[ -f "$BACKUP" ]]; then
    cp "$BACKUP" "$WS_SETTINGS"
    echo "[SAFE] Restored from $BACKUP"
  else
    echo "[WARN] No backup found. Manual cleanup required." >&2
  fi
else
  echo "Unknown argument: $cmd (expected on|off)" >&2
  exit 1
fi

# Короткий отчет
if command -v grep >/dev/null 2>&1; then
  echo "--- CURRENT FLAGS ---"
  grep -E 'copilotAutoAccept.strategy|copilotAutoAccept.idleMs|smartGuards|global.autoApprove|terminal.autoApprove' "$WS_SETTINGS" || true
  echo "---------------------"
fi

echo "Done."