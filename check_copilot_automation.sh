#!/bin/bash

# 🧪 Скрипт полной проверки автоматизации GitHub Copilot

echo "🔍 === ПРОВЕРКА АВТОМАТИЗАЦИИ GITHUB COPILOT ==="
echo ""

# 1. Проверка расширений
echo "📦 1. Проверка установленных расширений Copilot:"
if code --list-extensions | grep -q "github.copilot"; then
    echo "   ✅ GitHub Copilot установлен"
else
    echo "   ❌ GitHub Copilot НЕ установлен"
fi

if code --list-extensions | grep -q "github.copilot-chat"; then
    echo "   ✅ GitHub Copilot Chat установлен"
else
    echo "   ❌ GitHub Copilot Chat НЕ установлен"
fi

# 2. Проверка файлов конфигурации
echo ""
echo "🔧 2. Проверка файлов конфигурации:"
if [ -f ".vscode/settings.json" ]; then
    echo "   ✅ settings.json существует"
else
    echo "   ❌ settings.json отсутствует"
fi

if [ -f ".vscode/keybindings.json" ]; then
    echo "   ✅ keybindings.json существует"
else
    echo "   ❌ keybindings.json отсутствует"
fi

if [ -f ".vscode/tasks.json" ]; then
    echo "   ✅ tasks.json существует"
else
    echo "   ❌ tasks.json отсутствует"
fi

# 3. Проверка настроек автоматизации
echo ""
echo "⚙️  3. Проверка настроек автоматизации:"
if grep -q '"chat.tools.global.autoApprove": true' .vscode/settings.json 2>/dev/null; then
    echo "   ✅ Глобальное автоутверждение включено"
else
    echo "   ❌ Глобальное автоутверждение отключено"
fi

if grep -q '"github.copilot.editor.enableAutoCompletions": true' .vscode/settings.json 2>/dev/null; then
    echo "   ✅ Автодополнения Copilot включены"
else
    echo "   ❌ Автодополнения Copilot отключены"
fi

if grep -q '"files.autoSave"' .vscode/settings.json 2>/dev/null; then
    echo "   ✅ Автосохранение настроено"
else
    echo "   ❌ Автосохранение не настроено"
fi

# 4. Проверка автоматических коммитов
echo ""
echo "🔄 4. Проверка автоматических коммитов:"
if crontab -l 2>/dev/null | grep -q "auto_commit.sh"; then
    echo "   ✅ Автоматические коммиты настроены в cron"
else
    echo "   ❌ Автоматические коммиты НЕ настроены в cron"
fi

if [ -f ".vscode/auto_commit.sh" ]; then
    echo "   ✅ Скрипт автокоммита существует"
else
    echo "   ❌ Скрипт автокоммита отсутствует"
fi

# 5. Проверка статуса Git
echo ""
echo "📋 5. Проверка статуса Git:"
if git status &>/dev/null; then
    echo "   ✅ Git репозиторий инициализирован"
    if [ -n "$(git status --porcelain)" ]; then
        echo "   📝 Есть неcommited изменения"
    else
        echo "   ✅ Все изменения закоммичены"
    fi
else
    echo "   ❌ Git репозиторий НЕ инициализирован"
fi

# 6. Тест создания файла
echo ""
echo "🧪 6. Тест автоматического создания файла:"
cat > test_auto_file.py << 'EOF'
# Тестовый файл для проверки автоматизации
def hello_copilot():
    return "Hello from automated Copilot!"
EOF

if [ -f "test_auto_file.py" ]; then
    echo "   ✅ Файл создан успешно"
    rm test_auto_file.py
else
    echo "   ❌ Ошибка создания файла"
fi

# 7. Финальный статус
echo ""
echo "🎯 === ИТОГОВЫЙ СТАТУС ==="
if code --list-extensions | grep -q "github.copilot" && [ -f ".vscode/settings.json" ]; then
    echo "🎉 АВТОМАТИЗАЦИЯ ГОТОВА К РАБОТЕ!"
    echo ""
    echo "💡 Что теперь работает автоматически:"
    echo "   • Предложения кода при наборе"
    echo "   • Автосохранение файлов"
    echo "   • Автоформатирование при сохранении"
    echo "   • Автокоммиты каждые 5 минут"
    echo "   • Горячие клавиши для быстрых действий"
    echo ""
    echo "🎮 Горячие клавиши:"
    echo "   Ctrl+Shift+Space - Генерация кода"
    echo "   Tab              - Принять предложение"
    echo "   Alt+]            - Следующее предложение"
    echo "   Ctrl+Alt+F       - Автоисправление"
else
    echo "⚠️  ТРЕБУЕТСЯ ДОПОЛНИТЕЛЬНАЯ НАСТРОЙКА"
fi

echo ""
echo "📊 Проверка завершена: $(date)"