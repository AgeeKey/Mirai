#!/usr/bin/env bash
set -euo pipefail

HOST="${1:-127.0.0.1}"
PORT="${2:-8000}"

BASE="http://$HOST:$PORT"

echo "[*] Health check: $BASE/health"
if command -v curl >/dev/null 2>&1; then
  curl -fsS "$BASE/health" | sed 's/.*/[OK] &/'
elif command -v wget >/dev/null 2>&1; then
  wget -qO- "$BASE/health" | sed 's/.*/[OK] &/'
else
  echo "[!] Neither curl nor wget is available" >&2
  exit 1
fi

echo "[*] Root check: $BASE/"
if command -v curl >/dev/null 2>&1; then
  curl -fsS "$BASE/" | sed 's/.*/[OK] &/'
else
  wget -qO- "$BASE/" | sed 's/.*/[OK] &/'
fi

echo "[*] Smoke OK"

