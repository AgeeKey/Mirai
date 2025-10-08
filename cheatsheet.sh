#!/bin/bash

# 🚀 Mirai AI - Шпаргалка Команд
# Все команды для быстрого управления

cat << 'EOF'

╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║              🤖 Mirai AI - Шпаргалка Команд                   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

📦 БЫСТРЫЙ ЗАПУСК:
═══════════════════════════════════════════════════════════════

  /root/mirai/start_mirai.sh
  
  ↑ Запускает всё автоматически!

═══════════════════════════════════════════════════════════════

🎮 УПРАВЛЕНИЕ СЕРВИСОМ:
═══════════════════════════════════════════════════════════════

  Запуск:         sudo systemctl start mirai-agent
  Остановка:      sudo systemctl stop mirai-agent
  Перезапуск:     sudo systemctl restart mirai-agent
  Статус:         sudo systemctl status mirai-agent
  
  Автозапуск:     sudo systemctl enable mirai-agent
  Отключить авто: sudo systemctl disable mirai-agent

═══════════════════════════════════════════════════════════════

📜 ПРОСМОТР ЛОГОВ:
═══════════════════════════════════════════════════════════════

  Live логи:         sudo journalctl -u mirai-agent -f
  Последние 50:      sudo journalctl -u mirai-agent -n 50
  За последний час:  sudo journalctl -u mirai-agent --since "1 hour ago"
  Только ошибки:     sudo journalctl -u mirai-agent -p err
  Сегодня:           sudo journalctl -u mirai-agent --since today

═══════════════════════════════════════════════════════════════

🌐 ВЕБ-ИНТЕРФЕЙС:
═══════════════════════════════════════════════════════════════

  Браузер:          http://localhost:8000/
  Health Check:     curl http://localhost:8000/health
  Статистика:       curl http://localhost:8000/stats
  Status:           curl http://localhost:8000/status

═══════════════════════════════════════════════════════════════

💬 TELEGRAM БОТ:
═══════════════════════════════════════════════════════════════

  /start    - Приветствие
  /status   - Статус агента
  /help     - Помощь
  /tasks    - Активные задачи
  /stats    - Статистика

═══════════════════════════════════════════════════════════════

🔧 НАСТРОЙКА:
═══════════════════════════════════════════════════════════════

  Редактировать .env:       nano /root/mirai/mirai-agent/.env
  Просмотр ключей:          grep API /root/mirai/mirai-agent/.env
  Проверка конфига:         cat /root/mirai/mirai-agent/.env
  Systemd сервис:           nano /etc/systemd/system/mirai-agent.service
  Nginx конфиг:             nano /etc/nginx/sites-available/mirai

═══════════════════════════════════════════════════════════════

🔍 ДИАГНОСТИКА:
═══════════════════════════════════════════════════════════════

  Быстрая проверка:     /root/mirai/quick_check.sh
  
  Проверка API:         curl http://localhost:8000/health
  Проверка процесса:    ps aux | grep "python3.*main.py"
  Проверка портов:      netstat -tlnp | grep 8000
  Проверка базы:        ls -lh /root/mirai/mirai-agent/data/state/mirai.db
  Проверка ключей:      grep -E "OPENAI|TELEGRAM" /root/mirai/mirai-agent/.env | sed 's/=.*/=***/'

═══════════════════════════════════════════════════════════════

🛠️ ОБСЛУЖИВАНИЕ:
═══════════════════════════════════════════════════════════════

  Перезагрузка systemd:     sudo systemctl daemon-reload
  Проверка nginx:           sudo nginx -t
  Перезапуск nginx:         sudo systemctl restart nginx
  Очистка логов:            sudo journalctl --vacuum-time=7d
  
  Backup:
    cd /root/mirai/mirai-agent
    tar -czf mirai_backup_$(date +%Y%m%d).tar.gz .env data/state/mirai.db

  Восстановление:
    tar -xzf mirai_backup_YYYYMMDD.tar.gz

═══════════════════════════════════════════════════════════════

📊 МОНИТОРИНГ:
═══════════════════════════════════════════════════════════════

  Статистика API:
    curl -s http://localhost:8000/stats | python3 -m json.tool
  
  Здоровье системы:
    curl -s http://localhost:8000/health | python3 -m json.tool
  
  Количество задач:
    curl -s http://localhost:8000/stats | grep -o '"tasks_completed":[0-9]*'
  
  Использование памяти:
    ps aux | grep "python3.*main.py" | awk '{print $6/1024 " MB"}'
  
  Размер базы данных:
    ls -lh /root/mirai/mirai-agent/data/state/mirai.db

═══════════════════════════════════════════════════════════════

🚨 РЕШЕНИЕ ПРОБЛЕМ:
═══════════════════════════════════════════════════════════════

  Сервис не запускается:
    sudo journalctl -u mirai-agent -n 50
    sudo systemctl restart mirai-agent
  
  API не отвечает:
    sudo netstat -tlnp | grep 8000
    sudo systemctl status mirai-agent
  
  Telegram не отвечает:
    sudo journalctl -u mirai-agent | grep Telegram | tail -20
    grep TELEGRAM /root/mirai/mirai-agent/.env
  
  Высокое использование памяти:
    sudo systemctl restart mirai-agent
  
  База данных заблокирована:
    sudo systemctl stop mirai-agent
    rm -f /root/mirai/mirai-agent/data/state/mirai.db-shm
    rm -f /root/mirai/mirai-agent/data/state/mirai.db-wal
    sudo systemctl start mirai-agent

═══════════════════════════════════════════════════════════════

📖 ДОКУМЕНТАЦИЯ:
═══════════════════════════════════════════════════════════════

  Полная инструкция:    /root/mirai/QUICK_START.md
  Веб-интерфейс:        /root/mirai/WEB_ACCESS_GUIDE.md
  AI возможности:       /root/mirai/WEB_AND_AI_TOOLS.md
  Эта шпаргалка:        /root/mirai/cheatsheet.sh

═══════════════════════════════════════════════════════════════

🎯 ПОЛЕЗНЫЕ ОДНО-СТРОЧНИКИ:
═══════════════════════════════════════════════════════════════

  # Полная проверка системы
  systemctl is-active mirai-agent && curl -s http://localhost:8000/health && echo "✅ Всё работает!"
  
  # Количество выполненных задач
  curl -s http://localhost:8000/stats | grep -o '"tasks_completed":[0-9]*' | cut -d: -f2
  
  # Последние 5 ошибок
  sudo journalctl -u mirai-agent -p err -n 5
  
  # Перезапуск всего
  sudo systemctl restart mirai-agent nginx
  
  # Статус всех сервисов
  systemctl status mirai-agent nginx --no-pager | grep Active

═══════════════════════════════════════════════════════════════

🚀 БЫСТРЫЕ ДЕЙСТВИЯ:
═══════════════════════════════════════════════════════════════

  1. Запустить всё:
     /root/mirai/start_mirai.sh
  
  2. Проверить работу:
     curl http://localhost:8000/health
  
  3. Посмотреть что делает:
     sudo journalctl -u mirai-agent -f
  
  4. Открыть веб:
     http://localhost:8000/
  
  5. Проверить Telegram:
     Отправь боту: /status

═══════════════════════════════════════════════════════════════

✅ ИТОГОВАЯ ПРОВЕРКА (копируй и выполни):
═══════════════════════════════════════════════════════════════

echo "🔍 Статус Mirai:" && \
systemctl is-active mirai-agent && \
echo "🌐 API:" && \
curl -s http://localhost:8000/health && \
echo "" && echo "📊 Статистика:" && \
curl -s http://localhost:8000/stats | python3 -m json.tool && \
echo "" && echo "✅ Всё работает отлично!"

═══════════════════════════════════════════════════════════════

🎉 Готово! Mirai AI - Полностью Автономный AI Агент!

EOF
