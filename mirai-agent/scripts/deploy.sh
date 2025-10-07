#!/bin/bash
# Simple deployment script for Mirai Agent on Linux VPS
set -e

PROJECT_ROOT=${PROJECT_ROOT:-/home/mirai/mirai-agent}
VENV_PATH=${VENV_PATH:-$PROJECT_ROOT/venv}
SERVICE_NAMES=${SERVICE_NAMES:-"mirai-master mirai-api"}

cd "$PROJECT_ROOT"

echo "📥 Pulling latest changes..."
git pull --ff-only

echo "📦 Installing dependencies..."
if [ -d "$VENV_PATH" ]; then
  # shellcheck disable=SC1090
  source "$VENV_PATH/bin/activate"
  pip install -r requirements.txt
else
  pip3 install -r requirements.txt
fi

for svc in $SERVICE_NAMES; do
  if systemctl list-units --type=service | grep -q "$svc"; then
    echo "🔁 Restarting $svc"
    sudo systemctl restart "$svc"
  fi
done

echo "✅ Deployment complete."
