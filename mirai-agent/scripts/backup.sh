#!/bin/bash
set -e

PROJECT_ROOT=${PROJECT_ROOT:-/home/mirai/mirai-agent}
BACKUP_DIR=${BACKUP_DIR:-$PROJECT_ROOT/data/backups}
STATE_DB=${STATE_DB:-$PROJECT_ROOT/data/state/mirai.db}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Archive code (excluding heavy directories)
tar --exclude='venv' --exclude='data/backups' --exclude='.git' \
    -czf "$BACKUP_DIR/code_$TIMESTAMP.tar.gz" -C "$PROJECT_ROOT" .

if [ -f "$STATE_DB" ]; then
  sqlite3 "$STATE_DB" ".backup '$BACKUP_DIR/mirai_$TIMESTAMP.db'"
fi

echo "✅ Бэкап завершён: $BACKUP_DIR"
