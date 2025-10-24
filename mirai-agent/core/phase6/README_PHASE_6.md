# 🚀 Phase 6: Application Control System

## 📋 Описание

Phase 6 - это специализированный модуль для управления приложениями на компьютере. Агент MIRAI получает полный контроль над:

- **CapCut** - видео редактирование
- **VSCode** - редактирование кода  
- **File Explorer** - управление файлами
- **System Apps** - Notepad, Calculator, Task Manager, Command Prompt

## 🎯 Возможности (150 шагов)

### РАЗДЕЛ 1: Application Detection & Initialization (Шаги 1-35)
✅ Обнаружение установленных приложений  
✅ Поиск путей к приложениям  
✅ Создание реестра приложений  
✅ Запуск и контроль приложений  
✅ Обработка ошибок запуска

### РАЗДЕЛ 2: CapCut Video Editing (Шаги 36-75)
🚧 Управление CapCut  
🚧 Импорт видео файлов  
🚧 Редактирование timeline  
🚧 Эффекты и переходы  
🚧 Экспорт видео

### РАЗДЕЛ 3: VSCode Code Editing (Шаги 76-105)
✅ Запуск VSCode  
✅ Управление файлами (открытие, сохранение, закрытие)  
✅ Редактирование кода  
✅ Поиск и замена  
✅ Форматирование и запуск кода  
✅ Работа с терминалом

### РАЗДЕЛ 4: File Explorer & System Apps (Шаги 106-135)
✅ Notepad - текстовый редактор  
✅ Calculator - калькулятор  
✅ Task Manager - управление процессами  
✅ Command Prompt - выполнение команд  
🚧 File Explorer - управление файлами

### РАЗДЕЛ 5: Error Handling & Integration (Шаги 136-150)
🚧 Обработка сбоев приложений  
🚧 Координация между приложениями  
🚧 Мониторинг ресурсов  
🚧 Интеграция с Vision системой

## 📦 Установка

```bash
cd /home/runner/work/Mirai/Mirai/mirai-agent
pip install -r requirements.txt
```

Дополнительные зависимости:
```bash
pip install pyautogui psutil
```

## 🚀 Быстрый старт

### Пример 1: Обнаружение приложений

```python
from core.phase6.app_detector import detect_applications

# Обнаружить все установленные приложения
results = detect_applications()

print(f"Найдено приложений: {results['installed_count']}")
print(f"Приложения: {results['installed_apps']}")
```

### Пример 2: Работа с Notepad

```python
from core.phase6.system_app_controller import get_system_app_controller

# Получить контроллер системных приложений
controller = get_system_app_controller()
notepad = controller.get_notepad()

# Открыть Notepad
notepad.open_notepad()

# Написать текст
notepad.edit_text("Привет из MIRAI! 🤖")

# Сохранить файл
notepad.save_text("C:/temp/mirai_test.txt")

# Закрыть
notepad.close()
```

### Пример 3: Работа с VSCode

```python
from core.phase6.vscode_controller import get_vscode_controller

# Получить VSCode контроллер
vscode = get_vscode_controller()

# Запустить VSCode
vscode.launch_vscode()

# Создать новый файл
vscode.create_new_file()

# Написать код
code = """
def hello_mirai():
    print("Hello from MIRAI!")
    
hello_mirai()
"""
vscode.type_code(code)

# Сохранить
vscode.save_file("test_script.py")

# Форматировать код
vscode.format_code()

# Запустить
vscode.run_code()
```

### Пример 4: Выполнение команд

```python
from core.phase6.system_app_controller import get_system_app_controller

# Получить CMD контроллер
controller = get_system_app_controller()
cmd = controller.get_cmd()

# Выполнить команду
output = cmd.execute_command("dir")

# Прочитать вывод
result = cmd.read_output(output)
print(f"Строк вывода: {result['line_count']}")
```

## 🏗️ Архитектура

```
core/phase6/
├── __init__.py                    # Инициализация модуля
├── application_manager.py         # Главный менеджер (Шаг 10)
├── app_detector.py                # Обнаружение приложений (Шаги 1-20)
├── app_launcher.py                # Запуск приложений (Шаги 21-35)
├── vscode_controller.py           # VSCode контроллер (Шаги 76-105)
├── system_app_controller.py       # Системные приложения (Шаги 121-135)
├── application_tests.py           # Тесты
└── README_PHASE_6.md             # Эта документация
```

## 🧪 Тестирование

Запуск всех тестов:

```bash
cd /home/runner/work/Mirai/Mirai/mirai-agent
python -m core.phase6.application_tests
```

Тесты проверяют:
- ✅ Инициализацию Application Manager
- ✅ Регистрацию приложений
- ✅ Обнаружение установленных приложений
- ✅ Запуск и закрытие приложений
- ✅ Контроллеры VSCode и System Apps
- ✅ Выполнение команд

## 📊 Статистика реализации

| Раздел | Шаги | Статус | Прогресс |
|--------|------|--------|----------|
| Detection & Init | 1-35 | ✅ Готово | 100% |
| CapCut Video | 36-75 | 🚧 В разработке | 20% |
| VSCode Editing | 76-105 | ✅ Готово | 100% |
| File Explorer | 106-120 | 🚧 В разработке | 30% |
| System Apps | 121-135 | ✅ Готово | 100% |
| Error Handling | 136-150 | 🚧 В разработке | 40% |

**Общий прогресс: ~65%** (98 из 150 шагов реализовано)

## 🔧 API Reference

### ApplicationManager

```python
from core.phase6.application_manager import get_application_manager

manager = get_application_manager()

# Регистрация приложения
manager.register_application(app_info)

# Получение информации
app = manager.get_application("notepad")

# Список всех приложений
apps = manager.list_applications()

# Статистика
stats = manager.get_statistics()
```

### AppDetector

```python
from core.phase6.app_detector import AppDetector

detector = AppDetector()

# Полное обнаружение
results = detector.discover_all()

# Проверка запущенных приложений
is_running = detector.running_detector.is_app_running("notepad")
```

### AppLauncher

```python
from core.phase6.app_launcher import launch_application, close_application

# Запуск приложения
result = launch_application("notepad", wait_ready=True)

if result.success:
    print(f"Запущено, PID: {result.pid}")

# Закрытие
close_application("notepad", force=False)
```

## 🐛 Известные ограничения

1. **pyautogui** - требует активное GUI окружение, не работает в headless режиме
2. **Windows-специфичные функции** - некоторые приложения доступны только на Windows
3. **Права доступа** - некоторые операции требуют прав администратора
4. **Таймауты** - приложения могут запускаться медленно на слабых системах

## 🔮 Планы развития

### В следующей версии (v1.1):
- [ ] Полная реализация CapCut контроллера (Шаги 36-75)
- [ ] File Explorer контроллер (Шаги 106-120)
- [ ] Улучшенная обработка ошибок (Шаги 136-150)
- [ ] Интеграция с Vision системой для автоматического распознавания UI

### В будущем (v2.0):
- [ ] Поддержка macOS и Linux приложений
- [ ] Machine Learning для оптимизации работы с приложениями
- [ ] Автоматическое обучение работе с новыми приложениями
- [ ] Web-интерфейс для управления

## 💡 Примеры использования

### Сценарий 1: Автоматизация документирования

```python
# Открыть VSCode, написать код, добавить комментарии
vscode = get_vscode_controller()
vscode.launch_vscode()
vscode.open_file("my_project.py")
vscode.type_code("# TODO: Add documentation")
vscode.save_file()
```

### Сценарий 2: Системный мониторинг

```python
# Открыть Task Manager и получить статистику
controller = get_system_app_controller()
tm = controller.get_task_manager()
tm.open_task_manager()
processes = tm.monitor_processes()
print(f"Топ процессов по CPU: {processes['top_cpu']}")
```

### Сценарий 3: Пакетная обработка

```python
# Выполнить несколько команд
cmd = get_system_app_controller().get_cmd()
commands = ["dir", "ipconfig", "systeminfo"]

for command in commands:
    output = cmd.execute_command(command)
    result = cmd.read_output(output)
    print(f"{command}: {result['line_count']} строк")
```

## 🤝 Вклад в проект

Если вы хотите внести вклад:

1. Реализуйте недостающие шаги (CapCut, File Explorer)
2. Добавьте тесты для новых функций
3. Улучшите обработку ошибок
4. Добавьте поддержку других ОС
5. Оптимизируйте производительность

## 📝 Лицензия

Часть проекта MIRAI AI Agent

---

**Автор:** MIRAI AI Team  
**Дата:** 2025-10-24  
**Версия:** 1.0  
**Статус:** 🚧 В активной разработке
