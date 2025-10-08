# 🚀 Mirai AI - Полная Инструкция Запуска

## 📋 Что Нужно Перед Запуском

### Требования:
- ✅ Ubuntu 24.04 (или выше)
- ✅ Python 3.12
- ✅ Доступ к интернету
- ✅ Root доступ (или sudo)

### API Ключи (обязательно):
- ✅ **OpenAI API Key** - для GPT-4
- ✅ **Telegram Bot Token** - для Telegram бота
- ✅ **Telegram Chat ID** - твой Telegram ID

---

## 🔑 Шаг 1: Получение API Ключей

### 1.1 OpenAI API Key

1. Зайди на https://platform.openai.com/api-keys
2. Залогинься или зарегистрируйся
3. Нажми "Create new secret key"
4. Скопируй ключ (начинается с `sk-proj-...`)
5. Сохрани его (больше не покажут!)

**Пример:** `sk-proj-UD4dZOKyjJokICg3JBYN1aO1ETQ6ugFKu...`

### 1.2 Telegram Bot Token

1. Открой Telegram
2. Найди бота **@BotFather**
3. Отправь команду `/newbot`
4. Следуй инструкциям:
   - Введи имя бота (например: `Mirai AI Bot`)
   - Введи username (например: `mirai_ai_bot`)
5. Получишь токен (начинается с цифр)

**Пример:** `8104619923:AAGS0IUt18-LoVbI_UTXk51xEfF4vbr2Sr4`

### 1.3 Telegram Chat ID (твой ID)

1. Открой бота **@userinfobot** в Telegram
2. Нажми `/start`
3. Скопируй свой ID (число)

**Пример:** `6428365358`

---

## 📦 Шаг 2: Установка Системы

### 2.1 Клонирование проекта (если ещё не сделано)

```bash
cd /root
git clone https://github.com/AgeeKey/Mirai.git mirai
cd mirai/mirai-agent
```

### 2.2 Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2.3 Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Дополнительно (для веб и поиска):**
```bash
pip install beautifulsoup4 lxml requests python-dotenv
```

---

## ⚙️ Шаг 3: Настройка Конфигурации

### 3.1 Создание файла .env

```bash
cd /root/mirai/mirai-agent
nano .env
```

**Вставь этот контент (подставь СВОИ ключи!):**

```env
# OpenAI API
OPENAI_API_KEY=sk-proj-ТВОЙ_КЛЮЧ_СЮДА

# Grok API (опционально, если есть кредиты)
GROK_API_KEY=xai-ТВОЙ_КЛЮЧ_СЮДА

# Telegram Bot
TELEGRAM_BOT_TOKEN=ТВОЙ_ТОКЕН_СЮДА
TELEGRAM_CHAT_ID_ADMIN=ТВОЙ_CHAT_ID_СЮДА

# Режимы работы
DRY_RUN=false
ENABLE_TELEGRAM=true
AUTONOMOUS_MODE=true

# База данных
MIRAI_DB_PATH=data/state/mirai.db

# Безопасность
JWT_SECRET=mirai-secret-change-in-production
```

**Сохрани:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 3.2 Проверка .env файла

```bash
# Проверь что ключи на месте (без показа значений)
grep -E "OPENAI_API_KEY|TELEGRAM_BOT_TOKEN|TELEGRAM_CHAT_ID_ADMIN" .env | sed 's/=.*/=***/'
```

Должно вывести:
```
OPENAI_API_KEY=***
TELEGRAM_BOT_TOKEN=***
TELEGRAM_CHAT_ID_ADMIN=***
```

---

## 🔧 Шаг 4: Создание Systemd Сервиса

### 4.1 Создание файла сервиса

```bash
sudo nano /etc/systemd/system/mirai-agent.service
```

**Вставь:**

```ini
[Unit]
Description=Mirai Autonomous AI Agent
Documentation=https://github.com/AgeeKey/Mirai
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/mirai/mirai-agent
Environment="PATH=/root/mirai/mirai-agent/venv/bin"
EnvironmentFile=/root/mirai/mirai-agent/.env
ExecStart=/root/mirai/mirai-agent/venv/bin/python3 /root/mirai/mirai-agent/main.py
Restart=always
RestartSec=10

# Security
NoNewPrivileges=true
PrivateTmp=true

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=mirai-agent

[Install]
WantedBy=multi-user.target
```

**Сохрани:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 4.2 Активация сервиса

```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Включение автозапуска
sudo systemctl enable mirai-agent

# Запуск сервиса
sudo systemctl start mirai-agent

# Проверка статуса
sudo systemctl status mirai-agent
```

**Должно показать:** `Active: active (running)`

---

## 🌐 Шаг 5: Настройка Веб-Интерфейса (Nginx)

### 5.1 Установка Nginx (если не установлен)

```bash
sudo apt-get update
sudo apt-get install -y nginx
```

### 5.2 Создание конфига для домена (опционально)

```bash
sudo nano /etc/nginx/sites-available/mirai
```

**Вставь:**

```nginx
server {
    listen 80;
    server_name aimirai.online www.aimirai.online;
    
    # Логи
    access_log /var/log/nginx/mirai_access.log;
    error_log /var/log/nginx/mirai_error.log;
    
    # Reverse proxy к FastAPI
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        
        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Таймауты
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Статические файлы
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg)$ {
        proxy_pass http://127.0.0.1:8000;
        proxy_cache_valid 200 1h;
        expires 1h;
        add_header Cache-Control "public";
    }
}
```

### 5.3 Активация конфига

```bash
# Создать симлинк
sudo ln -sf /etc/nginx/sites-available/mirai /etc/nginx/sites-enabled/mirai

# Проверить конфиг
sudo nginx -t

# Перезапустить nginx
sudo systemctl restart nginx

# Проверить статус
sudo systemctl status nginx
```

---

## ✅ Шаг 6: Проверка Работы

### 6.1 Проверка Mirai Agent

```bash
# Статус сервиса
sudo systemctl status mirai-agent

# Логи (последние 50 строк)
sudo journalctl -u mirai-agent -n 50

# Live логи
sudo journalctl -u mirai-agent -f
```

**Должно быть:** `Active: active (running)` без ошибок

### 6.2 Проверка API

```bash
# Health check
curl http://localhost:8000/health

# Статистика
curl http://localhost:8000/stats
```

**Ожидаемый ответ:**
```json
{
    "status": "healthy",
    "agent_running": true,
    "trader_running": true
}
```

### 6.3 Проверка Веб-Интерфейса

**В браузере открой:**
```
http://localhost:8000/
```

**Или через домен (если настроен DNS):**
```
http://aimirai.online/
```

**Должно показать:**
- 🤖 Mirai AI Agent Dashboard
- 📊 4 карточки статуса (все зелёные)
- 📝 Active Tasks
- 📈 Statistics
- 📜 Recent Logs (обновляются)
- 🎮 4 кнопки управления

### 6.4 Проверка Telegram Бота

1. Открой Telegram
2. Найди своего бота (по username)
3. Отправь `/start`
4. Отправь `/status`

**Бот должен ответить** с информацией об агенте!

---

## 🎮 Шаг 7: Основные Команды Управления

### Управление сервисом:

```bash
# Запуск
sudo systemctl start mirai-agent

# Остановка
sudo systemctl stop mirai-agent

# Перезапуск
sudo systemctl restart mirai-agent

# Статус
sudo systemctl status mirai-agent

# Включить автозапуск
sudo systemctl enable mirai-agent

# Отключить автозапуск
sudo systemctl disable mirai-agent
```

### Просмотр логов:

```bash
# Последние 50 строк
sudo journalctl -u mirai-agent -n 50

# Live логи
sudo journalctl -u mirai-agent -f

# Логи за последний час
sudo journalctl -u mirai-agent --since "1 hour ago"

# Только ошибки
sudo journalctl -u mirai-agent -p err
```

### Telegram команды:

```
/start   - Приветствие
/status  - Статус агента
/help    - Помощь
/tasks   - Активные задачи
/stats   - Статистика
```

---

## 🔧 Шаг 8: Быстрая Диагностика

### Скрипт быстрой проверки:

```bash
cat << 'EOF' > /root/mirai/quick_check.sh
#!/bin/bash
echo "🔍 Быстрая Проверка Mirai AI"
echo ""
echo "1. Сервис Mirai Agent:"
systemctl is-active mirai-agent && echo "✅ Работает" || echo "❌ Не работает"
echo ""
echo "2. API Сервер:"
curl -s http://localhost:8000/health > /dev/null && echo "✅ Доступен" || echo "❌ Недоступен"
echo ""
echo "3. Ключи настроены:"
grep -q "OPENAI_API_KEY=sk-" /root/mirai/mirai-agent/.env && echo "✅ OpenAI ключ есть" || echo "❌ OpenAI ключ отсутствует"
grep -q "TELEGRAM_BOT_TOKEN=" /root/mirai/mirai-agent/.env && echo "✅ Telegram токен есть" || echo "❌ Telegram токен отсутствует"
echo ""
echo "4. База данных:"
[ -f /root/mirai/mirai-agent/data/state/mirai.db ] && echo "✅ База данных существует" || echo "❌ База данных отсутствует"
echo ""
echo "5. Последние 5 логов:"
sudo journalctl -u mirai-agent -n 5 --no-pager
EOF

chmod +x /root/mirai/quick_check.sh
```

**Запуск:**
```bash
/root/mirai/quick_check.sh
```

---

## 🆘 Решение Проблем

### Проблема 1: "Сервис не запускается"

**Диагностика:**
```bash
sudo journalctl -u mirai-agent -n 50
```

**Возможные причины:**
- ❌ Неверный путь в .service файле
- ❌ Нет прав на выполнение
- ❌ Отсутствуют зависимости

**Решение:**
```bash
# Проверь пути
ls -la /root/mirai/mirai-agent/main.py
ls -la /root/mirai/mirai-agent/venv/bin/python3

# Переустанови зависимости
cd /root/mirai/mirai-agent
source venv/bin/activate
pip install -r requirements.txt

# Перезапусти
sudo systemctl restart mirai-agent
```

### Проблема 2: "API ключи не работают"

**Диагностика:**
```bash
# Проверь .env файл
cat /root/mirai/mirai-agent/.env | grep API_KEY
```

**Решение:**
```bash
# Отредактируй .env
nano /root/mirai/mirai-agent/.env

# Замени ключи на правильные
# Перезапусти
sudo systemctl restart mirai-agent
```

### Проблема 3: "Telegram бот не отвечает"

**Диагностика:**
```bash
# Проверь логи Telegram
sudo journalctl -u mirai-agent | grep Telegram
```

**Возможные причины:**
- ❌ Неверный токен бота
- ❌ Неверный Chat ID
- ❌ ENABLE_TELEGRAM=false

**Решение:**
```bash
# Проверь .env
grep TELEGRAM /root/mirai/mirai-agent/.env

# Должно быть:
# TELEGRAM_BOT_TOKEN=твой_токен
# TELEGRAM_CHAT_ID_ADMIN=твой_id
# ENABLE_TELEGRAM=true

# Перезапусти
sudo systemctl restart mirai-agent
```

### Проблема 4: "Веб-интерфейс не открывается"

**Диагностика:**
```bash
# Проверь API
curl http://localhost:8000/health

# Проверь nginx
sudo systemctl status nginx
```

**Решение:**
```bash
# Перезапусти оба сервиса
sudo systemctl restart mirai-agent
sudo systemctl restart nginx
```

---

## 📊 Что Должно Работать После Запуска

### ✅ Checklist:

- [ ] Mirai Agent сервис активен (`systemctl status mirai-agent`)
- [ ] API отвечает на `/health` (HTTP 200)
- [ ] Веб-интерфейс открывается (`http://localhost:8000/`)
- [ ] Telegram бот отвечает на `/status`
- [ ] В логах видны запросы к OpenAI
- [ ] Задачи создаются и выполняются
- [ ] База данных растёт (`data/state/mirai.db`)
- [ ] Нет критических ошибок в логах

### 📈 Мониторинг:

**Через веб:**
```
http://localhost:8000/
```

**Через API:**
```bash
curl http://localhost:8000/stats
```

**Через Telegram:**
```
/status
```

**Через логи:**
```bash
sudo journalctl -u mirai-agent -f
```

---

## 🎯 Следующие Шаги

### После успешного запуска:

1. **Настрой домен (если есть):**
   ```bash
   # Настрой DNS A-запись
   aimirai.online → IP_сервера
   
   # Установи SSL
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d aimirai.online
   ```

2. **Добавь авторизацию:**
   ```bash
   # Для веб-интерфейса
   sudo apt install apache2-utils
   sudo htpasswd -c /etc/nginx/.htpasswd admin
   ```

3. **Настрой мониторинг:**
   - Проверяй логи ежедневно
   - Следи за статистикой через Telegram
   - Проверяй веб-интерфейс

4. **Backup:**
   ```bash
   # Создай backup
   cd /root/mirai/mirai-agent
   tar -czf mirai_backup_$(date +%Y%m%d).tar.gz \
       .env \
       data/state/mirai.db \
       configs/
   ```

---

## 📚 Полезные Ссылки

### Документация:
- `/root/mirai/MIRAI_READY_REPORT.md` - Полный отчёт о системе
- `/root/mirai/WEB_ACCESS_GUIDE.md` - Веб-интерфейс и доступ
- `/root/mirai/WEB_AND_AI_TOOLS.md` - AI Tools и возможности
- `/root/mirai/QUICK_START.md` - **ЭТА ИНСТРУКЦИЯ**

### API Endpoints:
- `http://localhost:8000/` - Dashboard
- `http://localhost:8000/health` - Health check
- `http://localhost:8000/stats` - Статистика
- `http://localhost:8000/status` - Полный статус

### Логи и Мониторинг:
```bash
# Live логи
sudo journalctl -u mirai-agent -f

# Статус
sudo systemctl status mirai-agent

# API
curl http://localhost:8000/health
```

---

## 🎉 Готово!

После выполнения всех шагов у тебя будет:

✅ **Полностью автономный AI агент**
- Работает 24/7
- Сам ставит и выполняет задачи
- Учится через GPT-4

✅ **Telegram бот**
- Отвечает на команды
- Показывает статус
- Отправляет уведомления

✅ **Веб-интерфейс**
- Мониторинг в реальном времени
- Красивый dashboard
- Live логи

✅ **AI Tools**
- Поиск в интернете
- Создание кода
- Выполнение задач

---

**Проверено:** 08.10.2025

**Версия:** Mirai AI v2.0

🚀 **Welcome to Autonomous AI Agent!**
