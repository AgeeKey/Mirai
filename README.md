# Mirai Agent - AI-Powered Autonomous Trading Agent

<div align="center">

![Mirai Agent](https://img.shields.io/badge/AI-Agent-blue)
![Python](https://img.shields.io/badge/Python-3.12-green)
![GPT-4](https://img.shields.io/badge/GPT--4-Enabled-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

**🤖 Автономный AI агент для торговли криптовалютой 24/7**

[Быстрый старт](#-быстрый-старт) • [Возможности](#-возможности) • [Документация](#-документация) • [API](#-api)

</div>

---

## 🎯 Что это?

**Mirai Agent** — это полностью автономный AI агент, который:

- 🤖 **Работает самостоятельно** 24/7 без вашего участия
- 🧠 **Использует GPT-4 и Grok** для принятия решений
- 💰 **Торгует криптовалютой** на Binance (BTC, ETH, BNB)
- 📚 **Учится из интернета** и применяет новые знания
- 🎯 **Ставит себе цели** и выполняет их автоматически
- 🌐 **Предоставляет API** для мониторинга и управления

---

## ✨ Возможности

### 🤖 Автономная работа
- Самостоятельное принятие решений через AI
- Автоматическая постановка и выполнение задач
- Обучение на основе анализа интернета
- Запоминание опыта в базе данных

### 💰 Торговля
- Анализ рынка криптовалют (BTC/USDT, ETH/USDT, BNB/USDT)
- AI-powered анализ через GPT-4
- Управление рисками (стоп-лосс, лимиты позиций)
- DEMO режим для безопасного тестирования

### 🌐 API Сервер
- REST API для мониторинга
- Веб-интерфейс статистики
- Интеграция с внешними системами
- Real-time логи и метрики

### 🧠 AI Движок
- GPT-4 (OpenAI) для сложных задач
- Grok (X.AI) как альтернатива
- Автоматическое переключение между моделями
- Кеширование ответов

---

## 🚀 Быстрый старт

### Требования
- Python 3.8+
- OpenAI API ключ
- Grok API ключ (опционально)
- Binance API ключ (для реальной торговли)

### Установка

```bash
# Клонируй репозиторий
git clone https://github.com/AgeeKey/Mirai.git
cd Mirai

# Создай виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Установи зависимости
cd mirai-agent
pip install -r requirements.txt

# Настрой API ключи
cp .env.example .env
nano .env  # Добавь свои ключи
```

### Запуск

#### Вариант 1: Панель управления (рекомендуется)
```bash
bash ../CONTROL_PANEL.sh
```

#### Вариант 2: Автоматический запуск
```bash
bash ../START_NOW.sh
```

#### Вариант 3: Ручной запуск
```bash
python -m core.master_agent
```

---

## 📊 Архитектура

```
mirai-agent/
├── core/                  # Ядро системы
│   ├── master_agent.py   # Главный оркестратор
│   ├── ai_engine.py      # AI движок (GPT-4/Grok)
│   └── config.py         # Конфигурация
├── modules/
│   ├── agent/            # Автономный агент
│   ├── trading/          # Торговый модуль
│   ├── api/              # API сервер
│   ├── security/         # Безопасность
│   └── utils/            # Утилиты
├── configs/              # Конфигурация
├── state/                # База данных
├── data/                 # Логи и данные
└── scripts/              # Скрипты управления
```

---

## 🎮 Панель управления

```bash
╔═══════════════════════════════════════════════════╗
║      🤖 MIRAI AGENT - ПАНЕЛЬ УПРАВЛЕНИЯ          ║
╚═══════════════════════════════════════════════════╝

  1) 🚀 Запустить агента
  2) 📊 Показать статус
  3) 📝 Показать логи (live)
  4) 🔍 Проверить API
  5) 💰 Статистика торговли
  6) 🧠 Спросить AI
  7) 🛑 Остановить агента
  8) 🔄 Перезапустить
  9) 📚 База данных агента
  0) ❌ Выход
```

---

## 🌐 API

### Endpoints

```bash
# Health check
GET http://localhost:8000/health

# Статистика агента
GET http://localhost:8000/stats

# Спросить AI
POST http://localhost:8000/ai/ask
{
  "question": "Что происходит с BTC?",
  "model": "gpt-4"
}

# Статус торговли
GET http://localhost:8000/trading/status

# Документация
GET http://localhost:8000/docs
```

---

## 📝 Примеры использования

### Проверка статуса
```bash
curl http://localhost:8000/health
```

### Получение статистики
```bash
curl http://localhost:8000/stats
```

### Вопрос к AI
```bash
curl -X POST http://localhost:8000/ai/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Стоит ли покупать BTC сейчас?"}'
```

---

## ⚙️ Конфигурация

### API Ключи (.env)
```env
OPENAI_API_KEY=sk-...
GROK_API_KEY=xai-...
BINANCE_API_KEY=...
BINANCE_SECRET_KEY=...
```

### Настройки агента (configs/production.yaml)
```yaml
agent_settings:
  cycle_interval: 60          # Секунды между циклами
  max_goals: 5                # Максимум целей
  learning_sessions_limit: 10 # Лимит обучающих сессий

trader_settings:
  cycle_interval: 120         # Секунды между анализом
  demo_mode: true             # DEMO режим (безопасно!)
```

---

## 🛡️ Безопасность

- ✅ API ключи хранятся в `.env` (не в git)
- ✅ DEMO режим для тестирования без рисков
- ✅ Лимиты позиций и стоп-лоссы
- ✅ Логирование всех действий
- ✅ Автоматические бэкапы

---

## 📚 Документация

- [Быстрый старт](QUICK_START_GUIDE.md) - Полный гайд
- [Простое объяснение](README_SIMPLE.md) - Для новичков
- [Быстрые команды](QUICK_COMMANDS.md) - Шпаргалка
- [Статус системы](STATUS.txt) - Текущее состояние

---

## 🔥 Что умеет агент?

### Автономные задачи
```
[19:27] 📝 Task created: Implement Sentiment Analysis for Market Predictions
[19:27] ⚡ Executing task...
[19:27] 💡 GPT-4: "Analyzing market sentiment..."
[19:27] ✅ Task completed
[19:27] 📊 Stats: 3 tasks completed, 3 learning sessions
```

### Торговля
```
[19:26] 📊 Analyzing market BTC/USDT...
[19:26] 💡 GPT-4 Analysis: "Market is stable, good time to buy"
[19:26] 💰 Balance: $10,000
[19:26] 📈 Positions: 0
[19:26] 🛡️ Max position size: $200
```

---

## 🤝 Вклад

Contributions welcome! 

1. Fork репозиторий
2. Создай feature ветку (`git checkout -b feature/amazing`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing`)
5. Открой Pull Request

---

## 📜 Лицензия

MIT License - см. [LICENSE](LICENSE)

---

## 💬 Контакты

- GitHub: [@AgeeKey](https://github.com/AgeeKey)
- Repository: [Mirai](https://github.com/AgeeKey/Mirai)

---

## ⚠️ Дисклеймер

**ВАЖНО:** Этот агент — экспериментальный проект. Торговля криптовалютой несет риски. Используйте DEMO режим для тестирования. Автор не несет ответственности за финансовые потери.

**Рекомендации:**
- ✅ Начинайте с DEMO режима
- ✅ Используйте малые суммы при реальной торговле
- ✅ Мониторьте агента регулярно
- ✅ Устанавливайте лимиты рисков

---

## 🌟 Star History

Если проект полезен - поставь ⭐!

---

<div align="center">

**Сделано с ❤️ и AI**

[⬆ Наверх](#mirai-agent---ai-powered-autonomous-trading-agent)

</div>
