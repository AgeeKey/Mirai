#!/bin/bash
# MIRAI - Запуск режима самоулучшения

echo "🔧 MIRAI - РЕЖИМ САМОУЛУЧШЕНИЯ"
echo "================================"
echo ""
echo "Агент будет САМ решать свои проблемы:"
echo "  1. ✅ Валидация кода"
echo "  2. 📝 Улучшение логирования"
echo "  3. 📊 Система мониторинга"
echo "  4. 📚 Генерация документации"
echo "  5. 🧪 Создание автотестов"
echo "  6. 🔒 Улучшение безопасности"
echo "  7. ⚡ Добавление асинхронности"
echo "  8. 🔄 Настройка CI/CD"
echo ""
echo "================================"

cd /root/mirai/mirai-agent

# Активируем виртуальное окружение
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Ошибка: venv не найден"
    exit 1
fi

# Загружаем переменные окружения
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ Ошибка: .env не найден"
    exit 1
fi

echo "✅ Окружение настроено"
echo ""
echo "🚀 Запуск режима самоулучшения..."
echo "📝 Логи: /tmp/mirai_self_improvement.log"
echo ""
echo "⏰ Это займет примерно 4-5 минут"
echo "   (8 задач × 30 сек паузы)"
echo ""

# Запускаем режим самоулучшения
python3 self_improvement.py

echo ""
echo "================================"
echo "✅ Самоулучшение завершено!"
echo ""
echo "📄 Отчет: /root/mirai/mirai-agent/self_improvement_report.md"
echo "📝 Логи: /tmp/mirai_self_improvement.log"
echo ""
echo "🔍 Проверьте что создал агент:"
echo "   ls -la core/validation.py"
echo "   ls -la core/advanced_logger.py"
echo "   ls -la utils/monitoring.py"
echo "   ls -la tests/"
