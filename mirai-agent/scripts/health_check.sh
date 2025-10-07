#!/bin/bash
set -e

API_URL=${API_URL:-http://127.0.0.1:8000/health}
MASTER_SERVICE=${MASTER_SERVICE:-mirai-master}

status_ok=true

if systemctl list-units --type=service | grep -q "$MASTER_SERVICE"; then
  if ! systemctl is-active --quiet "$MASTER_SERVICE"; then
    echo "❌ Service $MASTER_SERVICE inactive"
    status_ok=false
  fi
fi

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL" || echo 000)
if [ "$HTTP_CODE" != "200" ]; then
  echo "❌ API health check failed (status $HTTP_CODE)"
  status_ok=false
else
  echo "✅ API health check passed"
fi

if [ "$status_ok" = true ]; then
  echo "✅ Mirai Agent healthy"
  exit 0
else
  echo "⚠️ Issues detected"
  exit 1
fi
