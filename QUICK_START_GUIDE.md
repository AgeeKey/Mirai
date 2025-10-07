# 🚀 MIRAI AGENT - БЫСТРЫЙ СТАРТ

## 📋 ЧТО УЖЕ ЕСТЬ:
✅ VPS сервер (Linux)
✅ OpenAI ключ (GPT-4)
✅ Grok ключ (X.AI)
✅ Готовый код Mirai Agent
✅ Ключи ИСПРАВЛЕНЫ и настроены!

---

## 🎯 ЗАПУСК ЗА 3 ШАГА:

### ШАГ 1: Установка зависимостей (1 минута)

```bash
cd /root/mirai/mirai-agent

# Создаем виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Устанавливаем библиотеки
pip install -r requirements.txt
```

### ШАГ 2: Тестовый запуск (30 секунд)

```bash
# Запускаем агента
python -m core.master_agent
```

**ЧТО ДОЛЖНО ПРОИЗОЙТИ:**
```
🤖 MasterAgent initialized
🚀 Starting MasterAgent...
✅ AI Engine готов (GPT-4 + Grok)
🔄 Автономный агент запущен
💰 Трейдер запущен (DEMO режим)
🌐 API сервер: http://0.0.0.0:8000
```

### ШАГ 3: Проверка работы

**Открой в браузере:**
```
http://ВАШ_IP_АДРЕС:8000/health
```

**Должно показать:**
```json
{
  "status": "🟢 healthy",
  "uptime": "5 минут",
  "agent": "работает",
  "trader": "работает (DEMO)",
  "ai": "✅ GPT-4 готов"
}
```

---

## 🎮 ЧТО ДЕЛАЕТ АГЕНТ СЕЙЧАС:

### 1️⃣ АВТОНОМНЫЙ АГЕНТ (AutonomousAgent)
- ✅ Работает в цикле каждые 60 секунд
- ✅ Ставит себе цели (например: "изучить рынок BTC")
- ✅ Использует GPT-4 для принятия решений
- ✅ Учится из интернета (поиск информации)
- ✅ Запоминает что делал (БД: `state/agent_memory.db`)

**Логи агента:**
```bash
tail -f data/logs/ai_agent.log
```

### 2️⃣ ТРЕЙДЕР (Trader)
- ✅ Анализирует рынок каждые 120 секунд
- ⚠️ **DEMO режим** (НЕ торгует реально)
- ✅ Использует AI для анализа
- ✅ Показывает сигналы: КУПИТЬ/ПРОДАТЬ/ЖДАТЬ

**Логи трейдера:**
```bash
tail -f logs/mirai_agent.log
```

### 3️⃣ API СЕРВЕР (FastAPI)
**Доступные эндпоинты:**

```bash
# Проверка здоровья
curl http://localhost:8000/health

# Статистика агента
curl http://localhost:8000/stats

# Спросить AI
curl -X POST http://localhost:8000/ai/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Что сейчас происходит с BTC?"}'

# Статус трейдера
curl http://localhost:8000/trading/status
```

---

## 📊 КАК СМОТРЕТЬ ЧТО ДЕЛАЕТ АГЕНТ:

### Вариант 1: Логи в реальном времени
```bash
# Все логи
tail -f data/logs/*.log

# Только агент
tail -f data/logs/ai_agent.log

# Только трейдер
tail -f logs/mirai_agent.log
```

### Вариант 2: API запросы
```bash
# Что агент делает сейчас
curl http://localhost:8000/agent/status

# Сколько задач выполнено
curl http://localhost:8000/stats
```

### Вариант 3: База данных
```bash
# Открыть БД агента
sqlite3 state/agent_memory.db

# Посмотреть все цели
SELECT * FROM goals;

# Посмотреть историю действий
SELECT * FROM actions ORDER BY timestamp DESC LIMIT 10;
```

---

## 🛠️ НАСТРОЙКИ:

### Включить реальную торговлю (⚠️ ОПАСНО!)

1. Получи API ключи Binance: https://www.binance.com/en/my/settings/api-management

2. Отредактируй `.env`:
```bash
BINANCE_API_KEY=твой_ключ
BINANCE_SECRET_KEY=твой_секрет
BINANCE_TESTNET=false  # false = реальная торговля
```

3. В `configs/production.yaml` измени:
```yaml
trader_settings:
  demo_mode: false  # Включить реальную торговлю
```

⚠️ **ВАЖНО:** Начинай с малых сумм! Агент может терять деньги!

### Изменить частоту работы

В `configs/production.yaml`:
```yaml
agent_settings:
  cycle_interval: 60  # Секунды между циклами агента

trader_settings:
  cycle_interval: 120  # Секунды между анализом рынка
```

---

## 🚀 ЗАПУСК 24/7 (systemd)

### Создать сервис:
```bash
cd /root/mirai/mirai-agent

# Скопировать service файл
sudo cp scripts/mirai-agent.service /etc/systemd/system/

# Отредактировать пути
sudo nano /etc/systemd/system/mirai-agent.service

# Запустить
sudo systemctl daemon-reload
sudo systemctl enable mirai-agent
sudo systemctl start mirai-agent

# Проверить статус
sudo systemctl status mirai-agent

# Логи
sudo journalctl -u mirai-agent -f
```

---

## 🔥 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

### Пример 1: Спросить AI о рынке
```bash
curl -X POST http://localhost:8000/ai/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Стоит ли сейчас покупать Bitcoin?",
    "model": "gpt-4"
  }'
```

### Пример 2: Дать агенту задачу
```bash
curl -X POST http://localhost:8000/agent/goal \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Изучить стратегию Mean Reversion для BTC"
  }'
```

### Пример 3: Получить рекомендацию трейдера
```bash
curl http://localhost:8000/trading/recommendation
```

---

## 📱 TELEGRAM БОТ (ОПЦИОНАЛЬНО):

1. Создай бота: https://t.me/BotFather
2. Получи токен
3. Добавь в `.env`:
```bash
TELEGRAM_BOT_TOKEN=твой_токен
TELEGRAM_CHAT_ID_ADMIN=твой_chat_id
```

4. Перезапусти агента

Теперь агент будет присылать уведомления в Telegram!

---

## ❓ ЧАСТЫЕ ВОПРОСЫ:

### Q: Агент не запускается
```bash
# Проверь логи
cat data/logs/ai_agent.log

# Проверь что Python 3.8+
python3 --version

# Переустанови зависимости
pip install -r requirements.txt --force-reinstall
```

### Q: AI не отвечает
```bash
# Проверь ключи
cat .env | grep API_KEY

# Тест OpenAI
python scripts/test_ai_keys.py
```

### Q: Как остановить агента
```bash
# Если запущен в терминале
Ctrl+C

# Если systemd сервис
sudo systemctl stop mirai-agent
```

### Q: Где хранятся данные?
```
state/          - БД агента
data/logs/      - Логи
data/backups/   - Бэкапы
```

### Q: Как сделать бэкап?
```bash
cd /root/mirai/mirai-agent
./scripts/backup.sh
```

---

## 🎯 ЧТО ДАЛЬШЕ?

### Уровень 1: Наблюдение (первые дни)
- ✅ Запусти агента
- ✅ Смотри логи
- ✅ Проверяй API
- ✅ Изучай что он делает

### Уровень 2: Настройка (1-2 недели)
- ✅ Измени настройки под себя
- ✅ Добавь Telegram бот
- ✅ Протестируй на Binance Testnet

### Уровень 3: Продакшн (когда готов)
- ✅ Включи реальную торговлю
- ✅ Настрой малый депозит
- ✅ Мониторь 24/7
- ✅ Анализируй результаты

---

## 🆘 ПОМОЩЬ:

**Логи:**
```bash
tail -f data/logs/ai_agent.log
tail -f logs/mirai_agent.log
```

**Статус:**
```bash
curl http://localhost:8000/health
```

**Перезапуск:**
```bash
sudo systemctl restart mirai-agent
```

---

## ✅ ЧЕКЛИСТ ГОТОВНОСТИ:

- [ ] Python зависимости установлены
- [ ] `.env` файл настроен (ключи API)
- [ ] Агент запускается без ошибок
- [ ] API отвечает на http://IP:8000/health
- [ ] Логи пишутся в `data/logs/`
- [ ] Понимаю как остановить/перезапустить
- [ ] Знаю где смотреть ошибки
- [ ] (Опционально) Binance ключи настроены
- [ ] (Опционально) Telegram бот работает
- [ ] (Опционально) Systemd сервис создан

---

🎉 **ВСЁ ГОТОВО! ТВОЙ AI АГЕНТ РАБОТАЕТ 24/7!**

💬 Если что-то не работает - проверь логи и API эндпоинты выше.
