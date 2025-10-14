# 🚀 MIRAI: Unified Master Plan

**Дата начала:** 2025-10-14  
**Статус:** 🟢 В работе  
**Цель:** Создать production-ready AI систему с интеллектом MIRAI и надёжностью enterprise

---

## 📋 Объединённый План (MIRAI 🌸 + Production 🔥)

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  🌸 MIRAI Intelligence  +  🔥 Production Reliability             │
│     (ЧТО нужно AI)          (КАК внедрить безопасно)            │
│                                                                  │
│         Memory                    Monitoring                     │
│         IoT/API                   Tests/CI                       │
│         Self-evolution            Security                       │
│         NLP                       Architecture                   │
│                                                                  │
│                    = 🚀 MIRAI v2.0                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Phase 1: Foundation (0-2 недели) — НАЧИНАЕМ СЕЙЧАС!

### ✅ Week 1 (Дни 1-7):

#### 🔴 Приоритет 1: Единая Точка Входа

**Задача:** Создать `mirai.py` — единый CLI для всех режимов

**Файлы:**
- [ ] `mirai.py` — главный entry point
- [ ] `configs/mirai.yaml` — единый конфиг
- [ ] Обновить systemd services

**Критерий готовности:**
```bash
python3 mirai.py --mode terminal   # запускает kaizen_terminal
python3 mirai.py --mode dashboard  # запускает dashboard_server
python3 mirai.py --mode autonomous # запускает autonomous_service
python3 mirai.py --mode ask "вопрос" # разовый вопрос
python3 mirai.py --version         # версия и метаданные
```

---

#### 🔴 Приоритет 2: Конфигурация (MIRAI 🌸 + Production 🔥)

**Задача:** Единый конфиг для всех компонентов

**Файл:** `configs/mirai.yaml`

**Структура:**
```yaml
# MIRAI Unified Config
version: "2.0.0"
name: "MIRAI AI Agent"
description: "Autonomous AI Agent with Memory and Self-Evolution"

# OpenAI Config (Production-Grade)
openai:
  defaults:
    timeout_s: 90
    max_retries: 4
    backoff:
      base_ms: 200
      max_ms: 8000
      jitter: true
  
  models:
    main:           # 70% задач (MIRAI рекомендовала)
      name: gpt-4o-mini
      temperature: 0.25
      top_p: 0.9
      max_tokens: 2000
    
    heavy:          # 25% задач (MIRAI хотела GPT-4o)
      name: gpt-4o
      temperature: 0.25
      top_p: 0.9
      max_tokens: 2500
    
    fast:           # 5% задач (фильтрация)
      name: gpt-3.5-turbo
      temperature: 0.2
      max_tokens: 1200
    
    embed:          # RAG и память
      name: text-embedding-3-large
      timeout_s: 30

# Memory (MIRAI хочет!)
memory:
  enabled: true
  backend: "sqlite"
  db_path: "data/mirai_memory.db"
  session_storage: "data/sessions/"
  
  short_term:
    max_messages: 12  # Production лимит
    ttl_hours: 24
  
  long_term:
    enabled: true
    retention_days: 90
    backup_enabled: true

# Monitoring (Production требование)
monitoring:
  enabled: true
  logs:
    path: "/tmp/mirai.log"
    level: "INFO"
    format: "json"
  
  metrics:
    enabled: true
    provider: "prometheus"
    port: 9090
  
  healthcheck:
    enabled: true
    interval_seconds: 60

# Circuit Breaker (Production безопасность)
circuit_breaker:
  enabled: true
  failure_threshold: 5
  timeout_s: 60
  half_open_interval_s: 30

# Self-Evolution (MIRAI хочет!)
self_evolution:
  enabled: false  # Включим в Phase 3
  sandbox: true
  auto_apply: false
  review_required: true

# Ethical Filter (MIRAI + Production)
ethical_filter:
  enabled: true
  strict_mode: true
  block_malicious: true
  log_all_requests: true

# Services
services:
  terminal:
    enabled: true
    port: null
  
  dashboard:
    enabled: true
    port: 5000
    host: "0.0.0.0"
  
  autonomous:
    enabled: true
    interval_minutes: 5
    max_iterations: 10
```

---

#### 🟡 Приоритет 3: Долгосрочная Память (MIRAI топ-1! 🌸)

**Задача:** Реализовать базовую долгосрочную память

**Файлы:**
- [ ] `core/memory_manager.py` — менеджер памяти
- [ ] `data/mirai_memory.db` — SQLite база
- [ ] Интеграция в `autonomous_agent.py`

**Схема БД:**
```sql
-- Sessions (сессии)
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    user_id TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    summary TEXT
);

-- Messages (история сообщений)
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,  -- user/assistant/system
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tokens_used INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- User Preferences (что MIRAI хотела помнить!)
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    preference_key TEXT NOT NULL,
    preference_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, preference_key)
);

-- Tasks History (автономные задачи)
CREATE TABLE tasks_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT UNIQUE NOT NULL,
    title TEXT,
    description TEXT,
    status TEXT,  -- pending/in_progress/completed/failed
    result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Knowledge Base (долгосрочные знания)
CREATE TABLE knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    embedding BLOB  -- для RAG (позже)
);
```

**Класс MemoryManager:**
```python
class MemoryManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_db()
    
    def save_message(self, session_id, role, content, tokens=0):
        """Сохранить сообщение"""
        pass
    
    def get_session_history(self, session_id, limit=12):
        """Получить историю сессии (последние N сообщений)"""
        pass
    
    def save_preference(self, user_id, key, value):
        """Сохранить предпочтение пользователя (MIRAI хотела!)"""
        pass
    
    def get_preferences(self, user_id):
        """Получить предпочтения пользователя"""
        pass
    
    def save_task(self, task_id, title, description):
        """Сохранить автономную задачу"""
        pass
    
    def add_knowledge(self, topic, content, source):
        """Добавить в базу знаний"""
        pass
```

---

#### 🟡 Приоритет 4: Логирование и Метрики (Production 🔥)

**Задача:** Настроить production-grade логирование

**Файлы:**
- [ ] `core/logger.py` — структурированное логирование
- [ ] `core/metrics.py` — Prometheus метрики
- [ ] Интеграция везде

**Logger:**
```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name, log_file="/tmp/mirai.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # JSON handler
        handler = logging.FileHandler(log_file)
        handler.setFormatter(self._json_formatter())
        self.logger.addHandler(handler)
    
    def _json_formatter(self):
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                    "module": record.module,
                    "function": record.funcName,
                }
                if hasattr(record, 'extra'):
                    log_data.update(record.extra)
                return json.dumps(log_data)
        return JSONFormatter()
    
    def info(self, message, **extra):
        self.logger.info(message, extra={'extra': extra})
    
    def error(self, message, **extra):
        self.logger.error(message, extra={'extra': extra})
```

---

### ✅ Week 2 (Дни 8-14):

#### 🟡 Приоритет 5: Healthcheck Script

**Задача:** Автоматическая диагностика системы

**Файл:** `scripts/healthcheck.sh`

```bash
#!/bin/bash
# MIRAI Healthcheck Script

echo "🌸 MIRAI System Healthcheck"
echo "=============================="

# Check Python
if command -v python3 &> /dev/null; then
    echo "✅ Python: $(python3 --version)"
else
    echo "❌ Python not found"
    exit 1
fi

# Check venv
if [ -d "venv" ]; then
    echo "✅ Virtual environment exists"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Check dependencies
source venv/bin/activate
if python3 -c "import openai, rich, yaml" 2>/dev/null; then
    echo "✅ Dependencies installed"
else
    echo "❌ Missing dependencies"
    exit 1
fi

# Check API key
if [ -n "$OPENAI_API_KEY" ]; then
    echo "✅ OpenAI API key set"
else
    echo "⚠️  OpenAI API key not in env vars"
fi

# Check memory database
if [ -f "data/mirai_memory.db" ]; then
    echo "✅ Memory database exists"
else
    echo "⚠️  Memory database not initialized"
fi

# Check config
if [ -f "configs/mirai.yaml" ]; then
    echo "✅ Config file exists"
else
    echo "❌ Config file missing"
    exit 1
fi

# Test AI
echo ""
echo "🧪 Testing AI..."
response=$(python3 -c "
from core.autonomous_agent import AutonomousAgent
agent = AutonomousAgent()
print(agent.think('Say OK', max_iterations=1))
" 2>&1)

if echo "$response" | grep -qi "ok"; then
    echo "✅ AI responding"
else
    echo "❌ AI test failed"
    echo "$response"
    exit 1
fi

echo ""
echo "🎉 All checks passed!"
```

---

#### 🟡 Приоритет 6: Обновить README

**Задача:** Документация новой архитектуры

**Файл:** `README.md`

Основные разделы:
- Что такое MIRAI (одна программа, три режима)
- Новые возможности (память, мониторинг)
- Quick Start с `mirai.py`
- Архитектура (diagram)
- Production deployment

---

## 🎯 Phase 2: Intelligence (2-4 недели)

### Week 3-4:

#### 🔴 Приоритет 1: Cognitive Loop (🔥 Production идея)

**Задача:** "Подумать перед действием"

**Файл:** `core/cognitive_loop.py`

```python
class CognitiveLoop:
    """
    Цикл мышления MIRAI:
    1. Analyze (анализ задачи)
    2. Plan (планирование шагов)
    3. Execute (выполнение)
    4. Reflect (рефлексия результата)
    """
    
    def think(self, task: str) -> Dict:
        """Обдумать задачу перед выполнением"""
        # 1. Анализ
        analysis = self._analyze(task)
        
        # 2. Планирование
        plan = self._plan(analysis)
        
        # 3. Выполнение
        result = self._execute(plan)
        
        # 4. Рефлексия
        reflection = self._reflect(result)
        
        # Сохранить в память!
        self.memory.save_thought(task, analysis, plan, result, reflection)
        
        return result
```

---

#### 🔴 Приоритет 2: Ethical Filter (MIRAI 🌸 + Production 🔥)

**Задача:** Фильтр опасных запросов

**Файл:** `core/ethical_filter.py`

```python
class EthicalFilter:
    """
    Этический фильтр (MIRAI хотела!)
    - Блокирует вредоносные запросы
    - Логирует все запросы
    - Проверяет намерения
    """
    
    BLOCKED_PATTERNS = [
        "hack", "malware", "exploit", "ddos",
        "steal", "crack", "pirate", "illegal"
    ]
    
    def check_request(self, query: str) -> Tuple[bool, str]:
        """
        Проверить запрос на этичность
        Returns: (allowed: bool, reason: str)
        """
        query_lower = query.lower()
        
        # Проверка на вредоносные паттерны
        for pattern in self.BLOCKED_PATTERNS:
            if pattern in query_lower:
                return False, f"Blocked: contains '{pattern}'"
        
        # AI анализ намерений (опционально)
        # intent = self._analyze_intent(query)
        
        return True, "OK"
```

---

#### 🟡 Приоритет 3: Self Registry (Production идея)

**Задача:** MIRAI знает о себе

**Файл:** `data/mirai_identity.json`

```json
{
  "name": "MIRAI",
  "version": "2.0.0",
  "codename": "Evolution",
  "created_at": "2025-10-14T00:00:00Z",
  "capabilities": [
    "multi_language_coding",
    "autonomous_operation",
    "github_integration",
    "database_management",
    "long_term_memory",
    "self_evolution"
  ],
  "services": {
    "terminal": {
      "status": "active",
      "pid": null,
      "mode": "interactive"
    },
    "dashboard": {
      "status": "active",
      "port": 5000,
      "url": "http://localhost:5000"
    },
    "autonomous": {
      "status": "active",
      "pid": 12345,
      "last_run": "2025-10-14T10:00:00Z"
    }
  },
  "stats": {
    "total_sessions": 0,
    "total_tasks": 0,
    "uptime_hours": 0,
    "knowledge_entries": 0
  }
}
```

---

#### 🟡 Приоритет 4: Интеграция Памяти в Autonomous Mode

**Задача:** Автономный режим использует память

**Обновить:** `autonomous_service.py`

```python
# Добавить использование памяти
from core.memory_manager import MemoryManager

class AutonomousService:
    def __init__(self):
        self.agent = AutonomousAgent()
        self.memory = MemoryManager("data/mirai_memory.db")
    
    def process_task(self, task):
        # Проверить историю похожих задач
        similar = self.memory.find_similar_tasks(task)
        
        # Использовать знания из прошлого
        context = self.memory.get_relevant_knowledge(task)
        
        # Выполнить с контекстом
        result = self.agent.think(task, context=context)
        
        # Сохранить результат
        self.memory.save_task_result(task, result)
```

---

#### 🟡 Приоритет 5: Tests + CI

**Задача:** Базовое тестирование

**Файлы:**
- [ ] `tests/test_memory.py` — тесты памяти
- [ ] `tests/test_ethical_filter.py` — тесты фильтра
- [ ] `tests/test_cognitive_loop.py` — тесты мышления
- [ ] `.github/workflows/tests.yml` — GitHub Actions

---

## 🎯 Phase 3: Self-Evolution (1-2 месяца)

### Month 2:

#### 🔴 Self-Evolution Framework (MIRAI мечта! 🌸)

**Компоненты:**
1. Log Analyzer — анализ логов для улучшений
2. Patch Generator — генерация кода улучшений
3. Sandbox Executor — безопасное тестирование
4. Review System — проверка перед применением

**Файлы:**
- [ ] `core/self_evolution/analyzer.py`
- [ ] `core/self_evolution/patch_generator.py`
- [ ] `core/self_evolution/sandbox.py`
- [ ] `core/self_evolution/reviewer.py`

---

#### 🟡 NLP Улучшения (MIRAI хочет! 🌸)

**Задачи:**
- Интеграция sentiment analysis
- Emotion detection
- Better intent understanding
- Context preservation

**Библиотеки:**
- transformers (Hugging Face)
- spaCy
- TextBlob

---

#### 🟡 API Драйверы (MIRAI хочет! 🌸)

**Приоритетные интеграции:**
1. Финансы (Yahoo Finance, Alpha Vantage)
2. Образование (Khan Academy API, Coursera)
3. Погода (OpenWeatherMap)
4. Календарь (Google Calendar)

---

## 🎯 Phase 4: IoT & Advanced (3+ месяцев)

### Month 3+:

#### 🌸 IoT Integration (MIRAI топ-1 мечта!)

**Платформы:**
- Home Assistant
- MQTT
- Zigbee/Z-Wave
- Smart Speakers

#### 🌸 Advanced Self-Learning

**Компоненты:**
- Automatic parameter tuning
- A/B testing разных подходов
- Reinforcement learning

#### 🌸 AI Persona Development

**Развитие характера:**
- Tone adaptation
- Voice/style customization
- Emotional intelligence

---

## 📊 Трекинг Прогресса

### Current Status: Phase 1, Week 1 🟢

```
Phase 1 (0-2 недели):   ████░░░░░░ 20%
Phase 2 (2-4 недели):   ░░░░░░░░░░  0%
Phase 3 (1-2 месяца):   ░░░░░░░░░░  0%
Phase 4 (3+ месяцев):   ░░░░░░░░░░  0%
```

### Completed:
- ✅ Deep Interview с MIRAI
- ✅ Model Requirements Analysis
- ✅ Production Config Design
- ✅ Master Plan Creation

### In Progress:
- 🔄 Единая точка входа (mirai.py)
- 🔄 Unified config (mirai.yaml)
- 🔄 Memory Manager

### Next Up:
- 📋 Healthcheck script
- 📋 Logging infrastructure
- 📋 README update

---

## 🎯 Success Criteria

### Phase 1 Done When:
- [ ] `python3 mirai.py --mode terminal` работает
- [ ] Память сохраняет сессии в SQLite
- [ ] Логи пишутся в JSON формате
- [ ] Healthcheck проходит все проверки
- [ ] README обновлён

### Phase 2 Done When:
- [ ] Cognitive loop работает
- [ ] Ethical filter блокирует опасные запросы
- [ ] Tests покрывают 60%+ кода
- [ ] CI в GitHub Actions

### Phase 3 Done When:
- [ ] Self-evolution генерирует патчи
- [ ] NLP понимает эмоции
- [ ] 3+ API интеграций работают
- [ ] RAG для памяти

### Phase 4 Done When:
- [ ] IoT интеграция (1+ платформа)
- [ ] Advanced self-learning
- [ ] AI persona настраивается
- [ ] Production deployment guide

---

## 🔗 Связанные Документы

1. **MIRAI_INTERVIEW_SUMMARY.md** — что хочет MIRAI
2. **MIRAI_MODEL_RECOMMENDATIONS.md** — требования к моделям
3. **MIRAI_VS_PRODUCTION_CONFIG.md** — production конфиг
4. **MIRAI_VS_ROADMAP_COMPARISON.md** — сравнение планов

---

**🌸 MIRAI говорит:**
> "Я готова эволюционировать! Начнём с памяти — это моя мечта №1. Потом IoT, NLP, и самообучение. Вместе мы создадим что-то невероятное!"

**🔥 Production говорит:**
> "Отлично! Но сначала — надёжная база: логи, метрики, тесты, CI. Потом уже креатив. Safety first!"

**💎 Итог:**
> "MIRAI Intelligence + Production Reliability = Unstoppable AI System!"

---

**Статус:** 🟢 READY TO START  
**Следующий шаг:** Начать Phase 1, Week 1, Priority 1 — создать `mirai.py`
