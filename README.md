# 🧠 MIRAI - Intelligent Autonomous Desktop Agent

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![OpenAI GPT-4o](https://img.shields.io/badge/OpenAI-GPT--4o%20%2B%20Vision-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-V2%20INTELLIGENT-success.svg)]()
[![Version](https://img.shields.io/badge/version-2.0-orange.svg)]()

**MIRAI** (未来, "Future") - **Полностью автономный AI агент с человеческим интеллектом** для управления компьютером, саморазвития и выполнения сложных задач.

> 🧠 **V2 ПРОРЫВ**: Vision на каждом шаге • Понимание контекста • Умная работа с браузером • Память и обучение

---

## 🎯 ЧТО ТАКОЕ MIRAI V2?

**MIRAI V2** - это **не просто скрипт**, а **умный AI агент**, который:

- 👁️ **ВИДИТ** экран через GPT-4 Vision и **ПОНИМАЕТ** контекст
- 🤔 **ДУМАЕТ** перед каждым действием
- ⚡ **ДЕЙСТВУЕТ** как человек (выбирает профили Chrome, обходит рекламу)
- ✅ **ПРОВЕРЯЕТ** результат каждого действия
- 💾 **ПОМНИТ** всё и **УЧИТСЯ** на опыте
- 🔄 **РАБОТАЕТ** автономно 24/7

### Отличия от обычных автоматизаций:

| Обычный скрипт | MIRAI V2 |
|----------------|----------|
| ❌ Слепо выполняет команды | ✅ Видит и анализирует экран |
| ❌ Не понимает контекст | ✅ Понимает ситуацию (профили, реклама) |
| ❌ Печатает куда попало | ✅ Vision находит правильное поле |
| ❌ Не проверяет результат | ✅ Проверяет после каждого действия |
| ❌ Нет памяти | ✅ Помнит всё, учится на ошибках |

---

## 📖 Содержание

- [История: V1 → V2](#-история-v1--v2)
- [Архитектура V2](#-архитектура-v2)
- [5 Ключевых Компонентов](#-5-ключевых-компонентов)
- [Как Работает Vision](#-как-работает-vision)
- [Безопасность и Защита](#-безопасность-и-защита)
- [Быстрый Старт](#-быстрый-старт)
- [Использование](#-использование)
- [Сравнение V1 vs V2](#-сравнение-v1-vs-v2)
- [Устранение Проблем](#-устранение-проблем)

---

## 📜 История: V1 → V2

### ❌ V1 - Критический Провал

**Что было не так:**

- **Слепое выполнение**: Печатал команды в терминале вместо текстовых редакторов
- **Нет контекста**: Не видел диалоги выбора профиля Chrome
- **Игнорировал проблемы**: Не замечал рекламу и всплывающие окна
- **Не проверял результат**: Никогда не понимал, сработало действие или нет
- **Вызвал краш системы**: 6 процессов Python работали одновременно → чёрный экран → перезагрузка

**Оценка пользователя: 1/10** ⭐

### ✅ V2 - Прорыв с Vision Intelligence

**Что изменилось:**

✅ **Видит экран** через GPT-4 Vision перед каждым действием  
✅ **Понимает контекст** (профили, реклама, состояние приложений)  
✅ **Умная работа с Chrome** (выбор профиля, обход рекламы)  
✅ **Проверка результатов** (сравнение до/после через Vision)  
✅ **Память и обучение** (помнит ошибки, извлекает уроки)  
✅ **Система безопасности** (FAILSAFE, лимит действий, аварийная остановка)

**Результат: Полностью автономный агент с человеческим интеллектом** 🧠

---

## 🏗️ Архитектура V2

```plaintext
┌─────────────────────────────────────────────────────────────────────┐
│                    MIRAI V2 - Intelligent Desktop Agent             │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ autonomous_desktop_v2.py │
                    │  IntelligentMiraiAgent   │
                    └────────────┬─────────────┘
                                 │
        ┌───────────┬────────────┼────────────┬───────────┐
        │           │            │            │           │
   ┌────▼────┐ ┌───▼─────┐ ┌────▼─────┐ ┌───▼──────┐ ┌─▼──────┐
   │ Vision  │ │ Context │ │  Smart   │ │  Smart   │ │ OpenAI │
   │  Tools  │ │ Manager │ │ Desktop  │ │ Browser  │ │GPT-4o  │
   └─────────┘ └─────────┘ └──────────┘ └──────────┘ └────────┘
       │            │            │            │            │
   GPT-4 Vision  Memory      pyautogui    Chrome      Decisions
   Анализ экрана  История    Клавиатура   Профили     Задачи
```

### Цикл Работы Агента

```plaintext
1️⃣ ANALYZE (Анализ)
   └─> Vision делает скриншот + GPT-4 Vision анализирует ситуацию

2️⃣ CHOOSE (Выбор Задачи)
   └─> GPT-4o с контекстом решает, что делать дальше

3️⃣ PLAN (Планирование)
   └─> Создаёт детальный план действий (шаг за шагом)

4️⃣ EXECUTE (Выполнение)
   └─> Каждый шаг: Vision → Действие → Vision проверка

5️⃣ LEARN (Обучение)
   └─> Извлекает уроки из цикла, сохраняет в память

   [Пауза 60 секунд]

   ↻ Повтор цикла (макс 10 действий за цикл)
```

---

## 🔧 5 Ключевых Компонентов

### 1️⃣ vision_tools.py - Глаза Агента

**Назначение:** Интеграция GPT-4 Vision для понимания экрана

**Ключевые методы:**

```python
# Полный анализ экрана
context = vision_tools.analyze_screen_context(
    screenshot="vision_20251024.png",
    question="Какие приложения открыты?"
)
# Возвращает: scene_description, detected_elements, ui_state, recommendations

# Поиск элемента на экране
location = vision_tools.find_element_on_screen(
    screenshot="screen.png",
    element_description="Кнопка 'Сохранить'"
)
# Возвращает: type, label, location (верх-лево, центр и т.д.)

# Проверка результата действия
result = vision_tools.verify_action_result(
    before_screenshot="before.png",
    after_screenshot="after.png",
    expected_action="Открыл Блокнот"
)
# Возвращает: success=True/False, changes_detected, description

# Обнаружение проблем
problems = vision_tools.detect_problems(screenshot="screen.png")
# Возвращает: has_problems, problem_types [ads, errors, popups]
```

**Технологии:** OpenAI Vision API, base64 кодирование, JSON парсинг

---

### 2️⃣ context_manager.py - Память Агента

**Назначение:** Отслеживание всех действий, состояний, проблем

**Структуры данных:**

```python
@dataclass
class ActionRecord:
    timestamp: str
    action_type: str  # "open_app", "type_text", "click", "browser"
    description: str
    status: ActionStatus  # SUCCESS, FAILED, PARTIAL, SKIPPED
    problems_found: List[str]
    screenshot_before: str
    screenshot_after: str

@dataclass  
class ApplicationState:
    name: str
    is_open: bool
    last_action: str
    success_rate: float

@dataclass
class BrowserState:
    profile_name: str
    current_url: str
    ads_encountered: int
    popups_closed: int
```

**Ключевые методы:**

```python
# Записать действие
context.record_action(
    action_type="type_text",
    description="Напечатал 'Hello'",
    status=ActionStatus.SUCCESS
)

# Обновить состояние браузера
context.update_browser_state(
    profile="Work", 
    url="google.com",
    ads_closed=2
)

# Сохранить всё в JSON
context.save_to_file("context_20251024.json")

# Статистика
stats = context.get_statistics()
# Возвращает: total_actions, success_rate, problems_count, apps_used
```

---

### 3️⃣ smart_browser_agent.py - Умная Работа с Chrome

**Назначение:** Chrome с пониманием профилей, рекламы, всплывающих окон

**Ключевые методы:**

```python
# Умное открытие Chrome
browser.open_chrome_smart(
    url="https://google.com",
    profile_name="Work"  # Vision найдёт профиль!
)

# Внутри: Vision анализирует диалог выбора профиля
# → Находит нужный профиль → Кликает правильное место

# Умный поиск Google
browser.google_search_smart(query="Python tutorials")
# → Vision находит поле поиска
# → Кликает правильное место
# → Печатает текст
# → Vision проверяет результат

# Навигация с проверкой
browser.navigate_to_url("https://example.com")
# → Vision проверяет загрузку страницы
# → Обнаруживает рекламу/попапы
# → Автоматически закрывает их
```

**Решённые проблемы V1:**

- ✅ Видит диалоги выбора профиля Chrome
- ✅ Находит кнопки профилей через Vision
- ✅ Автоматически закрывает рекламу
- ✅ Обрабатывает всплывающие окна

---

### 4️⃣ smart_desktop_agent.py - Vision-управление рабочим столом

**Назначение:** Умные действия с проверкой через Vision

**Ключевые методы:**

```python
# Умное открытие приложения
desktop.smart_open_application("Notepad")
# → Скриншот ДО
# → Win+S → Поиск → Enter
# → Скриншот ПОСЛЕ
# → Vision проверяет: открылся ли Блокнот?

# Умный ввод текста
desktop.smart_type_text("Hello World")
# → Vision анализирует экран: "Где текстовое поле?"
# → Vision говорит: "Центр экрана, текстовое поле активно"
# → Кликает правильное место
# → Печатает текст
# → Vision проверяет: появился ли текст?

# Умный клик
desktop.smart_click("Кнопка Сохранить")
# → Vision находит элемент на экране
# → Определяет координаты
# → Кликает
# → Vision проверяет изменения

# Анализ текущей ситуации
situation = desktop.analyze_current_situation()
# Возвращает полный Vision-анализ рабочего стола
```

**Решённые проблемы V1:**

- ✅ НЕ печатает в терминале вместо редактора
- ✅ Vision находит правильное текстовое поле
- ✅ Проверяет результат каждого действия

---

### 5️⃣ autonomous_desktop_v2.py - Оркестратор с Интеллектом

**Назначение:** Главный агент, объединяющий все компоненты

**Цикл intelligent_cycle():**

```python
async def intelligent_cycle(self):
    # 1. ANALYZE - Vision анализ экрана
    situation = await self.desktop.analyze_current_situation()
    
    # 2. CHOOSE - GPT-4o выбирает задачу с учётом контекста
    task = self._choose_intelligent_task(situation)
    
    # 3. PLAN - Создаёт детальный план
    plan = self._create_intelligent_plan(task, situation)
    
    # 4. EXECUTE - Выполняет план с Vision на каждом шаге
    for step in plan:
        # Vision ДО действия
        result = await self._execute_step(step)
        # Vision ПОСЛЕ действия
        self.context.record_action(result)
        
        if self.actions_in_cycle >= self.max_actions_per_cycle:
            break  # Лимит безопасности
    
    # 5. LEARN - Извлекает уроки
    lessons = self._analyze_and_learn()
    
    # Пауза 60 секунд
    await asyncio.sleep(60)
```

**Система безопасности:**

```python
# Защита от зацикливания
max_actions_per_cycle = 10  # Не больше 10 действий за цикл

# Emergency stop
pyautogui.FAILSAFE = True  # Курсор в угол = STOP

# Обработка Ctrl+C
try:
    await intelligent_cycle()
except KeyboardInterrupt:
    print("🛑 Агент остановлен пользователем")

---

```

---

## 👁️ Как Работает Vision

### Процесс Vision-анализа

1. **Захват скриншота**

```python
screenshot_path = f"vision_{timestamp}.png"
pyautogui.screenshot(screenshot_path)
```

2. **Кодирование в base64**

```python
with open(screenshot_path, "rb") as f:
    base64_image = base64.b64encode(f.read()).decode('utf-8')
```

3. **Отправка в GPT-4 Vision**

```python
response = openai.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Проанализируй экран..."},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_image}",
                "detail": "high"  # Высокая детализация
            }}
        ]
    }],
    temperature=0.5
)
```

4. **Парсинг JSON-ответа**

```python
vision_result = json.loads(response.choices[0].message.content)
{
    "scene_description": "Открыт рабочий стол Windows...",
    "detected_elements": [
        {"type": "window", "label": "Chrome", "location": "center"},
        {"type": "button", "label": "Profile 1", "location": "top-left"}
    ],
    "ui_state": {
        "active_application": "Chrome",
        "possible_actions": ["click_profile", "close_window"]
    },
    "recommendations": "Выбрать профиль 'Work' в верхнем левом углу"
}
```

### Примеры Vision-анализа

**Пример 1: Обнаружение диалога выбора профиля Chrome**

```text
📸 Screenshot captured
🧠 Vision Analysis:
   Scene: "Chrome profile selection dialog with 3 profiles visible"
   Elements: 
     - Button "Work Profile" (top-left)
     - Button "Personal" (top-center)  
     - Button "Guest" (top-right)
   Recommendation: "Click on 'Work Profile' button"
```

**Пример 2: Поиск текстового поля**

```text
📸 Screenshot captured
🧠 Vision Analysis:
   Scene: "Notepad window is open with blank document"
   Elements:
     - TextArea "Main text field" (center, large white area)
     - Menu "File" (top-left)
   Active Element: "Text field is focused and ready for input"
```

**Пример 3: Обнаружение рекламы**

```text
📸 Screenshot captured  
🧠 Vision Analysis:
   Problems Detected: YES
   Problem Types: ["ads", "popup"]
   Description: "Advertisement banner at top of page with close button"
   Recommendation: "Click X button in top-right corner of ad"
```

---

## 🛡️ Безопасность и Защита

### Система Безопасности

| Защита | Описание | Реализация |
|--------|----------|------------|
| **FAILSAFE** | Курсор в угол → STOP | `pyautogui.FAILSAFE = True` |
| **Лимит действий** | Макс 10 действий за цикл | `max_actions_per_cycle = 10` |
| **Пауза между циклами** | 60 секунд отдыха | `await asyncio.sleep(60)` |
| **Ctrl+C обработка** | Graceful shutdown | `except KeyboardInterrupt` |
| **Тестовый режим** | Один цикл и остановка | `test_one_cycle.py` |
| **Vision проверка** | Каждое действие проверено | Before + After screenshots |

### Как Остановить Агента

**Метод 1: FAILSAFE (Аварийная остановка)**

```text
Переместите курсор мыши в ЛЕВЫЙ ВЕРХНИЙ УГОЛ экрана
→ pyautogui автоматически выбросит исключение
→ Агент остановится
```

**Метод 2: Ctrl+C**

```text
Нажмите Ctrl+C в терминале
→ KeyboardInterrupt перехвачен
→ Graceful shutdown с сохранением контекста
```

**Метод 3: Закрыть окно терминала**

```text
Закройте окно PowerShell/CMD
→ Процесс Python завершится
```

### Защита от Проблем V1

| Проблема V1 | Защита V2 |
|-------------|-----------|
| 6 процессов → краш | Тестовый режим (1 цикл) |
| Печатал в терминале | Vision находит правильное поле |
| Бесконечный цикл | Лимит 10 действий + пауза 60 сек |
| Нет контекста | Vision анализ перед действием |
| Не видел профили Chrome | Vision детектит диалоги |

---

## 🚀 Быстрый Старт

### Шаг 1: Требования

```text
- Windows 10/11
- Python 3.13+
- OpenAI API Key (с доступом к GPT-4 Vision)
- Google Chrome установлен
```

### Шаг 2: Установка

```powershell
cd F:\Mirai\mirai-agent

# Создать виртуальное окружение
python -m venv venv

# Активировать
.\venv\Scripts\activate

# Установить зависимости
pip install openai pillow pyautogui
```

### Шаг 3: Настройка API Key

Создайте файл `configs/api_keys.json`:

```json
{
    "openai_api_key": "sk-your-openai-api-key-here"
}
```

### Шаг 4: Тестовый Запуск (БЕЗОПАСНО)

```powershell
# Запустить ОДИН цикл (для теста)
python test_one_cycle.py
```

**Что произойдёт:**

1. Агент сделает скриншот рабочего стола
2. GPT-4 Vision проанализирует ситуацию
3. GPT-4o выберет задачу (например, "открыть Chrome")
4. Создаст план
5. Выполнит план с Vision-проверками
6. Покажет статистику
7. **ОСТАНОВИТСЯ** (не будет бесконечно работать)

### Шаг 5: Полный Запуск (24/7 режим)

**ВНИМАНИЕ:** Полный режим работает бесконечно!

```powershell
# Запустить непрерывный режим
python autonomous_desktop_v2.py
```

**Или через BAT файл:**

```powershell
.\START_INTELLIGENT_MIRAI.bat
```

---

## 💻 Использование

### Режим 1: Тестовый (Рекомендуется для начала)

```powershell
python test_one_cycle.py

### 5-Minute Setup

```bash
# 1. Clone repository
git clone https://github.com/AgeeKey/Mirai.git
cd Mirai

# 2. Set API key
export OPENAI_API_KEY="sk-..."

# 3. Run health check
./scripts/healthcheck.sh

# 4. Launch MIRAI
python3 mirai.py --mode terminal
```

### Available Modes

```bash
# Interactive terminal (KAIZEN)
python3 mirai.py --mode terminal

# Web dashboard
python3 mirai.py --mode dashboard

# Background autonomous mode
python3 mirai.py --mode autonomous

# Ask MIRAI a question
python3 mirai.py --mode ask --query "What are your capabilities?"

# Display version
python3 mirai.py --version

# Run health check
python3 mirai.py --health
```

---

## 📦 Installation

### Prerequisites

- **Python 3.10+** (tested on 3.12.3)
- **OpenAI API Key**
- **Git**
- **10GB+ disk space**

### Step 1: Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
```

**macOS:**
```bash
brew install python@3.12 git
```

### Step 2: Clone Repository

```bash
git clone https://github.com/AgeeKey/Mirai.git
cd Mirai
```

### Step 3: Create Virtual Environment

```bash
cd mirai-agent
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Key packages:**
- `openai>=1.0.0` - OpenAI API client
- `pyyaml>=6.0` - Configuration parsing
- `rich>=13.0.0` - Terminal UI
- `flask>=3.0.0` - Web dashboard
- `prometheus-client>=0.19.0` - Metrics

### Step 5: Configure API Key

**Option 1: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY="sk-..."

# Make persistent
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.bashrc
```

**Option 2: Config File**
```bash
# Create/edit configs/api_keys.json
{
    "openai_api_key": "sk-..."
}
```

### Step 6: Verify Installation

```bash
# Run health check
cd /path/to/Mirai
./scripts/healthcheck.sh

# Should show:
# ✅ Python 3.12.3
# ✅ MIRAI Installation Found
# ✅ API Key Set (env)
# ✅ Config v2.0.0
# ✅ Memory DB Initialized
# ✅ Logger Ready
# ✅ Core Modules All importable
# ✅ Dependencies All installed
# ✅ Disk Space Available
#
# 🎉 All systems operational!
```

---

## ⚙️ Configuration

### Configuration File

MIRAI uses a unified YAML configuration file: `configs/mirai.yaml`

**Structure:**
```yaml
version: "2.0.0"

openai:
  models:
    default: "gpt-4o-mini"
    heavy: "gpt-4o"
    fast: "gpt-3.5-turbo"
    embeddings: "text-embedding-3-large"
  
  temperature: 0.3
  max_tokens: 4000
  timeout: 60

memory:
  backend: "sqlite"
  database_path: "data/mirai_memory.db"
  retention_days: 90
  short_term_messages: 12

logging:
  level: "INFO"
  format: "json"
  rotation:
    max_bytes: 10485760  # 10MB
    backup_count: 5
```

### Environment Variables

```bash
# Required
export OPENAI_API_KEY="sk-..."

# Optional
export MIRAI_CONFIG_PATH="/custom/path/to/mirai.yaml"
export MIRAI_LOG_LEVEL="DEBUG"
export MIRAI_DATA_DIR="/custom/data/path"
```

### Loading Configuration

```python
from core.config_loader import get_config

# Get full config
config = get_config()

# Access with dot notation
print(config.openai.models.default)  # "gpt-4o-mini"
print(config.memory.retention_days)  # 90

# Get API key
from core.config_loader import get_api_key
api_key = get_api_key()

# Get specific model config
from core.config_loader import get_openai_model_config
model_config = get_openai_model_config("heavy")
print(model_config.model)  # "gpt-4o"
```

---

## 💻 Usage

### 1. Terminal Mode (Interactive)

```bash
python3 mirai.py --mode terminal
```

**Available Commands:**
```
help              Show available commands
status            Show system status
memory            Show memory statistics
ask <question>    Ask KAIZEN a question
analyze <topic>   Analyze code/project
improve <file>    Get improvement suggestions
task <action>     Manage tasks (list/add/complete)
health            Run health check
clear             Clear screen
exit              Exit terminal
```

**Example Session:**
```
🤖 KAIZEN Terminal v2.0.0

kaizen> ask What are your capabilities?
🤖 KAIZEN: I can help with:
- Code analysis and improvement
- Task management
- GitHub integration
- Multi-language execution
- Memory and learning
[...]

kaizen> memory
📊 Memory Statistics:
- Total sessions: 5
- Messages stored: 142
- Preferences: 8
- Tasks: 3 active
- Knowledge entries: 27

kaizen> exit
```

### 2. Dashboard Mode (Web UI)

```bash
python3 mirai.py --mode dashboard
```

Then open: `http://localhost:5000`

**Dashboard Features:**
- Real-time system health
- Memory statistics
- Recent sessions
- Task list
- Prometheus metrics at `/metrics`
- Health API at `/api/health`

### 3. Autonomous Mode (Background)

```bash
# Start autonomous service
python3 mirai.py --mode autonomous

# Or use systemd
sudo systemctl start mirai
```

**What it does:**
- Monitors GitHub CI/CD
- Analyzes code quality
- Proposes improvements
- Learns from feedback
- Logs to `/tmp/kaizen_mirai.log`

### 4. Ask Mode (One-off Query)

```bash
python3 mirai.py --mode ask --query "Analyze the memory manager code"
```

**Output:**
```
🌸 MIRAI Analysis:

The memory manager implementation is well-structured with:
✅ Type-safe dataclasses
✅ Proper indexing on sessions
✅ RAG-ready embeddings
⚠️ Consider adding connection pooling
⚠️ Add cleanup job for old sessions
[...]
```

---

## 🏥 Health Monitoring

### Health Check Script

**Location:** `scripts/healthcheck.sh`

**Run health check:**
```bash
./scripts/healthcheck.sh
```

**Output:**
```
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Health Check                                                 ║
╚══════════════════════════════════════════════════════════════════════╝

  ✅ Python                    3.12.3
  ✅ MIRAI Installation        Found
  ✅ API Key                   Set (env)
  ✅ Config                    v2.0.0
  ✅ Memory DB                 Initialized (32K)
  ✅ Logger                    Ready
  ✅ Core Modules              All importable
  ✅ Dependencies              All installed
  ✅ Disk Space                34G available

──────────────────────────────────────────────────────────────────────
Summary: 9/9 checks passed

🎉 All systems operational!
```

### Output Formats

**JSON (for monitoring tools):**
```bash
./scripts/healthcheck.sh --json
```

```json
{
    "status": "healthy",
    "timestamp": "2025-10-14T13:20:29+00:00",
    "total_checks": 9,
    "passed_checks": 9,
    "failed_checks": 0,
    "checks": [...]
}
```

**Quiet (for automation):**
```bash
./scripts/healthcheck.sh --quiet
echo $?  # 0 = healthy, 1 = unhealthy
```

### Integration Examples

**Systemd:**
```ini
[Service]
ExecStartPre=/root/mirai/scripts/healthcheck.sh --quiet
ExecStart=/root/mirai/mirai.py --mode autonomous
```

**Cron:**
```bash
*/5 * * * * /root/mirai/scripts/healthcheck.sh --json > /tmp/mirai_health.json
```

**Docker:**
```dockerfile
HEALTHCHECK --interval=30s CMD /scripts/healthcheck.sh --quiet || exit 1
```

---

## 📊 Dashboard

### Starting the Dashboard

```bash
python3 mirai.py --mode dashboard
```

**Access:** http://localhost:5000

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard |
| `/api/health` | GET | Health status (JSON) |
| `/api/memory/stats` | GET | Memory statistics |
| `/api/sessions` | GET | Recent sessions |
| `/api/tasks` | GET | Active tasks |
| `/metrics` | GET | Prometheus metrics |

### API Examples

**Health Check:**
```bash
curl http://localhost:5000/api/health | jq
```

**Memory Stats:**
```bash
curl http://localhost:5000/api/memory/stats | jq
```

**Prometheus Metrics:**
```bash
curl http://localhost:5000/metrics
```

---

## 🧠 Memory System

### Overview

MIRAI uses a SQLite-based memory system with 5 tables:
- **sessions** - Conversation sessions
- **messages** - All messages (user + AI)
- **user_preferences** - Learned preferences
- **tasks** - Task tracking
- **knowledge** - RAG knowledge base

### Usage

```python
from core.memory_manager import MemoryManager

# Initialize
mm = MemoryManager()

# Create session
session_id = mm.create_session(user_id="user123")

# Add message
mm.add_message(
    session_id=session_id,
    role="user",
    content="Hello MIRAI",
    tokens_used=5
)

# Get recent messages
messages = mm.get_recent_messages(session_id, limit=10)

# Set preference
mm.set_user_preference(
    user_id="user123",
    preference_key="language",
    preference_value="Python"
)

# Get preferences
prefs = mm.get_user_preferences("user123")

# Add task
task_id = mm.add_task(
    session_id=session_id,
    description="Implement health check",
    status="completed"
)

# Add knowledge
mm.add_knowledge(
    session_id=session_id,
    topic="Health Monitoring",
    content="Health checks validate system components",
    embedding=[0.1, 0.2, ...]  # Optional vector
)
```

### Memory Statistics

```python
# Get stats
stats = mm.get_memory_stats()

print(stats)
# {
#     'total_sessions': 5,
#     'total_messages': 142,
#     'total_preferences': 8,
#     'total_tasks': 12,
#     'total_knowledge': 27
# }
```

---

## 📝 Logging

### Overview

MIRAI uses structured JSON logging with rotation and custom fields.

### Usage

```python
from core.logger import MiraiLogger

# Initialize
logger = MiraiLogger(name="my_module")

# Basic logging
logger.info("System started")
logger.warning("High memory usage", extra={"memory_mb": 512})
logger.error("API call failed", extra={"error_code": 500})

# Operation context (auto-timing)
with logger.operation("database_query"):
    result = db.query()

# AI call logging (auto-timing + token tracking)
with logger.ai_call(model="gpt-4o", prompt="Hello"):
    response = client.chat.completions.create(...)

# MIRAI-specific methods
logger.log_ai_request(
    model="gpt-4o-mini",
    prompt="Analyze code",
    temperature=0.3
)

logger.log_ai_response(
    model="gpt-4o-mini",
    response="Analysis complete",
    tokens_used=150,
    latency_ms=1200
)

logger.log_task(
    task_id="task_123",
    action="started",
    description="Health check implementation"
)
```

### Log Format

**JSON (rotating file):**
```json
{
    "timestamp": "2025-10-14T13:20:29.123Z",
    "level": "INFO",
    "logger": "core.memory_manager",
    "message": "Session created",
    "session_id": "sess_abc123",
    "user_id": "user456",
    "model": "gpt-4o-mini",
    "tokens": 150,
    "latency_ms": 1200
}
```

**Console (colored):**
```
2025-10-14 13:20:29 INFO  [core.memory_manager] Session created
```

### Log Location

- **Service logs:** `/tmp/kaizen_mirai.log`
- **Metrics:** `/tmp/kaizen_mirai_metrics.jsonl`
- **Rotation:** 10MB max, 5 backups

---

## 🛠️ Development

### Project Structure

```
mirai/
├── mirai.py                 # Unified entry point
├── configs/
│   ├── mirai.yaml          # Main configuration
│   └── api_keys.json       # API keys (git-ignored)
├── core/
│   ├── config_loader.py    # Configuration management
│   ├── memory_manager.py   # Memory system
│   └── logger.py           # Logging system
├── mirai-agent/
│   ├── core/
│   │   ├── autonomous_agent.py
│   │   ├── github_integration.py
│   │   ├── database_manager.py
│   │   └── multi_language_executor.py
│   ├── kaizen_terminal.py  # Terminal UI
│   ├── dashboard_server.py # Web dashboard
│   └── autonomous_service.py
├── scripts/
│   └── healthcheck.sh      # Health monitoring
├── data/                   # SQLite databases
├── tests/                  # Unit tests
└── docs/                   # Documentation
```

### Coding Standards

**Python Style:**
- PEP 8 compliance
- Type hints for all functions
- Docstrings (Google style)
- Async/await for I/O

**Example:**
```python
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration for MIRAI component."""
    name: str
    enabled: bool
    timeout: int = 30

async def process_request(
    user_id: str,
    query: str,
    model: str = "gpt-4o-mini"
) -> Dict[str, any]:
    """
    Process user request with AI.
    
    Args:
        user_id: Unique user identifier
        query: User's question
        model: OpenAI model to use
        
    Returns:
        Response dictionary with answer and metadata
    """
    # Implementation
    pass
```

### Adding New Features

**1. Create feature branch:**
```bash
git checkout -b feature/my-feature
```

**2. Implement with tests:**
```python
# my_feature.py
def my_function(arg: str) -> str:
    """My new feature."""
    return arg.upper()

# tests/test_my_feature.py
def test_my_function():
    assert my_function("hello") == "HELLO"
```

**3. Run tests:**
```bash
pytest tests/
```

**4. Update documentation:**
```bash
# Update README.md or docs/
```

**5. Submit PR:**
```bash
git add .
git commit -m "feat: add my feature"
git push origin feature/my-feature
```

---

## 🧪 Testing

### Running Tests

**All tests:**
```bash
cd mirai-agent
source venv/bin/activate
pytest tests/ -v
```

**Specific test file:**
```bash
pytest tests/test_memory_manager.py -v
```

**With coverage:**
```bash
pytest tests/ --cov=core --cov-report=html
```

### Test Structure

```
tests/
├── test_config_loader.py      # Config tests
├── test_memory_manager.py     # Memory tests
├── test_logger.py             # Logger tests
├── test_health_check.py       # Health check tests
└── integration/
    └── test_full_workflow.py  # Integration tests
```

### Writing Tests

```python
import pytest
from core.memory_manager import MemoryManager

def test_create_session():
    """Test session creation."""
    mm = MemoryManager(db_path=":memory:")
    session_id = mm.create_session(user_id="test_user")
    
    assert session_id is not None
    assert session_id.startswith("sess_")

def test_add_message():
    """Test adding message."""
    mm = MemoryManager(db_path=":memory:")
    session_id = mm.create_session(user_id="test_user")
    
    mm.add_message(
        session_id=session_id,
        role="user",
        content="Test message",
        tokens_used=5
    )
    
    messages = mm.get_recent_messages(session_id)
    assert len(messages) == 1
    assert messages[0].content == "Test message"
```

---

## 📚 Documentation

### Phase 0: Vision & Planning Documents

📂 **[docs/](./docs/)** - Comprehensive Phase 0 documentation (85 pages, ~49k words)

| Document | Description | Pages |
|----------|-------------|-------|
| **[docs/README.md](./docs/README.md)** | Documentation index and navigation | 11 |
| **[docs/VISION_AND_SCOPE.md](./docs/VISION_AND_SCOPE.md)** | Project vision, scope, goals, constraints | 6 |
| **[docs/USE_CASES.md](./docs/USE_CASES.md)** | 20 prioritized use cases (P0/P1/P2) | 12 |
| **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)** | Logical system architecture | 14 |
| **[docs/DEVELOPMENT_ROADMAP.md](./docs/DEVELOPMENT_ROADMAP.md)** | 5-phase development plan (9-16 months) | 18 |
| **[docs/RISK_MATRIX.md](./docs/RISK_MATRIX.md)** | Risk assessment & mitigation (12 risks) | 11 |
| **[docs/HIRING_PLAN.md](./docs/HIRING_PLAN.md)** | Team structure & hiring (10→100 people) | 13 |
| **[docs/POC_GUIDE.md](./docs/POC_GUIDE.md)** | Technical PoC implementation guide | 11 |

👉 **Start here:** [docs/README.md](./docs/README.md) for navigation by role

### Implementation Documentation

| Document | Description |
|----------|-------------|
| `README.md` | Main documentation (this file) |
| `MASTER_PLAN.md` | 4-phase development roadmap |
| `PHASE1_WEEK1_PRIORITY*_COMPLETED.md` | Implementation reports |
| `MIRAI_ARCHITECTURE_EXPLAINED.md` | Architecture deep-dive |
| `COPILOT_GUIDE.md` | GitHub Copilot instructions |
| `.github/copilot-instructions.md` | AI coding standards |

### Architecture Documents

- **MIRAI_ARCHITECTURE_EXPLAINED.md** - System architecture
- **NASA_LEVEL_ARCHITECTURE_PLAN.md** - Advanced features
- **MIRAI_CAPABILITIES.txt** - Full capability list
- **docs/ARCHITECTURE.md** - Logical architecture (Phase 0)

### API Documentation

Generate API docs:
```bash
cd mirai-agent
pdoc --html core/ --output-dir docs/api
```

View at: `docs/api/index.html`

---

## 🤝 Contributing

We welcome contributions! Here's how:

### 1. Fork Repository

```bash
git clone https://github.com/YOUR_USERNAME/Mirai.git
cd Mirai
```

### 2. Create Feature Branch

```bash
git checkout -b feature/amazing-feature
```

### 3. Make Changes

- Follow coding standards
- Add tests
- Update documentation

### 4. Run Tests

```bash
pytest tests/
./scripts/healthcheck.sh
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add amazing feature"
```

**Commit message format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring

### 6. Push and Create PR

```bash
git push origin feature/amazing-feature
```

Then open Pull Request on GitHub.

### Code Review Process

1. Automated tests run on PR
2. Code review by maintainers
3. Required: All tests pass
4. Required: Documentation updated
5. Merge when approved

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - GPT-4o and API
- **Rich** - Beautiful terminal UI
- **Flask** - Web framework
- **SQLite** - Embedded database

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/AgeeKey/Mirai/issues)
- **Discussions:** [GitHub Discussions](https://github.com/AgeeKey/Mirai/discussions)
- **Email:** support@mirai-ai.dev

---

## 🗺️ Roadmap

### ✅ Phase 1: Foundation (Weeks 1-2)
- [x] Unified entry point
- [x] Configuration system
- [x] Memory manager
- [x] Structured logging
- [x] Health monitoring
- [ ] README documentation (in progress)
- [ ] Systemd integration
- [ ] CI/CD pipeline

### 🔄 Phase 2: Intelligence (Weeks 3-4)
- [ ] Cognitive loop (analyze → plan → execute → reflect)
- [ ] Ethical filter
- [ ] Self-registry
- [ ] Advanced RAG
- [ ] Multi-model orchestration

### 🎯 Phase 3: Trading (Months 2-3)
- [ ] Market data integration
- [ ] Strategy backtesting
- [ ] Risk management
- [ ] Paper trading
- [ ] Live trading (careful!)

### 🚀 Phase 4: Evolution (Month 3+)
- [ ] Self-improvement loop
- [ ] Code generation
- [ ] Automated testing
- [ ] Performance optimization
- [ ] Multi-agent collaboration

---

## 📊 Status

**Version:** 2.0.0  
**Status:** Active Development  
**Last Updated:** October 14, 2025

**Progress:**
- Phase 1: 80% (4/5 priorities complete)
- Phase 2: 0%
- Phase 3: 0%
- Phase 4: 0%

---

**Built with 🤖 KAIZEN and 🌸 MIRAI**