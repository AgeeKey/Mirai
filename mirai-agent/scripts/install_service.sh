#!/usr/bin/env bash
set -euo pipefail

# Install and enable systemd unit for Mirai Master Agent

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_SRC="$ROOT_DIR/services/mirai-agent.service"
SERVICE_DST="/etc/systemd/system/mirai-agent.service"
ENV_FILE="$ROOT_DIR/.env"
VENV_PY="$ROOT_DIR/venv/bin/python"

if [[ ! -x "$VENV_PY" ]]; then
  echo "[!] Python venv not found at $VENV_PY" >&2
  echo "    Create it first: cd $ROOT_DIR && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt" >&2
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "[!] Env file not found at $ENV_FILE" >&2
  echo "    Copy template: cp $ROOT_DIR/.env.template $ENV_FILE and fill your secrets." >&2
  exit 1
fi

echo "[*] Installing systemd unit to $SERVICE_DST"
sudo mkdir -p /etc/systemd/system
sudo bash -c "sed -e 's|__WORKDIR__|$ROOT_DIR|g' -e 's|__PYTHON__|$VENV_PY|g' -e 's|__ENVFILE__|$ENV_FILE|g' \"$SERVICE_SRC\" > \"$SERVICE_DST\""

echo "[*] Reloading systemd daemon"
sudo systemctl daemon-reload

echo "[*] Enabling and starting mirai-agent.service"
sudo systemctl enable --now mirai-agent.service

echo "[*] Checking status"
sudo systemctl --no-pager --full status mirai-agent.service || true

echo "[*] Tail logs (Ctrl-C to exit)"
sudo journalctl -u mirai-agent.service -f -n 50

