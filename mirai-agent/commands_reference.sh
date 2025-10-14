#!/bin/bash
# 🚀 NASA-Level Integration - Command Reference

cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════╗
║  🚀 NASA-LEVEL INTEGRATION - COMMAND REFERENCE                      ║
╚══════════════════════════════════════════════════════════════════════╝

📋 БЫСТРЫЕ КОМАНДЫ:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧪 ТЕСТИРОВАНИЕ:

# Полный тест интеграции
cd /root/mirai/mirai-agent && python3 test_nasa_integration.py

# Тест базового обучения
cd /root/mirai/mirai-agent && python3 -c "
from core.nasa_level.orchestrator import NASALearningOrchestrator
nasa = NASALearningOrchestrator()
result = nasa.learn_technology('json', depth='basic')
print(f'Success: {result.success}, Proficiency: {result.proficiency}%')
"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 РУЧНОЙ ЗАПУСК:

# Autonomous Service (foreground)
cd /root/mirai/mirai-agent
source venv/bin/activate
python3 autonomous_service.py --interval 600

# Dashboard (в другом терминале)
cd /root/mirai/mirai-agent
source venv/bin/activate
python3 dashboard_server.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  SYSTEMD SERVICES:

# Установка
cd /root/mirai/mirai-agent
sudo ./install_nasa_services.sh

# Управление
sudo systemctl start nasa-learning
sudo systemctl stop nasa-learning
sudo systemctl restart nasa-learning
sudo systemctl status nasa-learning

sudo systemctl start nasa-dashboard
sudo systemctl stop nasa-dashboard
sudo systemctl restart nasa-dashboard
sudo systemctl status nasa-dashboard

# Автозапуск
sudo systemctl enable nasa-learning
sudo systemctl enable nasa-dashboard
sudo systemctl disable nasa-learning
sudo systemctl disable nasa-dashboard

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📜 ЛОГИ:

# Real-time логи
tail -f /tmp/kaizen_mirai.log

# Последние 100 строк
tail -100 /tmp/kaizen_mirai.log

# Поиск ошибок
grep -i error /tmp/kaizen_mirai.log

# Systemd журналы
sudo journalctl -u nasa-learning -f
sudo journalctl -u nasa-dashboard -f
sudo journalctl -u nasa-learning --since "1 hour ago"

# Метрики
tail -f /tmp/kaizen_mirai_metrics.jsonl
cat /tmp/kaizen_mirai_metrics.jsonl | jq .

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 API ENDPOINTS:

# Статус системы
curl http://localhost:5000/api/nasa/status | jq

# Метрики обучения
curl http://localhost:5000/api/nasa/metrics | jq

# Список технологий
curl http://localhost:5000/api/nasa/knowledge | jq

# Детали технологии
curl http://localhost:5000/api/nasa/knowledge/requests | jq

# Поиск
curl http://localhost:5000/api/nasa/search/HTTP | jq

# Полный отчёт
curl http://localhost:5000/api/nasa/report | jq

# Prometheus метрики
curl http://localhost:5000/api/nasa/prometheus

# CI/CD endpoints
curl http://localhost:5000/api/health | jq
curl http://localhost:5000/api/metrics | jq
curl http://localhost:5000/api/runs | jq

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 NASA LEARNING CLI:

# Изучить технологию
cd /root/mirai/mirai-agent
python3 core/nasa_level/orchestrator.py learn --tech numpy --depth basic

# Добавить в очередь
python3 core/nasa_level/orchestrator.py queue --tech pandas --priority high

# Статус системы
python3 core/nasa_level/orchestrator.py status

# Поиск в базе знаний
python3 core/nasa_level/orchestrator.py search --query "HTTP requests"

# Полный отчёт
python3 core/nasa_level/orchestrator.py report

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 МОНИТОРИНГ:

# Статус сервисов
systemctl is-active nasa-learning
systemctl is-active nasa-dashboard

# Использование ресурсов
ps aux | grep -E "(autonomous_service|dashboard_server)"
top -p $(pgrep -f autonomous_service)

# Размер логов
du -h /tmp/kaizen_mirai.log
du -h /tmp/kaizen_mirai_metrics.jsonl

# Статистика обучения
sqlite3 /root/mirai/mirai-agent/data/knowledge.db \
  "SELECT COUNT(*) as total, AVG(proficiency) as avg_prof 
   FROM knowledge;"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 ОТЛАДКА:

# Проверка портов
netstat -tulpn | grep 5000
lsof -i :5000

# Проверка процессов
pgrep -af autonomous_service
pgrep -af dashboard_server

# Убить процесс
pkill -f autonomous_service
pkill -f dashboard_server

# Очистка логов
> /tmp/kaizen_mirai.log
> /tmp/kaizen_mirai_metrics.jsonl

# Пересоздать базу данных
rm /root/mirai/mirai-agent/data/knowledge.db
# База создастся автоматически при следующем запуске

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 ДОКУМЕНТАЦИЯ:

# Просмотр документов
cat /root/mirai/FINAL_INTEGRATION_REPORT.txt
cat /root/mirai/INTEGRATION_SUMMARY.md
cat /root/mirai/NASA_INTEGRATION_COMPLETE.md
cat /root/mirai/NASA_ARCHITECTURE_DIAGRAM.txt

# Quick start
/root/mirai/quick_start_integration.sh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 ОДНОЙ СТРОКОЙ:

# Полный тест + логи
cd /root/mirai/mirai-agent && python3 test_nasa_integration.py && tail -20 /tmp/kaizen_mirai.log

# Запуск всего (systemd)
sudo ./install_nasa_services.sh && sleep 5 && sudo systemctl status nasa-learning nasa-dashboard

# Проверка API
for endpoint in status metrics knowledge report; do echo "=== $endpoint ==="; curl -s http://localhost:5000/api/nasa/$endpoint | jq -c; done

# Статистика
echo "Services:" && systemctl is-active nasa-{learning,dashboard} && echo "Logs:" && wc -l /tmp/kaizen_mirai.log && echo "Technologies:" && sqlite3 /root/mirai/mirai-agent/data/knowledge.db "SELECT COUNT(*) FROM knowledge;"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 ПОЛЕЗНЫЕ АЛИАСЫ (добавь в ~/.bashrc):

alias nasa-start='sudo systemctl start nasa-learning nasa-dashboard'
alias nasa-stop='sudo systemctl stop nasa-learning nasa-dashboard'
alias nasa-status='sudo systemctl status nasa-learning nasa-dashboard'
alias nasa-logs='tail -f /tmp/kaizen_mirai.log'
alias nasa-test='cd /root/mirai/mirai-agent && python3 test_nasa_integration.py'
alias nasa-api='curl -s http://localhost:5000/api/nasa/status | jq'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF
