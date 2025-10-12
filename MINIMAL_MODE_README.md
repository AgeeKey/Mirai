# 🚀 MIRAI - MINIMAL EXPERIMENT MODE

## ✅ Готово к работе!

### 🎯 Что работает:

- ✅ **OpenAI API** - подключен и работает
- ✅ **Локальный веб-сервер** - запущен на порту 8000
- ✅ **Интерактивный чат** - доступен через браузер

### ❌ Что отключено:

- ❌ Telegram Bot
- ❌ Binance Trading
- ❌ Домены и SSL
- ❌ База данных
- ❌ Redis
- ❌ Docker
- ❌ Все внешние сервисы

---

## 🌐 Доступ к серверу

### Основной интерфейс:

```
http://localhost:8000
```

### API Endpoints:

**Главная страница с чатом:**

```
http://localhost:8000/
```

**Тест OpenAI подключения:**

```
http://localhost:8000/api/test
```

**Чат с AI:**

```
http://localhost:8000/api/chat?message=Привет
```

**Проверка здоровья системы:**

```
http://localhost:8000/health
```

**API документация:**

```
http://localhost:8000/docs
```

---

## 🎮 Управление сервером

### Запуск сервера:

```bash
cd /root/mirai/mirai-agent
source venv/bin/activate
export OPENAI_API_KEY="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"
python3 simple_server.py
```

### Запуск в фоне:

```bash
cd /root/mirai/mirai-agent
source venv/bin/activate
export OPENAI_API_KEY="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"
nohup python3 simple_server.py > /tmp/mirai_server.log 2>&1 &
```

### Проверка статуса:

```bash
ps aux | grep simple_server.py
```

### Остановка сервера:

```bash
pkill -f simple_server.py
```

### Просмотр логов:

```bash
tail -f /tmp/mirai_server.log
```

---

## 🧪 Быстрые тесты

### 1. Проверка сервера:

```bash
curl http://localhost:8000/health
```

### 2. Тест OpenAI:

```bash
curl "http://localhost:8000/api/test"
```

### 3. Отправка сообщения AI:

```bash
curl "http://localhost:8000/api/chat?message=Привет,%20как%20дела?"
```

### 4. Быстрый Python тест:

```bash
cd /root/mirai
python3 test_openai_quick.py
```

---

## 📁 Структура файлов

### Основные файлы:

- `/root/mirai/mirai-agent/.env` - Минимальная конфигурация
- `/root/mirai/mirai-agent/simple_server.py` - Основной сервер
- `/root/mirai/test_openai_quick.py` - Тест OpenAI
- `/root/mirai/start_minimal.sh` - Скрипт запуска

### Виртуальное окружение:

- `/root/mirai/mirai-agent/venv/` - Python зависимости

---

## 🔧 Установленные пакеты

Минимальный набор зависимостей:

- `openai` - для работы с OpenAI API
- `fastapi` - веб-фреймворк
- `uvicorn` - ASGI сервер
- `python-dotenv` - для .env файлов
- `pydantic` - валидация данных
- `aiohttp` - асинхронные HTTP запросы

---

## 🎨 Функции веб-интерфейса

### Главная страница:

- Красивый дизайн с градиентом
- Статус системы
- Интерактивный чат с AI
- Быстрые ссылки на API

### Чат:

- Отправка сообщений AI
- История чата (в памяти)
- Красивое отображение ответов

---

## 📊 Текущий статус

✅ **Сервер запущен**: PID 115629
✅ **OpenAI подключен**: Работает
✅ **Порт**: 8000
✅ **Режим**: Minimal Experiment

---

## 🚦 Следующие шаги

1. **Откройте браузер**: http://localhost:8000
2. **Попробуйте чат**: Введите сообщение и получите ответ от AI
3. **Изучите API**: Перейдите на http://localhost:8000/docs
4. **Экспериментируйте**: Добавляйте новые функции в `simple_server.py`

---

## 💡 Советы

### Добавление новых функций:

Отредактируйте `/root/mirai/mirai-agent/simple_server.py` и добавьте новые endpoints.

### Изменение модели AI:

В файле `simple_server.py` измените `model="gpt-3.5-turbo"` на другую модель (например, `gpt-4`).

### Увеличение лимита токенов:

Измените параметр `max_tokens` в функциях чата.

---

## 📞 Поддержка

Если что-то не работает:

1. Проверьте логи: `tail -f /tmp/mirai_server.log`
2. Проверьте порт: `lsof -i:8000`
3. Перезапустите сервер
4. Проверьте OpenAI ключ: `python3 test_openai_quick.py`

---

## 🎉 Готово!

Система настроена и готова к экспериментам!
Минимальная конфигурация - максимальная простота!

**Наслаждайтесь экспериментами с AI! 🤖**
