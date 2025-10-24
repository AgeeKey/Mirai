# MIRAI Desktop Agent V2

**Полный контроль над компьютером через AI**

## 🚀 Возможности

MIRAI Desktop Agent V2 - это автономный AI агент, который может управлять вашим компьютером:

### 🖱️ Управление вводом
- **Мышь**: клики, движение, получение позиции
- **Клавиатура**: ввод текста, нажатие клавиш и комбинаций (Ctrl+C, Alt+Tab, etc.)

### 📸 Визуальное восприятие
- **Скриншоты**: полный экран или выбранная область
- **GPT-4 Vision**: анализ содержимого экрана через AI
- **OCR**: распознавание текста на экране (pytesseract)
- **Computer Vision**: поиск изображений на экране (OpenCV)

### 🪟 Управление окнами
- Поиск окон по заголовку
- Активация и переключение между окнами
- Работа с несколькими приложениями одновременно
- Получение информации о запущенных процессах

### 🌐 Интеграция с браузером
- Открытие URL в Chrome/Firefox/Edge
- Интеграция с `browser_automation.py` для расширенных возможностей
- Поиск в Google напрямую

### 🤖 Автономная работа
- **Естественный язык**: задачи на русском или английском
- **Самостоятельное принятие решений**: агент сам решает какие действия нужны
- **Интеграция с MIRAI Core**: использует RAG, память, и другие возможности
- **Безопасность**: ограничения на частоту действий и запрещенные зоны

### 🧠 Память и логирование
- История всех действий
- Интеграция с долговременной памятью MIRAI
- Сохранение скриншотов с отметками времени
- Экспорт истории в JSON

## 📋 Требования

### Обязательные зависимости

```bash
pip install pyautogui pillow opencv-python openai
```

### Опциональные зависимости

```bash
# OCR (распознавание текста)
pip install pytesseract

# Windows API (для расширенных возможностей на Windows)
pip install pywin32

# MIRAI Core интеграция
# (уже включена если используете полную установку MIRAI)
```

### Системные требования

- **Python**: 3.10+
- **ОС**: Windows 10/11, Linux, macOS
- **API ключ**: OpenAI (для GPT-4o Vision)

#### Windows
- pywin32 для расширенных функций работы с окнами

#### Linux
- `scrot` или `gnome-screenshot` для скриншотов
- `xdotool` для управления окнами

#### macOS
- Разрешения на Accessibility (System Preferences → Security & Privacy → Privacy → Accessibility)

### Для OCR

**Windows:**
1. Скачать Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Установить и добавить в PATH
3. Или указать путь: `pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`

**Linux:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-rus
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

## 🎯 Использование

### Базовое использование

```python
from core.desktop_agent_v2 import MiraiDesktopAgent

# Создать агента
agent = MiraiDesktopAgent(
    enable_safety=True,      # Включить проверки безопасности
    enable_memory=True,      # Включить долговременную память
    screenshots_dir="screenshots"  # Директория для скриншотов
)

# Выполнить задачу на естественном языке
result = agent.execute_task(
    "Открой Chrome, найди в Google 'погода в Москве' и сделай скриншот"
)

print(result)
```

### Прямые команды

```python
# Управление мышью
agent.click_at_position(100, 200)
agent.move_mouse(500, 500, duration=1.0)
x, y = agent.get_mouse_position()

# Клавиатура
agent.type_text("Hello from MIRAI!")
agent.press_key("enter")
agent.press_key("ctrl+c")  # Копировать

# Скриншоты
agent.take_screenshot("full")
agent.take_screenshot("100,100,800,600")  # Область x,y,width,height

# Vision анализ
agent.analyze_screenshot("Что ты видишь на этом скриншоте?")

# OCR
agent.find_text_on_screen("File")

# Computer Vision
agent.find_image_on_screen("button_template.png")

# Окна
agent.find_window("Chrome")
agent.activate_window("Notepad")
agent.open_application("chrome", "https://google.com")

# Ожидание
agent.wait_seconds(2)
```

### Интерактивный режим

```bash
cd mirai-agent
python core/desktop_agent_v2.py
```

Или:

```python
from core.desktop_agent_v2 import main
main()
```

### Примеры задач

```python
# Простые задачи
agent.execute_task("Открой Notepad и напиши 'Hello World'")
agent.execute_task("Сделай скриншот рабочего стола")
agent.execute_task("Найди окно с Chrome и переключись на него")

# Сложные задачи
agent.execute_task(
    "Открой Chrome, перейди на github.com, "
    "найди кнопку Sign In и сделай скриншот"
)

agent.execute_task(
    "Сделай скриншот экрана, проанализируй его, "
    "найди текст 'File' и кликни на нем"
)
```

### История действий

```python
# Получить историю
history = agent.get_action_history(limit=10)

for action in history:
    print(f"{action['action_type']}: {action['result']}")
    print(f"  Длительность: {action['duration']:.3f}с")

# Сохранить в файл
agent.save_action_history("history.json")
```

## 🔒 Безопасность

Desktop Agent включает несколько уровней защиты:

### Rate Limiting
- **Клики**: максимум 60 в минуту
- **Нажатия клавиш**: максимум 300 в минуту
- **Скриншоты**: максимум 30 в минуту

### Запрещенные действия
- Клики в запрещенных зонах экрана (настраивается)
- Запрещенные клавиши (power, sleep)
- Защищенные процессы (System, explorer.exe)

### Fail-safe
- **PyAutoGUI Fail-safe**: двигайте курсор в угол экрана чтобы остановить агента
- **Настройка**: `pyautogui.FAILSAFE = True`

### Отключение безопасности

```python
# ⚠️ Используйте осторожно!
agent = MiraiDesktopAgent(enable_safety=False)
```

## 🧪 Тестирование

```bash
# Запустить все тесты
python test_desktop_agent.py

# Выбрать конкретный тест
python test_desktop_agent.py
# Выберите тест (1-7):
# 1. Базовые операции
# 2. Скриншоты и Vision
# 3. Управление окнами
# 4. OCR
# 5. Автономная задача
# 6. История действий
# 7. Все тесты
```

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────┐
│                  MIRAI Desktop Agent V2                 │
├─────────────────────────────────────────────────────────┤
│  Vision & OCR    │  Input Control  │  Window Manager   │
│  - GPT-4 Vision  │  - Mouse        │  - Find/Activate  │
│  - pytesseract   │  - Keyboard     │  - Resize/Move    │
│  - OpenCV        │  - Hotkeys      │  - List/Monitor   │
├─────────────────────────────────────────────────────────┤
│              Autonomous Decision Engine                 │
│              (GPT-4o + RAG + Memory)                    │
├─────────────────────────────────────────────────────────┤
│        Safety Layer (Limits + Forbidden Actions)        │
└─────────────────────────────────────────────────────────┘
```

### Интеграция с MIRAI Core

Desktop Agent V2 интегрируется с:
- **AutonomousAgent**: для расширенного мышления и планирования
- **BrowserAutomation**: для управления браузером
- **MemoryManager**: для долговременной памяти
- **RAG System**: для контекстного понимания задач

## 📊 Мониторинг

```python
# Получить статистику
print(f"Всего действий: {len(agent.action_history)}")
print(f"Последний скриншот: {agent.last_screenshot_path}")

# Посмотреть последние действия
for action in agent.action_history[-5:]:
    print(f"{action.action_type}: {action.result}")
```

## 🐛 Troubleshooting

### "OpenAI API key не найден"

**Решение:**
1. Создайте файл `mirai-agent/configs/api_keys.json`:
   ```json
   {
     "openai": "sk-your-api-key-here"
   }
   ```
2. Или установите переменную окружения:
   ```bash
   export OPENAI_API_KEY="sk-your-api-key-here"
   ```

### "Playwright не установлен"

Desktop Agent работает и без Playwright, но для полной функциональности:

```bash
pip install playwright
playwright install chromium
```

### "pytesseract не найден" (OCR)

1. Установите Tesseract (см. раздел "Требования")
2. Укажите путь в коде:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### "MIRAI core modules не найдены"

Агент работает и в standalone режиме, но для полной интеграции:

```bash
# Убедитесь что запускаете из правильной директории
cd mirai-agent
python core/desktop_agent_v2.py
```

### На Linux: "Permission denied" или не работает pyautogui

```bash
# Установить зависимости
sudo apt-get install python3-tk python3-dev scrot xdotool

# Добавить в ~/.bashrc
export DISPLAY=:0
```

## 🔮 Roadmap

- [ ] **Поддержка macOS** - полная интеграция с macOS API
- [ ] **Запись макросов** - записывать действия и воспроизводить
- [ ] **Визуальные сценарии** - GUI для создания сценариев
- [ ] **Удаленное управление** - управление через веб-интерфейс
- [ ] **Мультимониторы** - поддержка нескольких экранов
- [ ] **Улучшенный OCR** - EasyOCR, PaddleOCR для лучшего распознавания
- [ ] **Обучение** - учить агента новым действиям
- [ ] **Планировщик** - выполнение задач по расписанию

## 📝 Changelog

### V2.0 (2025-10-24)
- ✨ Полная переработка архитектуры
- ✨ Интеграция с MIRAI Core
- ✨ Добавлен GPT-4 Vision анализ
- ✨ Добавлен OCR (pytesseract)
- ✨ Добавлен Computer Vision (OpenCV)
- ✨ Система безопасности и rate limiting
- ✨ Долговременная память
- ✨ История действий
- ✨ Кроссплатформенность
- 🐛 Исправлены проблемы с окнами на Windows
- 📚 Полная документация

### V1.0 (Initial)
- Базовый функционал pyautogui
- Простое управление окнами
- Базовые скриншоты

## 📄 Лицензия

См. [LICENSE](../LICENSE) в корне проекта.

## 🤝 Контрибьюция

Contributions welcome! См. [CONTRIBUTING.md](../CONTRIBUTING.md)

## 📧 Контакты

- GitHub Issues: https://github.com/AgeeKey/Mirai/issues
- Telegram: @mirai_ai_support

---

**⚠️ ВАЖНО**: Desktop Agent имеет полный контроль над вашим компьютером. Используйте осторожно и всегда включайте `enable_safety=True` при работе с непроверенными задачами.

**🌸 Создано с любовью командой MIRAI**
