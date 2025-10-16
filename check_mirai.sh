#!/bin/bash
# Автоматическая проверка MIRAI после 30 минут работы

echo "🔍 ПРОВЕРКА MIRAI - РЕАЛЬНАЯ РАБОТА VS TODO"
echo "==========================================="
echo ""
echo "⏰ Время проверки: $(date)"
echo ""

# 1. Проверка статуса сервиса
echo "1️⃣ Статус сервиса:"
if systemctl is-active --quiet mirai; then
    echo "   ✅ РАБОТАЕТ"
    uptime_info=$(sudo systemctl status mirai --no-pager | grep 'Active:' | awk '{print $3, $4, $5}')
    echo "   ⏱️  Uptime: $uptime_info"
else
    echo "   ❌ НЕ РАБОТАЕТ!"
    exit 1
fi
echo ""

# 2. Подсчёт циклов
echo "2️⃣ Автономные циклы за 30 минут:"
cycles=$(sudo journalctl -u mirai --since "30 minutes ago" | grep "АВТОНОМНЫЙ ЦИКЛ" | wc -l)
echo "   📊 Выполнено: $cycles циклов"
if [ $cycles -ge 5 ]; then
    echo "   ✅ НОРМА (ожидалось ~6)"
else
    echo "   ⚠️  Меньше ожидаемого"
fi
echo ""

# 3. Проверка TODO
echo "3️⃣ TODO записи (должно быть 0!):"
todo_count=$(sudo journalctl -u mirai --since "30 minutes ago" | grep "TODO" | wc -l)
if [ $todo_count -eq 0 ]; then
    echo "   ✅ TODO: $todo_count - ОТЛИЧНО!"
else
    echo "   ❌ TODO: $todo_count - ПЛОХО!"
    echo "   Примеры:"
    sudo journalctl -u mirai --since "30 minutes ago" | grep "TODO" | head -3
fi
echo ""

# 4. Dashboard обновления
echo "4️⃣ Dashboard обновления:"
dashboard_updates=$(sudo journalctl -u mirai --since "30 minutes ago" | grep "Dashboard создан" | wc -l)
echo "   📊 Обновлений: $dashboard_updates"
if [ $dashboard_updates -ge 5 ]; then
    echo "   ✅ РАБОТАЕТ"
else
    echo "   ⚠️  Мало обновлений"
fi
echo ""

# 5. Метрики
echo "5️⃣ Метрики обновления:"
metrics_updates=$(sudo journalctl -u mirai --since "30 minutes ago" | grep "Метрики обновлены" | wc -l)
echo "   📊 Обновлений: $metrics_updates"

if [ -f /root/mirai/metrics/latest.json ]; then
    echo "   📄 Последняя метрика:"
    cat /root/mirai/metrics/latest.json | jq '.'
    
    timestamp=$(cat /root/mirai/metrics/latest.json | jq -r '.timestamp')
    echo "   ⏰ Timestamp: $timestamp"
else
    echo "   ❌ Файл метрик не найден!"
fi
echo ""

# 6. История метрик
echo "6️⃣ История метрик:"
if [ -f /root/mirai/metrics/history.jsonl ]; then
    history_lines=$(wc -l < /root/mirai/metrics/history.jsonl)
    echo "   📊 Строк в истории: $history_lines"
    if [ $history_lines -ge 5 ]; then
        echo "   ✅ РАСТЁТ"
    else
        echo "   ⚠️  Мало записей"
    fi
else
    echo "   ❌ Файл истории не найден!"
fi
echo ""

# 7. База знаний
echo "7️⃣ База знаний:"
if [ -f /root/mirai/knowledge_base/errors.json ]; then
    total_errors=$(cat /root/mirai/knowledge_base/errors.json | jq '.total_errors_analyzed')
    patterns=$(cat /root/mirai/knowledge_base/errors.json | jq '.error_patterns | length')
    echo "   📚 Всего ошибок: $total_errors"
    echo "   🔍 Паттернов: $patterns"
    echo "   ✅ ОБНОВЛЯЕТСЯ"
else
    echo "   ❌ Файл базы знаний не найден!"
fi
echo ""

# 8. Отчёты
echo "8️⃣ Отчёты:"
reports_count=$(ls -1 /root/mirai/reports/*.md 2>/dev/null | wc -l)
echo "   📝 Файлов отчётов: $reports_count"
if [ $reports_count -gt 0 ]; then
    echo "   ✅ СОЗДАЮТСЯ"
    ls -lh /root/mirai/reports/*.md | tail -3
else
    echo "   ⚠️  Отчёты не найдены"
fi
echo ""

# 9. Dashboard файл
echo "9️⃣ Dashboard:"
if [ -f /root/mirai/web/dashboard.html ]; then
    dashboard_size=$(stat -f%z /root/mirai/web/dashboard.html 2>/dev/null || stat -c%s /root/mirai/web/dashboard.html)
    dashboard_time=$(stat -f%Sm /root/mirai/web/dashboard.html 2>/dev/null || stat -c%y /root/mirai/web/dashboard.html)
    echo "   📄 Размер: $dashboard_size байт"
    echo "   ⏰ Обновлён: $dashboard_time"
    echo "   ✅ СУЩЕСТВУЕТ"
else
    echo "   ❌ Dashboard не найден!"
fi
echo ""

# 10. Последние логи
echo "🔟 Последние 5 важных событий:"
sudo journalctl -u mirai --since "5 minutes ago" | grep -E "(✅|❌|🔧|📊|📚)" | tail -5
echo ""

# ИТОГОВАЯ ОЦЕНКА
echo "==========================================="
echo "📊 ИТОГОВАЯ ОЦЕНКА:"
echo ""

score=0

# Проверки
[ $(systemctl is-active mirai) == "active" ] && ((score+=2)) && echo "✅ Сервис работает (+2)"
[ $cycles -ge 5 ] && ((score+=2)) && echo "✅ Достаточно циклов (+2)"
[ $todo_count -eq 0 ] && ((score+=3)) && echo "✅ Нет TODO записей (+3)" || echo "❌ Есть TODO записи (0)"
[ $dashboard_updates -ge 5 ] && ((score+=1)) && echo "✅ Dashboard обновляется (+1)"
[ $metrics_updates -ge 5 ] && ((score+=1)) && echo "✅ Метрики обновляются (+1)"
[ -f /root/mirai/web/dashboard.html ] && ((score+=1)) && echo "✅ Dashboard существует (+1)"

echo ""
echo "Финальный счёт: $score / 10"
echo ""

if [ $score -ge 8 ]; then
    echo "🎉 ОТЛИЧНО! MIRAI работает как надо!"
elif [ $score -ge 5 ]; then
    echo "⚠️  УДОВЛЕТВОРИТЕЛЬНО. Есть проблемы."
else
    echo "❌ ПЛОХО! Требуется исправление."
fi

echo "==========================================="
