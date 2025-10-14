# 🌸 MIRAI - Где она и как её использовать

**Обновлено:** 14 октября 2025 после очистки проекта

---

## 🤖 MIRAI РАБОТАЕТ!

```bash
# Проверить запущенные процессы:
ps aux | grep mirai

# Результат:
✅ mirai_autonomous.py    (работает 2+ дня)
✅ dashboard_server.py    (веб-интерфейс)
```

---

## 🚀 БЫСТРЫЙ СТАРТ

### Способ 1: Интерактивное меню
```bash
cd /root/mirai/mirai-agent
./quick_start.sh
```

### Способ 2: Прямой запуск

#### 1. Автономный режим (MIRAI работает сама)
```bash
cd /root/mirai/mirai-agent
python3 mirai_autonomous.py --interval 180
```
**Что делает:** MIRAI автономно мониторит GitHub, анализирует код, улучшает себя

#### 2. Веб-дашборд
```bash
cd /root/mirai/mirai-agent
python3 dashboard_server.py
```
**Открыть:** http://localhost:5000  
**Что видно:** Метрики, CI/CD статус, обучение в реальном времени

#### 3. Интерактивный терминал (KAIZEN)
```bash
cd /root/mirai/mirai-agent
python3 kaizen_terminal.py
```
**Команды:**
- `help` - список команд
- `health` - проверка здоровья системы
- `metrics` - показать метрики
- `improve` - запустить самоулучшение

#### 4. Задать вопрос MIRAI
```bash
cd /root/mirai/mirai-agent
python3 ask_mirai.py
```
**Что делает:** Чат с MIRAI через AI

#### 5. Boss Mode (управление проектом)
```bash
cd /root/mirai/mirai-agent
python3 boss_mode.py
```
**Что делает:** Анализ проекта, управление задачами

---

## 📁 СТРУКТУРА ПРОЕКТА (ПОСЛЕ ОЧИСТКИ)

```
/root/mirai/
├── mirai-agent/                    ← Основной код
│   ├── core/                       ← Ядро AI агента
│   │   ├── autonomous_agent.py    ← Базовый AI агент (GPT-4o-mini)
│   │   ├── cicd_monitor.py        ← Мониторинг CI/CD
│   │   ├── github_integration.py  ← GitHub API
│   │   └── nasa_level/            ← NASA-уровень архитектура
│   │
│   ├── modules/                    ← Модули функциональности
│   │   ├── analytics_engine.py    ← Аналитика
│   │   ├── learning_api.py        ← API обучения
│   │   ├── database_manager.py    ← Работа с БД
│   │   └── multi_language_executor.py  ← Выполнение кода
│   │
│   ├── web/                        ← Веб-интерфейс
│   │   ├── templates/
│   │   │   ├── dashboard.html     ← Дашборд CI/CD
│   │   │   └── main.html          ← Основной интерфейс
│   │   └── static/                ← CSS, JS, изображения
│   │
│   ├── configs/                    ← Конфигурация
│   │   └── api_keys.json          ← API ключи
│   │
│   ├── tests/                      ← Тесты
│   │
│   ├── mirai_autonomous.py         ← Автономный режим ⭐
│   ├── dashboard_server.py         ← Веб-сервер ⭐
│   ├── kaizen_terminal.py          ← Терминал ⭐
│   ├── ask_mirai.py                ← Чат с MIRAI ⭐
│   ├── boss_mode.py                ← Режим босса ⭐
│   └── quick_start.sh              ← Быстрый старт ⭐
│
├── archive/                        ← Архив (старые файлы)
│   ├── reports/                    ← 23 старых отчёта
│   ├── old_tests/                  ← Старые тесты
│   └── old_scripts/                ← Старые скрипты
│
├── mirai-showcase/                 ← GitHub репозиторий
│
├── MIRAI_DIAGNOSIS_REPORT.md       ← Диагностика проблем
├── CLEANUP_DONE.md                 ← Отчёт об очистке
└── README.md                       ← Этот файл
```

---

## 🎯 ОСНОВНЫЕ ФАЙЛЫ (ЧТО ЗАПУСКАТЬ)

### Файлы агентов:
| Файл | Описание | Запуск |
|------|----------|--------|
| `mirai_autonomous.py` | Автономный режим MIRAI | `python3 mirai_autonomous.py` |
| `dashboard_server.py` | Веб-дашборд (Flask) | `python3 dashboard_server.py` |
| `kaizen_terminal.py` | Интерактивный терминал | `python3 kaizen_terminal.py` |
| `ask_mirai.py` | Чат с MIRAI | `python3 ask_mirai.py` |
| `boss_mode.py` | Управление проектом | `python3 boss_mode.py` |

### Файлы ядра:
| Файл | Описание |
|------|----------|
| `core/autonomous_agent.py` | Базовый AI агент (OpenAI GPT-4o-mini) |
| `core/cicd_monitor.py` | Мониторинг GitHub Actions |
| `core/github_integration.py` | Интеграция с GitHub API |
| `core/nasa_level/*` | Архитектура уровня NASA |

### Модули:
| Файл | Описание |
|------|----------|
| `modules/analytics_engine.py` | Аналитика метрик |
| `modules/learning_api.py` | API обучения |
| `modules/database_manager.py` | SQLite, PostgreSQL, MongoDB, Redis |
| `modules/multi_language_executor.py` | Выполнение Python, JS, TS, C, C++, Go, Rust, Bash |

---

## 🔍 ЛОГИ И МЕТРИКИ

```bash
# Логи автономного режима
tail -f /tmp/kaizen_mirai.log

# Метрики в реальном времени
tail -f /tmp/kaizen_mirai_metrics.jsonl

# Логи CI/CD мониторинга
ls -la /root/mirai/mirai-agent/ci_cd_logs/

# Логи обучения
ls -la /root/mirai/mirai-agent/learning/
```

---

## 🌐 ВЕБ-ИНТЕРФЕЙСЫ

### Dashboard (порт 5000)
```bash
python3 dashboard_server.py
# Открыть: http://localhost:5000
```

**Возможности:**
- 📊 Метрики CI/CD в реальном времени
- 🧪 Статус тестов и сборок
- 📈 Графики производительности
- 🎓 Прогресс обучения MIRAI
- 🔔 Уведомления о событиях

---

## 🧪 ТЕСТИРОВАНИЕ

```bash
# Быстрый тест системы
python3 quick_test_phase3.py

# Тест обучения
python3 test_learning_api.py

# Тест NASA интеграции
python3 test_nasa_integration.py

# Полный набор тестов
cd tests && pytest
```

---

## 🛠️ КОНФИГУРАЦИЯ

### API ключи
Файл: `/root/mirai/mirai-agent/configs/api_keys.json`

```json
{
  "OPENAI_API_KEY": "sk-...",
  "GITHUB_TOKEN": "ghp_..."
}
```

### Переменные окружения
Файл: `/root/mirai/mirai-agent/.env`

---

## 📊 МЕТРИКИ

MIRAI собирает метрики:
- ✅ Успешность CI/CD
- ⏱️ Время выполнения задач
- 🎓 Прогресс обучения
- 🔧 Количество улучшений кода
- 📈 Performance тренды

**Хранение:** `/tmp/kaizen_mirai_metrics.jsonl`

---

## 🤝 АГЕНТЫ

### 🤖 KAIZEN (改善) - Исполнитель
- Выполняет задачи
- Пишет код
- Запускает тесты
- Мониторит систему

### 🌸 MIRAI (未来) - Советник
- Принимает стратегические решения
- Анализирует данные
- Планирует улучшения
- Обучает KAIZEN

---

## 🎓 ВОЗМОЖНОСТИ

### Языки программирования (8):
- Python, JavaScript, TypeScript
- C, C++, Go, Rust, Bash

### Базы данных (4):
- SQLite, PostgreSQL, MongoDB, Redis

### Интеграции:
- ✅ GitHub API (issues, PRs, actions)
- ✅ OpenAI GPT-4o-mini
- ✅ Multi-language execution
- ✅ Real-time learning

---

## 📚 ДОКУМЕНТАЦИЯ

- **Диагностика:** `/root/mirai/MIRAI_DIAGNOSIS_REPORT.md`
- **Очистка:** `/root/mirai/CLEANUP_DONE.md`
- **Copilot инструкции:** `/root/mirai/.github/copilot-instructions.md`
- **Архитектура NASA:** `/root/mirai/archive/reports/NASA_*.md`

---

## 🐛 TROUBLESHOOTING

### Проблема: Веб-дашборд не открывается
```bash
# Проверить процесс
ps aux | grep dashboard_server

# Перезапустить
pkill -f dashboard_server
python3 dashboard_server.py
```

### Проблема: MIRAI не отвечает
```bash
# Проверить логи
tail -100 /tmp/kaizen_mirai.log

# Перезапустить автономный режим
pkill -f mirai_autonomous
python3 mirai_autonomous.py --interval 180
```

### Проблема: Не хватает зависимостей
```bash
cd /root/mirai/mirai-agent
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🎯 СЛЕДУЮЩИЕ ШАГИ

1. ✅ **Проект очищен** - удалены старые файлы
2. ✅ **Веб-интерфейс исправлен** - templates на месте
3. ✅ **Структура понятна** - всё разложено по папкам
4. 📋 **Можно использовать** - выбери режим из `quick_start.sh`

---

## 💡 СОВЕТЫ

1. **Для мониторинга:** Запусти `dashboard_server.py`
2. **Для автономной работы:** Запусти `mirai_autonomous.py`
3. **Для экспериментов:** Используй `kaizen_terminal.py`
4. **Для вопросов:** Используй `ask_mirai.py`

---

## 🌸 ВЫВОД

**MIRAI полностью работоспособна!**

Все критические проблемы исправлены:
- ✅ Веб-интерфейс работает
- ✅ Старые файлы архивированы
- ✅ Структура проекта понятна
- ✅ Документация обновлена

**Начни с:** `./quick_start.sh`

---

*Обновлено после генеральной очистки проекта* 🧹✨
