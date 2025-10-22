# 🚀 MIRAI: Полный запуск на Windows 11 (локально)

Дата: 2025-10-22
Статус: Готово к локальному запуску без Linux-сервисов

---

## 1) Что уже есть в репозитории

- Единая точка входа: `mirai.py` (режимы: terminal, dashboard, autonomous, ask)
- Интеграция Web Search: `core/web_search_integration.py` (OpenAI gpt-5-search-api)
- Многоязычный исполнитель: `core/multi_language_executor.py`
- Память (SQLite): `core/memory_manager.py`
- Интеграции GitHub: `core/github_integration.py`
- Дашборд (Flask): `dashboard_server.py`
- Автономный сервис: `autonomous_service.py`
- Watchdog (Linux-ориентированный): `api_key_watchdog.py` — на Win запускается вручную/через Task Scheduler
- Безопасность: `.gitignore` уже исключает `.env` и `configs/api_keys.json`
- Зависимости: `mirai-agent/requirements.txt`

---

## 2) Необходимые программы

Установи:
- Python 3.11+ (при установке включи «Add Python to PATH»)
- Git
- Visual Studio Code (рекомендовано)

Опционально: WSL2 + Ubuntu (если хочешь окружение как на сервере)

Ссылки:
- Python: https://www.python.org/downloads/windows/
- Git: https://git-scm.com/download/win
- VS Code: https://code.visualstudio.com/

---

## 3) Клонирование репозитория

```powershell
git clone https://github.com/AgeeKey/Mirai.git
cd Mirai
```

---

## 4) Виртуальное окружение Python

```powershell
python -m venv venv
./venv/Scripts/Activate
```
Если PowerShell ругается на политику, запусти PowerShell от администратора:
```powershell
Set-ExecutionPolicy RemoteSigned
```

Обнови pip и установи зависимости:
```powershell
python -m pip install --upgrade pip
pip install -r mirai-agent/requirements.txt
```

---

## 5) Настройка ключей и переменных

### Вариант A — файл `configs/api_keys.json`
Создай файл `mirai-agent/configs/api_keys.json` по примеру ниже:
```json
{
  "openai": "<OPENAI_API_KEY>",
  "GITHUB_TOKEN": "<GITHUB_PERSONAL_ACCESS_TOKEN>",
  "TELEGRAM_BOT_TOKEN": "<TELEGRAM_BOT_TOKEN>",
  "TELEGRAM_CHAT_ID_ADMIN": "<TELEGRAM_CHAT_ID>"
}
```
Примечание: этот файл уже включён в `.gitignore` — не попадёт в Git.

### Вариант B — `.env`
Создай `mirai-agent/.env` (или используй пример `.env.example`):
```
OPENAI_API_KEY=<OPENAI_API_KEY>
GITHUB_TOKEN=<GITHUB_PERSONAL_ACCESS_TOKEN>
TELEGRAM_BOT_TOKEN=<TELEGRAM_BOT_TOKEN>
TELEGRAM_CHAT_ID_ADMIN=<TELEGRAM_CHAT_ID>
MIRAI_ENV=local
DASHBOARD_PORT=5000
```
И `python-dotenv` подхватит переменные автоматически (зависимость уже есть).

---

## 6) Быстрый старт (режимы запуска)

Все команды выполняй в корне проекта `Mirai` с активированным venv.

- Терминал (KAIZEN):
```powershell
python mirai-agent/mirai.py --mode terminal
```
- Дашборд (Flask):
```powershell
python mirai-agent/mirai.py --mode dashboard --port 5000
```
Открой браузер: http://localhost:5000

- Автономный режим:
```powershell
python mirai-agent/mirai.py --mode autonomous
```

- Разовый вопрос:
```powershell
python mirai-agent/mirai.py --mode ask "Что такое RAG?"
```

- Версия и здорова ли система:
```powershell
python mirai-agent/mirai.py --version
python mirai-agent/mirai.py --health
```

---

## 7) Проверка Web Search

Простой тест из Python:
```powershell
python - << 'PY'
from core.web_search_integration import WebSearchAgent
agent = WebSearchAgent()
print(agent.quick_search('Current weather in Tokyo')[:400])
PY
```
Если всё ок — увидишь актуальный ответ со сводкой.

---

## 8) Автозапуск и фоновые задачи на Windows

На сервере использовался systemd и cron. На Windows эквивалент — Планировщик заданий.

### Автозапуск автономного режима при входе в систему
1. Открой «Планировщик заданий» → «Создать задачу…»
2. Вкладка «Триггеры»: «При входе в систему»
3. Вкладка «Действия»: 
   - Программа: `powershell.exe`
   - Аргументы: `-NoProfile -ExecutionPolicy Bypass -Command "cd '%USERPROFILE%\Documents\Mirai'; ./venv/Scripts/Activate; python mirai-agent/mirai.py --mode autonomous"`
4. «Выполнять в наивысших правах» (по желанию)

### Периодический Watchdog (проверка API/очистка)
Запускать `api_key_watchdog.py` каждые 5–15 минут:
1. «Создать задачу…» → Триггеры: «По расписанию», каждые 5 или 15 минут
2. Действие (аналогично):
   - `powershell.exe`
   - Аргументы: `-NoProfile -ExecutionPolicy Bypass -Command "cd '%USERPROFILE%\Documents\Mirai'; ./venv/Scripts/Activate; python mirai-agent/api_key_watchdog.py"`

Альтернатива: создать `.bat` файл и запускать его из Планировщика:
```bat
@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
python mirai-agent\mirai.py --mode autonomous
```

---

## 9) Логи и диагностика

- Логи дашборда/сервиса выводятся в консоль.
- Доп. логи (если включены) — в `%TEMP%` или в каталоге проекта.
- Проверка зависимостей:
```powershell
python -V
pip list
```
- Тест памяти (SQLite): запусти автономный режим и убедись, что создаётся файл БД в `mirai-agent/data/` (если используется).

---

## 10) Безопасность

- Никогда не коммить `configs/api_keys.json` и `.env` (они уже в `.gitignore`).
- Храни ключи только локально.
- Если будешь пушить изменения — GitHub Push Protection заблокирует секреты в диффе.

---

## 11) Частые проблемы и решения

- «python» не найден: переоткрой терминал после установки Python или проверь PATH.
- PowerShell блокирует активацию: `Set-ExecutionPolicy RemoteSigned` (от админа).
- Port 5000 занят: поменяй `--port 5050`.
- Proxy/SSL: установи системные сертификаты и проверь интернет.
- Отсутствуют VC++ Build Tools (редко): установи «Desktop development with C++» из VS Build Tools для некоторых wheel-пакетов.

---

## 12) Полезные команды (шпаргалка)

```powershell
# 1) Клон, окружение, зависимости
git clone https://github.com/AgeeKey/Mirai.git
cd Mirai
python -m venv venv
./venv/Scripts/Activate
python -m pip install --upgrade pip
pip install -r mirai-agent/requirements.txt

# 2) Ключи
# Создай mirai-agent/configs/api_keys.json по примеру из раздела 5
# или mirai-agent/.env

# 3) Запуск
python mirai-agent/mirai.py --version
python mirai-agent/mirai.py --mode terminal
# или
python mirai-agent/mirai.py --mode dashboard --port 5000
# или
python mirai-agent/mirai.py --mode autonomous

# 4) Web Search быстрый тест
python - << 'PY'
from core.web_search_integration import WebSearchAgent
print(WebSearchAgent().quick_search('Bitcoin price in USD')[:300])
PY
```

---

## 13) Что дальше (бесплатные улучшения)
Смотри `FREE_IMPROVEMENTS_PLAN.md` — метрики обучения, база паттернов, SO-scraping и улучшения Dashboard — всё без затрат.

---

Готово! Если где-то споткнётся — пришли скрин/логи, починим быстро.
