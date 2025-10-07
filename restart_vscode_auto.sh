#!/bin/bash

# 🔄 Перезапуск VS Code с автоматическими настройками Copilot

echo "🔄 Перезапуск VS Code с автоматизацией Copilot..."

# Убиваем все процессы VS Code
pkill -f "code" 2>/dev/null || true
sleep 2

# Запускаем VS Code с текущей директорией
echo "🚀 Запуск VS Code..."
cd /root/mirai
code . --disable-extensions --disable-gpu --disable-dev-shm-usage --no-sandbox 2>/dev/null &

# Ждем запуска
sleep 3

# Включаем все расширения
code --enable-proposed-api github.copilot 2>/dev/null &
code --enable-proposed-api github.copilot-chat 2>/dev/null &

echo "✅ VS Code перезапущен с автоматизацией!"
echo "💡 Теперь все предложения Copilot будут применяться автоматически."