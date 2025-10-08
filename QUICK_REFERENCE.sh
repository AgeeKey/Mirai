#!/bin/bash
# ═══════════════════════════════════════════════════════
# 🤖 MIRAI QUICK COMMANDS - ШПАРГАЛКА
# ═══════════════════════════════════════════════════════

cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║            🤖 MIRAI AUTONOMOUS AGENT - КОМАНДЫ                ║
╚═══════════════════════════════════════════════════════════════╝

📦 УПРАВЛЕНИЕ СЕРВИСОМ:
──────────────────────────────────────────────────────────────
  sudo systemctl start mirai-agent      # Запустить
  sudo systemctl stop mirai-agent       # Остановить
  sudo systemctl restart mirai-agent    # Перезапустить
  sudo systemctl status mirai-agent     # Статус
  sudo systemctl enable mirai-agent     # Автозапуск ВКЛ
  sudo systemctl disable mirai-agent    # Автозапуск ВЫКЛ

📊 ЛОГИ:
──────────────────────────────────────────────────────────────
  sudo journalctl -u mirai-agent -f                # Real-time
  sudo journalctl -u mirai-agent -n 100            # 100 строк
  sudo journalctl -u mirai-agent --since "1h ago" # За час
  tail -f /root/mirai/mirai-agent/data/logs/mirai_agent.log

🌐 API ТЕСТЫ:
──────────────────────────────────────────────────────────────
  curl http://localhost:8000/health     # Здоровье
  curl http://localhost:8000/status     # Статус
  curl http://localhost:8000/tasks      # Задачи
  curl http://localhost:8000/docs       # Swagger UI

  # Создать задачу:
  curl -X POST http://localhost:8000/task \
    -H "Content-Type: application/json" \
    -d '{"goal": "Analyze market trends"}'

🔍 ПРОВЕРКА РАБОТЫ:
──────────────────────────────────────────────────────────────
  # Процесс запущен?
  pgrep -f "python3.*main.py"
  
  # AI работает? (должны быть запросы к OpenAI)
  sudo journalctl -u mirai-agent | grep "chat/completions"
  
  # Задачи создаются?
  sudo journalctl -u mirai-agent | grep "Task created"
  
  # Telegram работает?
  sudo journalctl -u mirai-agent | grep "telegram.org"

📁 ВАЖНЫЕ ФАЙЛЫ:
──────────────────────────────────────────────────────────────
  /root/mirai/mirai-agent/.env                  # Конфигурация
  /root/mirai/mirai-agent/main.py               # Точка входа
  /root/mirai/mirai-agent/data/state/mirai.db   # База данных
  /root/mirai/mirai-agent/data/logs/            # Логи
  /etc/systemd/system/mirai-agent.service       # Systemd

💾 БАЗА ДАННЫХ:
──────────────────────────────────────────────────────────────
  sqlite3 /root/mirai/mirai-agent/data/state/mirai.db
  > SELECT * FROM memories LIMIT 10;
  > SELECT * FROM trading_decisions LIMIT 10;
  > .quit


  Команды бота:
    /start   - Приветствие
    /status  - Статус агента
    /tasks   - Активные задачи
    /stats   - Статистика
    /help    - Помощь

🔧 РЕДАКТИРОВАНИЕ:
──────────────────────────────────────────────────────────────
  nano /root/mirai/mirai-agent/.env             # Конфигурация
  sudo systemctl daemon-reload                  # После изменения .service
  sudo systemctl restart mirai-agent            # Применить изменения

🚀 РУЧНОЙ ЗАПУСК (для разработки):
──────────────────────────────────────────────────────────────
  cd /root/mirai/mirai-agent
  source venv/bin/activate
  python3 main.py

📊 МОНИТОРИНГ:
──────────────────────────────────────────────────────────────
  # CPU и память
  ps aux | grep python3
  
  # Сетевая активность
  sudo netstat -tulpn | grep 8000
  
  # Размер логов
  du -sh /root/mirai/mirai-agent/data/logs/

🔥 БЫСТРАЯ ДИАГНОСТИКА:
──────────────────────────────────────────────────────────────
  # Всё работает?
  sudo systemctl is-active mirai-agent && \
  curl -sf http://localhost:8000/health && \
  echo "✅ ВСЁ РАБОТАЕТ!" || echo "❌ ЕСТЬ ПРОБЛЕМЫ"

╔═══════════════════════════════════════════════════════════════╗
║  📖 Полная документация: /root/mirai/MIRAI_READY_REPORT.md   ║
╚═══════════════════════════════════════════════════════════════╝
EOF
