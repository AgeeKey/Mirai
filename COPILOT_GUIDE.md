# 🚀 GitHub Copilot - Полное руководство для MIRAI проекта

## ✅ Что настроено

### 1. Copilot Instructions
📄 Файл: `.github/copilot-instructions.md`

Этот файл автоматически читается GitHub Copilot и помогает ему понимать:
- Структуру проекта MIRAI
- Coding standards
- Именования (KAIZEN, MIRAI)
- Типовые паттерны кода
- Эмодзи конвенции

### 2. VS Code Settings
📄 Файл: `.vscode/settings.json`

Настроено:
- ✅ Copilot включен для всех языков
- ✅ Автодополнение активировано
- ✅ Python форматирование (Black)
- ✅ Автосохранение файлов
- ✅ Git автофетч

### 3. Горячие клавиши
📄 Файл: `.vscode/keybindings.json`

Специальные команды для MIRAI:
- `Ctrl+Alt+K` - Запустить KAIZEN Terminal
- `Ctrl+Alt+M` - Проверить логи MIRAI
- `Ctrl+Alt+D` - Открыть Dashboard
- `Ctrl+Shift+I` - Copilot Chat
- `Ctrl+Shift+C` - Copilot для выделенного кода

## 🎯 Как использовать Copilot эффективно

### Специальные команды в Chat

Открой Copilot Chat (`Ctrl+Shift+I`) и используй:

```
/explain - Объяснить выделенный код
/tests - Сгенерировать тесты
/fix - Исправить ошибки
/optimize - Оптимизировать код
/docs - Создать документацию
```

### Примеры промптов для MIRAI проекта

#### ПЛОХО ❌
```
создай функцию
```

#### ХОРОШО ✅
```python
# Создай асинхронную функцию для KAIZEN Terminal
# Функция должна:
# 1. Принимать вопрос от пользователя (str)
# 2. Консультироваться с MIRAI через AutonomousAgent
# 3. Форматировать ответ с помощью rich.Panel
# 4. Логировать взаимодействие в /tmp/kaizen_terminal.log
# 5. Обрабатывать ошибки OpenAI API с retry
# Используй async/await, type hints и docstrings
```

#### ОТЛИЧНО 🌟
```python
# KAIZEN Command: Анализ производительности CI/CD
# 
# Создай команду для kaizen_terminal.py:
# - Название: cmd_performance_analysis
# - Получает метрики из CICDMonitor
# - Анализирует тренды (последние 20 runs)
# - Выводит таблицу с Rich.Table:
#   * Столбцы: Run#, Duration, Success, Trend (↑↓)
#   * Цвета: зелёный для улучшения, красный для ухудшения
# - Спрашивает MIRAI о рекомендациях
# - Формат вывода: Panel с заголовком "📊 Performance Analysis"
# 
# Стиль кода:
# - Async function
# - Type hints
# - Rich formatting (console.print, Panel, Table)
# - Error handling с logger
# - Docstring в Google Style
```

## 💡 Работа с комментариями

Copilot отлично понимает подробные комментарии. Используй это!

```python
# TODO: Добавить команду для KAIZEN Terminal
# Команда: /analyze [файл]
# Что делает:
# - Читает указанный Python файл
# - Анализирует сложность (cyclomatic complexity)
# - Находит потенциальные проблемы
# - Спрашивает MIRAI о рекомендациях по улучшению
# - Выводит красивый отчёт с rich.Panel

async def cmd_analyze(self, filepath: str):
    # Copilot автоматически сгенерирует код здесь!
    pass
```

## 🤖 Интеграция с KAIZEN и MIRAI

### Запросы через Copilot Chat

Попробуй в Copilot Chat:

```
@workspace Как запустить KAIZEN Terminal?
```

```
@workspace Покажи статус MIRAI автономного сервиса
```

```
@workspace Создай новую команду для kaizen_terminal.py которая показывает GitHub Actions logs
```

### Генерация целых файлов

В Copilot Chat:
```
Создай новый файл telegram_notifier.py для отправки уведомлений MIRAI в Telegram.

Требования:
- Использовать python-telegram-bot
- Класс TelegramNotifier
- Методы: send_alert, send_metric, send_report
- Интеграция с CICDMonitor
- Async/await
- Логирование
- Конфиг из configs/api_keys.json
```

## 🔧 Продвинутые техники

### 1. Multi-file editing
Выдели код в нескольких файлах, открой Chat:
```
Refactor this code to use dependency injection pattern
```

### 2. Context-aware suggestions
Copilot видит открытые файлы. Открой:
- `autonomous_agent.py`
- `kaizen_terminal.py`

Потом начни писать новую функцию - Copilot поймёт контекст!

### 3. Inline documentation
Напиши только:
```python
def complex_algorithm(data: list) -> dict:
    """
```
Copilot допишет docstring автоматически!

## 📚 Шпаргалка команд

### В редакторе
- `Tab` - Принять предложение
- `Esc` - Отклонить
- `Alt+]` / `Alt+[` - Следующее/предыдущее предложение
- `Ctrl+Enter` - Открыть панель с 10 вариантами

### В Chat
- `/explain` - Объяснить код
- `/tests` - Сгенерировать тесты
- `/fix` - Исправить баги
- `/doc` - Документация
- `@workspace` - Контекст всего проекта
- `@terminal` - Команды терминала

### KAIZEN Shortcuts
- `Ctrl+Alt+K` - KAIZEN Terminal
- `Ctrl+Alt+M` - Логи MIRAI
- `Ctrl+Alt+D` - Dashboard

## 🎓 Лучшие практики

### ✅ DO
- Пиши подробные комментарии ПЕРЕД кодом
- Используй type hints
- Открывай связанные файлы для контекста
- Проверяй сгенерированный код
- Используй `/tests` для автотестов

### ❌ DON'T
- Не принимай код слепо
- Не забывай про безопасность
- Не используй Copilot для sensitive data
- Не полагайся на Copilot для критической логики без review

## 🌟 Примеры для MIRAI

### Создание новой команды
```python
# В kaizen_terminal.py добавь команду для взаимодействия с MIRAI:
# Команда: consult
# Синтаксис: consult <question>
# Функция: Задаёт вопрос MIRAI и выводит ответ красиво
# Формат: Panel с заголовком "🌸 MIRAI Consultation"
```

### Добавление мониторинга
```python
# Создай новый monitor для отслеживания использования ресурсов:
# - CPU usage
# - Memory usage  
# - Disk I/O
# - Network traffic
# Интегрируй с autonomous_service.py
# Логируй в /tmp/resource_metrics.jsonl
```

### Улучшение Dashboard
```javascript
// В dashboard.html добавь график для:
// - Тренд продолжительности runs (линейный график)
// - Распределение типов ошибок (pie chart)
// - Активность по часам (bar chart)
// Используй Chart.js, цвета согласно существующей палитре
```

## 🚀 Готово!

Теперь GitHub Copilot полностью настроен для работы с MIRAI проектом!

Попробуй:
1. Открой `kaizen_terminal.py`
2. Напиши комментарий о новой функции
3. Нажми Enter - Copilot предложит код!

改善 (KAIZEN) - Continuous Improvement с помощью AI! 🤖
