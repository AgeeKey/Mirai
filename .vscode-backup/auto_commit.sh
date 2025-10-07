#!/bin/bash
# Автоматический коммит изменений
if [ -n "$(git status --porcelain)" ]; then
    git add .
    git commit -m "🤖 Auto commit: $(date '+%Y-%m-%d %H:%M:%S')"
    git push 2>/dev/null || echo "Не удалось отправить изменения"
    echo "✅ Изменения автоматически сохранены"
else
    echo "📋 Нет изменений для коммита"
fi
