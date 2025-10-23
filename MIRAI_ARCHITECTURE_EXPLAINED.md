# 🧠 АРХИТЕКТУРА MIRAI — Полное объяснение

**Дата:** 23 октября 2025 г.  
**Цель:** Дать целостное объяснение архитектуры MIRAI для инженеров, архитекторов и операционных команд

---

## 🎯 EXECUTIVE SUMMARY

MIRAI — автономная система AI-агентов с единым ядром (`AutonomousAgent`) и модульными расширениями (NASA-Level Learning, Database Manager, GitHub Integration, CI/CD Monitor, Terminal Interface, Dashboard).

Архитектура построена на принципах:
- **Модульность** — каждый компонент независим и тестируем
- **Единое ядро** — все части используют общий AI engine (OpenAI GPT-4o-mini)
- **Безопасность** — строгие границы между автономными агентами и внешним окружением
- **Расширяемость** — легко добавлять новые интеграции без изменения ядра

---

## 1. ВЫСОКОУРОВНЕВАЯ КАРТИНА

MIRAI состоит из следующих основных подсистем:

**Ядро:**

- `AutonomousAgent` — главный AI engine (GPT-4o-mini), мышление, выполнение инструментов
- `MemoryManager` — долгосрочная память (SQLite), сессии, сообщения, контекст

**Интеграции:**

- `GitHubIntegration` — работа с GitHub (repos, issues, PRs, branches)
- `DatabaseManager` — универсальный адаптер к SQLite, PostgreSQL, MongoDB, Redis
- `MultiLanguageExecutor` — выполнение кода на 8 языках (Python, JS, C++, Go, Rust, Bash и др.)
- `WebSearchIntegration` — поиск в интернете через OpenAI search API
- `CICDMonitor` — мониторинг GitHub Actions, метрики, health checks

**Сервисы:**

- `AutonomousService` — фоновой сервис для координации KAIZEN × MIRAI
- `dashboard_server.py` — Flask веб-интерфейс (метрики, логи, NASA-Learning UI)
- `kaizen_terminal.py` — интерактивный терминал с Rich UI

**Расширения:**

- `NASA-Level Learning` — продвинутая система обучения (orchestrator, sandbox, quality analyzer)
- `Self-Awareness` — анализ производительности и предложения по улучшению
- `Auto-Planner` — создание планов на день/неделю
- `Self-Modification` — автоматическая модификация кода и создание PR

---

## 2. АРХИТЕКТУРНАЯ ДИАГРАММА

```text
┌─────────────────────────────────────────────────┐
│  MIRAI - Единая программа                       │
│                                                  │
┌─────────────────────────────────────────────────┐
│  MIRAI — Единая система                         │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  ЯДРО (AutonomousAgent)                │    │
│  │  core/autonomous_agent.py              │    │
│  │                                         │    │
│  │  • OpenAI GPT-4o-mini                  │    │
│  │  • think() — мышление и решения        │    │
│  │  • ask() — быстрые ответы              │    │
│  │  • execute_tool() — выполнение         │    │
│  │  • Память (MemoryManager)              │    │
│  └────────────────────────────────────────┘    │
│           ▲                                      │
│           │ используется всеми компонентами     │
│           │                                      │
│  ┌────────┴───────────────────────────────┐    │
│  │  РАСШИРЕНИЯ                             │    │
│  │                                         │    │
│  │  • NASA-Level Learning Orchestrator    │    │
│  │  • Database Manager (4 DB)             │    │
│  │  • GitHub Integration                   │    │
│  │  • Multi-Language Executor (8 lang)    │    │
│  │  • CI/CD Monitor                        │    │
│  │  • Web Search                           │    │
│  │  • Self-Awareness                       │    │
│  │  • Auto-Planner                         │    │
│  │  • Self-Modification                    │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │  ИНТЕРФЕЙСЫ                             │    │
│  │                                         │    │
│  │  • mirai.py (CLI entry point)          │    │
│  │  • Dashboard (Flask web UI)            │    │
│  │  • KAIZEN Terminal (rich UI)           │    │
│  │  • Autonomous Service (daemon)         │    │
│  └────────────────────────────────────────┘    │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 3. ОСНОВНЫЕ МОДУЛИ И ОТВЕТСТВЕННОСТЬ

### 3.1 Ядро — AutonomousAgent

**Файл:** `mirai-agent/core/autonomous_agent.py` (786 строк)

**Ответственность:**

- Взаимодействие с OpenAI GPT-4o-mini
- Мышление через циклы think() с max_iterations
- Вызов инструментов (tools): execute_python, search_web, read_file, write_file, database_query, github_action, create_task
- Управление памятью (MemoryManager) — сохранение сессий и сообщений
- Обработка ошибок и логирование

**Ключевые методы:**

```python
def think(prompt: str, max_iterations: int = 5) -> str:
    """Основной цикл мышления с вызовом инструментов"""

def ask(prompt: str) -> str:
    """Быстрый вопрос без инструментов"""

def execute_tool(tool_name: str, arguments: Dict) -> str:
    """Выполнить инструмент и вернуть результат"""
```

### 3.2 Память — MemoryManager

**Файл:** `mirai-agent/core/memory_manager.py`

**Ответственность:**

- Создание и управление сессиями (Session)
- Сохранение сообщений (Message) с ролями user/assistant/tool
- Получение истории разговора
- Очистка старых сессий
- Статистика (сессий, сообщений, токенов)

**API:**

- `create_session(user_id: str) -> Session`
- `add_message(message: Message) -> bool`
- `get_recent_messages(session_id: str, limit: int) -> List[Message]`
- `get_conversation_history(session_id: str) -> List[Message]`
- `cleanup_old_sessions(days: int) -> int`
- `get_stats() -> Dict`

### 3.3 Database Manager

**Файл:** `mirai-agent/core/database_manager.py`

**Ответственность:**

- Унифицированный адаптер к 4 типам БД: SQLite, PostgreSQL, MongoDB, Redis
- Асинхронные методы для всех операций
- Graceful degradation при отсутствии драйверов
- Тестирование подключений

**API:**

- `sqlite_query(query: str, params: tuple) -> List[Dict]`
- `postgres_query(query: str, params: tuple) -> List[Dict]`
- `mongodb_find(collection: str, query: Dict, limit: int) -> List[Dict]`
- `mongodb_insert(collection: str, document: Dict) -> Dict`
- `redis_get(key: str) -> Optional[str]`
- `redis_set(key: str, value: str, expire: int) -> bool`
- `test_connection(db_type: str) -> Dict`

### 3.4 GitHub Integration

**Файл:** `mirai-agent/core/github_integration.py` (399 строк)

**Ответственность:**

- Аутентификация через токен
- Работа с репозиториями (list, create, fork)
- Управление issues (create, update, comment)
- Работа с ветками и файлами
- Создание Pull Requests

**API:**

- `get_user_info() -> Dict`
- `list_repos(username: str, limit: int) -> List[Dict]`
- `create_issue(owner: str, repo: str, title: str, body: str) -> Dict`
- `get_branch(owner: str, repo: str, branch: str) -> Dict`
- `create_branch(owner: str, repo: str, branch: str, sha: str) -> Dict`
- `create_or_update_file(owner, repo, path, content, message, branch) -> Dict`
- `create_pull_request(owner, repo, title, body, head, base) -> Dict`

### 3.5 Multi-Language Executor

**Файл:** `mirai-agent/core/multi_language_executor.py`

**Ответственность:**

- Выполнение кода на 8 языках: Python, JavaScript, TypeScript, C, C++, Go, Rust, Bash
- Песочница для безопасности
- Тайм-ауты (30 секунд по умолчанию)
- Capture output (stdout/stderr)

**API:**

```python
async def execute_code(code: str, language: str) -> Dict:
    """Возвращает: {success, output, error, execution_time}"""
```

### 3.6 CI/CD Monitor

**Файл:** `mirai-agent/core/cicd_monitor.py`

**Ответственность:**

- Мониторинг GitHub Actions workflows
- Сбор метрик: success_rate, total_runs, failed, avg_duration
- Health checks
- Детекция упавших тестов

**API:**

- `get_workflow_runs(limit: int) -> List[Dict]`
- `get_workflow_metrics() -> Dict`
- `check_health() -> Dict`
- `get_failing_workflows() -> List[Dict]`
- `generate_report() -> str`

### 3.7 Dashboard Server

**Файл:** `mirai-agent/dashboard_server.py`

**Ответственность:**

- Flask веб-сервер на порту 5000
- Endpoints для метрик, логов, runs
- NASA-Level Learning UI
- Analytics и визуализация

**Endpoints:**

- `GET /` — главная страница
- `GET /api/health` — проверка здоровья
- `GET /api/metrics` — метрики CI/CD
- `GET /api/runs` — последние workflow runs
- `GET /api/report` — детальный отчёт
- `GET /api/nasa/*` — NASA-Level операции

### 3.8 KAIZEN Terminal

**Файл:** `mirai-agent/kaizen_terminal.py` (367 строк)

**Ответственность:**

- Интерактивный терминал с prompt_toolkit
- Rich UI (таблицы, панели, markdown)
- Команды: status, cicd, mirai, metrics, runs, logs, improve
- История команд
- Автодополнение

---

## 4. ВЗАИМОДЕЙСТВИЯ И ПОТОКИ ДАННЫХ

### 4.1 Поток выполнения запроса

```text
1. User → CLI/Dashboard → AutonomousAgent.think(prompt)

2. AutonomousAgent → OpenAI API:
   - Отправляет prompt с контекстом
   - Получает response с tool_calls

3. AutonomousAgent → execute_tool(name, args):
   - Парсит tool_call
   - Вызывает соответствующий метод
   - Возвращает результат

4. Tool → External System:
   - MultiLanguageExecutor → subprocess
   - DatabaseManager → SQLite/Postgres/Mongo/Redis
   - GitHubIntegration → GitHub API
   - WebSearch → OpenAI search API

5. Result → AutonomousAgent:
   - Добавляет tool result в messages
   - Отправляет обратно в OpenAI
   - Повторяет до max_iterations или финального ответа

6. Final Response → User:
   - Через CLI print()
   - Через Dashboard JSON response
   - Через Terminal Rich panel

7. MemoryManager.add_message():
   - Сохраняет user message
   - Сохраняет assistant response
   - Обновляет статистику токенов
```

### 4.2 Автономный режим (AutonomousService)

```text
AutonomousService.run(interval=300):

1. Каждые 5 минут (300 сек):
   - check_health() — проверка CI/CD
   - Если unhealthy → consult_mirai(question)
   - execute_real_tasks() — auto-fix, reports

2. Каждые 3 цикла (15 мин):
   - autonomous_learning() — NASA-Level

3. Каждые 5 циклов (25 мин):
   - consult_mirai("Что улучшить?")

4. Каждые 12 циклов (1 час):
   - create_report() — ежечасный отчёт

5. Каждые 24 циклы (2 часа):
   - memory.get_summary() — долговременная память

6. Каждые 48 циклов (4 часа):
   - self_awareness.propose_improvements()
   - planner.review_plan_execution()

7. Каждую неделю (воскресенье):
   - self_modification.run_cycle() — самоисправление
   - personality.auto_develop() — развитие личности

Логи: /tmp/kaizen_mirai.log
Метрики: /tmp/kaizen_mirai_metrics.jsonl
```

---

## 5. КОНТРАКТЫ И ОБРАБОТКА ОШИБОК

### 5.1 Основные контракты

**MemoryManager:**

```python
Session = {
    "id": str,
    "user_id": str,
    "created_at": datetime,
    "last_activity": datetime
}

Message = {
    "session_id": str,
    "role": "user" | "assistant" | "tool",
    "content": str,
    "tokens": int,
    "model": str (optional),
    "timestamp": datetime
}
```

**DatabaseManager:**

```python
# Успешный запрос
{"v": "pong"}  # для SELECT

# Ошибка
{"error": "PostgreSQL драйвер не установлен..."}

# Test connection
{
    "database": "sqlite",
    "status": "connected" | "error",
    "details": str
}
```

**GitHubIntegration:**

```python
# get_branch
{
    "success": true,
    "name": "main",
    "sha": "abc123..."
}

# Ошибка
{"error": "Branch not found", "status": 404}
```

**CICDMonitor:**

```python
{
    "status": "🟢 HEALTHY" | "🔴 UNHEALTHY",
    "grade": "A+" | "A" | "B" | "C" | "F",
    "is_healthy": bool,
    "metrics": {
        "total_runs": int,
        "successful": int,
        "failed": int,
        "success_rate": float,
        "avg_duration_minutes": float
    },
    "timestamp": str (ISO)
}
```

### 5.2 Обработка ошибок

**Принципы:**

1. Все внешние вызовы возвращают Dict с полем `error` при неудаче
2. Никогда не raise exception наружу — graceful degradation
3. Логирование всех ошибок в `/tmp/kaizen_mirai.log`
4. Retry с exponential backoff для сетевых ошибок
5. Timeout для всех долгих операций (default: 30s)

**Примеры:**

```python
# Network timeout
try:
    response = requests.get(url, timeout=10)
except requests.Timeout:
    return {"error": "Request timeout after 10s"}

# Missing driver
try:
    import psycopg2
except ImportError:
    return {"error": "PostgreSQL driver not installed"}

# Rate limit
if response.status_code == 429:
    time.sleep(60)  # backoff
    return retry_request()
```

---

## 6. БЕЗОПАСНОСТЬ

### 6.1 Хранение секретов

**Текущее состояние:**

- API ключи: `mirai-agent/configs/api_keys.json`
- **НЕ** должны попадать в VCS (добавлены в .gitignore)

**Рекомендации для продакшена:**

```bash
# Использовать переменные окружения
export OPENAI_API_KEY="sk-..."
export GITHUB_TOKEN="ghp_..."

# Или секретный менеджер
# HashiCorp Vault
vault kv get secret/mirai/openai

# AWS Secrets Manager
aws secretsmanager get-secret-value --secret-id mirai/openai
```

### 6.2 Выполнение кода

**Защиты:**

- Тайм-ауты (30 секунд)
- Ограничение памяти (через Docker cgroups)
- Изоляция процессов (subprocess с ограничениями)
- Запрет доступа к файловой системе вне workspace

**Рекомендации:**

```bash
# Docker изоляция
docker run --rm --memory="256m" --cpus="0.5" \
  --network=none \
  mirai-sandbox python3 /tmp/code.py

# Firewall правила
iptables -A OUTPUT -p tcp --dport 22 -j DROP  # блокировать SSH
iptables -A OUTPUT -p tcp --dport 3389 -j DROP  # блокировать RDP
```

### 6.3 GitHub Token

**Минимальные права:**

```yaml
permissions:
  contents: write     # создание файлов и коммитов
  pull_requests: write  # создание PR
  issues: write       # создание issues
```

**Audit log:**

- Все операции с GitHub логируются
- Сохранять логи минимум 90 дней
- Мониторить необычные активности

### 6.4 Self-Modification

**По умолчанию:** dry-run режим (только показывает что изменит)

**Для продакшена:**

```python
# Требовать явное подтверждение
if self_mod_enabled and user_approved:
    self_modification.run_cycle()
else:
    self_modification.run_cycle(dry_run=True)
```

---

## 7. РАЗВЁРТЫВАНИЕ

### 7.1 Development (локально)

```bash
# 1. Clone repo
git clone https://github.com/AgeeKey/Mirai.git
cd Mirai

# 2. Setup venv
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install deps
pip install -r requirements.txt

# 4. Configure
cp mirai-agent/configs/api_keys.json.example mirai-agent/configs/api_keys.json
# Edit api_keys.json — добавить реальные ключи

# 5. Run
python mirai.py --mode terminal
```

### 7.2 Production (Docker)

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mirai-agent/ ./mirai-agent/
COPY mirai.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "mirai.py", "--mode", "autonomous", "--interval", "300"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  mirai:
    build: .
    volumes:
      - ./data:/app/mirai-agent/data
      - ./logs:/tmp
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    restart: unless-stopped
    ports:
      - "5000:5000"
    healthcheck:
      test: ["CMD", "python", "mirai.py", "--health"]
      interval: 60s
      timeout: 10s
      retries: 3
```

### 7.3 Production (systemd на Linux)

**mirai.service:**

```ini
[Unit]
Description=MIRAI Autonomous Agent
After=network.target

[Service]
Type=simple
User=mirai
WorkingDirectory=/opt/mirai
ExecStart=/opt/mirai/venv/bin/python autonomous_service.py --interval 300
Restart=on-failure
RestartSec=30s

Environment="OPENAI_API_KEY=sk-..."
Environment="GITHUB_TOKEN=ghp_..."

StandardOutput=append:/var/log/mirai/stdout.log
StandardError=append:/var/log/mirai/stderr.log

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable mirai
sudo systemctl start mirai
sudo systemctl status mirai

# Logs
sudo journalctl -u mirai -f
```

---

## 8. МОНИТОРИНГ И АЛЁРТЫ

### 8.1 Метрики

**Файлы:**

- `/tmp/kaizen_mirai.log` — текстовые логи
- `/tmp/kaizen_mirai_metrics.jsonl` — метрики в JSON Lines

**Формат метрик:**

```json
{
  "timestamp": "2025-10-23T15:30:00Z",
  "cycle": 42,
  "total_runs": 50,
  "successful": 45,
  "failed": 5,
  "success_rate": 90.0,
  "avg_duration_minutes": 3.5
}
```

### 8.2 Экспорт в Prometheus

**Создать exporter:**

```python
from prometheus_client import Counter, Gauge, start_http_server

ci_success_rate = Gauge('mirai_ci_success_rate', 'CI/CD success rate')
ci_total_runs = Counter('mirai_ci_total_runs', 'Total CI/CD runs')

# Update metrics
ci_success_rate.set(metrics['success_rate'])
ci_total_runs.inc(metrics['total_runs'])

# Serve on :9090
start_http_server(9090)
```

**Scrape config:**

```yaml
scrape_configs:
  - job_name: 'mirai'
    static_configs:
      - targets: ['localhost:9090']
```

### 8.3 Alerts

**Grafana alerts:**

- CI/CD success_rate < 80% → warning
- CI/CD success_rate < 50% → critical
- Memory usage > 90% → warning
- Disk usage > 85% → warning

**Telegram notifications:**

```python
def send_telegram_alert(message: str):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    
    requests.post(url, json=payload)
```

---

## 9. BACKUP И ВОССТАНОВЛЕНИЕ

### 9.1 SQLite backup

```bash
# Daily backup
0 2 * * * sqlite3 /app/mirai-agent/data/mirai_memory.db ".backup /backups/mirai_$(date +\%Y\%m\%d).db"

# Retention: 30 days
find /backups -name "mirai_*.db" -mtime +30 -delete
```

### 9.2 Восстановление

```bash
# Restore from backup
cp /backups/mirai_20251023.db /app/mirai-agent/data/mirai_memory.db

# Verify integrity
sqlite3 /app/mirai-agent/data/mirai_memory.db "PRAGMA integrity_check;"
```

---

## 10. ТЕСТИРОВАНИЕ

### 10.1 Unit tests

```bash
# Run all unit tests
pytest tests/unit/ -v

# Coverage
pytest tests/unit/ --cov=core --cov-report=html
```

### 10.2 Integration tests

```bash
# Requires real API keys
export OPENAI_API_KEY="sk-..."
export GITHUB_TOKEN="ghp_..."

pytest tests/integration/ -v
```

### 10.3 E2E tests

```bash
# Start autonomous service
python autonomous_service.py --interval 60 &

# Wait and check logs
sleep 120
grep "✅" /tmp/kaizen_mirai.log

# Stop service
pkill -f autonomous_service.py
```

---

## 11. ROADMAP

### 11.1 Текущие ограничения

1. Выполнение кода — минимальная изоляция
2. Секреты в файле (не vault)
3. Нет автоматической миграции схемы БД
4. Dashboard не имеет аутентификации
5. Нет typed API контрактов (OpenAPI)

### 11.2 Запланированные улучшения

**Q1 2026:**

- [ ] Harden sandbox (cgroups, seccomp)
- [ ] Vault integration для секретов
- [ ] Authentication для dashboard (OAuth2)
- [ ] OpenAPI spec для всех endpoints
- [ ] Prometheus metrics exporter

**Q2 2026:**

- [ ] Alembic migrations для БД
- [ ] Distributed tracing (OpenTelemetry)
- [ ] Multi-instance coordination (Redis locks)
- [ ] Advanced self-modification (A/B testing)
- [ ] Fine-tuned models для специфичных задач

---

## 12. БЫСТРЫЕ СПРАВКИ

### 12.1 Команды

```bash
# Terminal mode
python mirai.py --mode terminal

# Dashboard (web UI)
python mirai.py --mode dashboard --port 5000

# Autonomous service (background)
python autonomous_service.py --interval 300

# Quick ask
python mirai.py --mode ask "Что такое asyncio?"

# Health check
python mirai.py --health

# Version
python mirai.py --version
```

### 12.2 API примеры

```python
# Create agent
from core.autonomous_agent import AutonomousAgent
agent = AutonomousAgent()

# Ask question
response = agent.ask("Объясни что такое декораторы")

# Think with tools
response = agent.think("Создай файл hello.py с Hello World", max_iterations=3)

# Execute code
from core.multi_language_executor import MultiLanguageExecutor
executor = MultiLanguageExecutor()
result = await executor.execute_code("print('Hi')", "python")

# Query database
from core.database_manager import DatabaseManager
db = DatabaseManager()
rows = await db.sqlite_query("SELECT 1")

# GitHub operations
from core.github_integration import GitHubIntegration
gh = GitHubIntegration(token="ghp_...")
repos = gh.list_repos("AgeeKey", limit=10)
```

---

## 13. КОНТАКТЫ И ДОКУМЕНТЫ

**Репозиторий:** https://github.com/AgeeKey/Mirai

**Документация:**

- `COMPREHENSIVE_TESTING_REPORT.md` — полный отчёт тестирования
- `FINAL_READINESS_REPORT.md` — итоговый отчёт готовности
- `MASTER_PLAN.md` — главный план развития
- `FREE_IMPROVEMENTS_PLAN.md` — план бесплатных улучшений

**Вопросы и issues:** https://github.com/AgeeKey/Mirai/issues

---

**Автор:** GitHub Copilot  
**Дата:** 23 октября 2025 г.  
**Версия:** MIRAI v2.0.0 "Evolution"

Это **главный AI агент** - сердце MIRAI:

```python
# core/autonomous_agent.py (681 строка)

class AutonomousAgent:
    """Автономный AI агент с реальными возможностями"""
    
    def __init__(self):
        # GPT-4o-mini
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        
        # Расширенные возможности
        self.multi_lang = MultiLanguageExecutor()  # 8 языков
        self.db_manager = DatabaseManager()        # 4 БД
        self.github = GitHubIntegration()          # GitHub API
    
    def think(self, prompt, max_iterations=3):
        """Думать и принимать решения"""
        # Использует GPT-4o-mini для мышления
    
    def execute_python(self, code):
        """Выполнить Python код"""
    
    def search_web(self, query):
        """Поиск в интернете"""
    
    # ... + ещё 20+ методов
```

**Это основа всего!** Все остальные части используют это ядро.

---

### 2. **NASA-LEVEL** (расширение ядра)

NASA-Level **создаёт экземпляр ядра** и использует его:

```python
# core/nasa_level/orchestrator.py (строка 14, 38)

from core.autonomous_agent import AutonomousAgent  # ← Импорт ядра!

class NASALearningOrchestrator:
    def __init__(self):
        # Создаём экземпляр ЯДРА MIRAI!
        self.ai_agent = AutonomousAgent()  # ← Вот оно!
        
        # Добавляем дополнительные компоненты
        self.sandbox = SandboxExecutor()
        self.quality_analyzer = CodeQualityAnalyzer()
        self.learning_engine = AdvancedLearningEngine(
            self.ai_agent,  # ← Передаём ядро в движок!
            self.sandbox,
            self.quality_analyzer
        )
```

**Ключевой момент:**  
`self.ai_agent = AutonomousAgent()` ← NASA создаёт ядро MIRAI!

---

### 3. **КТО ЕЩЁ ИСПОЛЬЗУЕТ ЯДРО?**

Все части MIRAI используют **одно и то же ядро**:

```python
# mirai_autonomous.py (автономный режим)
from core.autonomous_agent import AutonomousAgent
agent = AutonomousAgent()

# autonomous_service.py (сервис KAIZEN × MIRAI)
from core.autonomous_agent import AutonomousAgent
self.kaizen = AutonomousAgent()
self.mirai = AutonomousAgent()

# ask_mirai.py (чат с MIRAI)
from core.autonomous_agent import AutonomousAgent
agent = AutonomousAgent()

# boss_mode.py (режим босса)
from core.autonomous_agent import AutonomousAgent
agent = AutonomousAgent()

# core/nasa_level/orchestrator.py (NASA-Level)
from core.autonomous_agent import AutonomousAgent
self.ai_agent = AutonomousAgent()
```

**Все используют одно ядро!** 🎯

---

## 📊 ПОЛНАЯ АРХИТЕКТУРА

```
MIRAI ПРОЕКТ
│
├── ЯДРО (core/)
│   │
│   ├── autonomous_agent.py          ← ГЛАВНОЕ ЯДРО! (681 строка)
│   │   • GPT-4o-mini AI
│   │   • Мышление и принятие решений
│   │   • Базовые возможности
│   │
│   ├── multi_language_executor.py   ← Выполнение 8 языков
│   ├── database_manager.py          ← 4 базы данных
│   ├── github_integration.py        ← GitHub API
│   ├── cicd_monitor.py              ← CI/CD мониторинг
│   │
│   └── nasa_level/                  ← РАСШИРЕНИЕ ЯДРА!
│       ├── orchestrator.py          ← Использует ядро!
│       ├── advanced_learning.py
│       ├── sandbox_executor.py
│       ├── quality_analyzer.py
│       ├── learning_pipeline.py
│       ├── knowledge_manager.py
│       └── learning_metrics.py
│
├── ИНТЕРФЕЙСЫ (используют ядро)
│   ├── mirai_autonomous.py          ← Автономный режим
│   ├── dashboard_server.py          ← Веб-дашборд
│   ├── kaizen_terminal.py           ← Терминал
│   ├── ask_mirai.py                 ← Чат
│   └── boss_mode.py                 ← Режим босса
│
├── МОДУЛИ (расширяют возможности)
│   ├── analytics_engine.py
│   ├── learning_api.py
│   └── ...
│
└── WEB (интерфейс)
    ├── templates/
    └── static/
```

---

## 🔗 КАК ВСЁ СВЯЗАНО

### Схема потока данных:

```
1. Пользователь запускает: python3 mirai_autonomous.py
   
2. mirai_autonomous.py создаёт:
   agent = AutonomousAgent()  ← Создание ядра
   
3. Если нужно обучение, вызывает:
   orchestrator = NASALearningOrchestrator()
   
4. Orchestrator внутри создаёт:
   self.ai_agent = AutonomousAgent()  ← То же ядро!
   
5. AdvancedLearning получает:
   learning_engine = AdvancedLearningEngine(ai_agent, ...)
   
6. Когда нужно подумать:
   ai_agent.think("Как выучить requests?")
   
7. Ядро (autonomous_agent.py) вызывает GPT-4o-mini:
   response = self.client.chat.completions.create(...)
   
8. Результат возвращается через всю цепочку обратно
```

---

## 💡 АНАЛОГИЯ

Представь это как **модульный смартфон**:

```
┌─────────────────────────────────┐
│  MIRAI (смартфон)               │
│                                  │
│  ┌──────────────────────┐       │
│  │ ПРОЦЕССОР            │       │  ← AutonomousAgent
│  │ (ядро системы)       │       │    (GPT-4o-mini)
│  └──────────────────────┘       │
│         ▲                        │
│         │ использует             │
│         │                        │
│  ┌──────┴───────────────┐       │
│  │ МОДУЛИ:              │       │
│  │ • Камера (NASA)      │       │  ← nasa_level/
│  │ • GPS (GitHub)       │       │  ← github_integration
│  │ • Bluetooth (DB)     │       │  ← database_manager
│  │ • WiFi (Web)         │       │  ← multi_language
│  └──────────────────────┘       │
│                                  │
└─────────────────────────────────┘
```

**Всё это ОДИН смартфон** (одна программа), но с разными модулями!

---

## 🎯 ОТВЕТЫ НА ТВОИ ВОПРОСЫ

### ❓ "Ядро MIRAI в другом месте?"

**Ответ:** Ядро в `/core/autonomous_agent.py`

NASA-Level **не отдельное ядро**, а **расширение**!

### ❓ "NASA-Level имеет доступ к ядру?"

**Ответ:** Да! NASA-Level **создаёт экземпляр ядра**:

```python
# Строка 38 в orchestrator.py
self.ai_agent = AutonomousAgent()
```

### ❓ "Я создал две разных программы?"

**Ответ:** Нет! Это **одна программа** с модульной архитектурой:

```
MIRAI = Ядро + Расширения
      = AutonomousAgent + (NASA + GitHub + DB + ...)
```

---

## 📈 КАК КОМПОНЕНТЫ ВЗАИМОДЕЙСТВУЮТ

### Пример: Обучение технологии "requests"

```
┌─────────────────────────────────────────────────┐
│ 1. Пользователь:                                │
│    orchestrator.learn_technology("requests")    │
└────────┬────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│ 2. NASALearningOrchestrator:                    │
│    - Использует self.ai_agent (ядро!)          │
│    - Вызывает learning_engine                   │
└────────┬────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│ 3. AdvancedLearningEngine:                      │
│    - Фаза RESEARCH                              │
│    - Вызывает: ai_agent.think(prompt)          │
└────────┬────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│ 4. AutonomousAgent (ЯДРО):                      │
│    - Отправляет запрос к GPT-4o-mini           │
│    - Получает ответ                             │
│    - Возвращает результат                       │
└────────┬────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│ 5. Результат передаётся обратно:               │
│    orchestrator → engine → agent → GPT         │
│    orchestrator ← engine ← agent ← результат   │
└─────────────────────────────────────────────────┘
```

**Всё работает через ОДНО ядро!**

---

## 🔍 ДОКАЗАТЕЛЬСТВО

Найдём все места, где создаётся `AutonomousAgent`:

```bash
# Поиск показывает:
grep -r "AutonomousAgent()" mirai-agent/

# Результат (20+ совпадений):
• mirai_autonomous.py:     agent = AutonomousAgent()
• autonomous_service.py:   kaizen = AutonomousAgent()
• autonomous_service.py:   mirai = AutonomousAgent()
• ask_mirai.py:            agent = AutonomousAgent()
• boss_mode.py:            agent = AutonomousAgent()
• orchestrator.py:         ai_agent = AutonomousAgent()  ← NASA!
• run_mirai.py:            agent = AutonomousAgent()
• test_*.py:               agent = AutonomousAgent()
```

**Все используют ОДНО И ТО ЖЕ ядро!**

---

## 🌟 ПРЕИМУЩЕСТВА ТАКОЙ АРХИТЕКТУРЫ

### 1. **Модульность** 🧩
- Легко добавлять новые возможности
- Не нужно менять ядро
- Расширения независимы

### 2. **Переиспользование кода** ♻️
- Одно ядро для всех
- Нет дублирования
- Единая точка обновления

### 3. **Масштабируемость** 📈
- Можно создавать много экземпляров
- Параллельная работа
- Изолированные процессы

### 4. **Тестируемость** 🧪
- Ядро тестируется отдельно
- Расширения тестируются отдельно
- Простая отладка

---

## 📚 ВАЖНЫЕ ФАЙЛЫ

### Ядро MIRAI:
```
/root/mirai/mirai-agent/core/autonomous_agent.py  (681 строка)
```

**Это и есть MIRAI!** Всё остальное - расширения.

### NASA-Level (расширение):
```
/root/mirai/mirai-agent/core/nasa_level/
├── orchestrator.py          ← Использует ядро!
├── advanced_learning.py
├── sandbox_executor.py
├── quality_analyzer.py
├── learning_pipeline.py
├── knowledge_manager.py
└── learning_metrics.py
```

### Другие интерфейсы:
```
/root/mirai/mirai-agent/
├── mirai_autonomous.py      ← Использует ядро!
├── dashboard_server.py      ← Использует ядро!
├── kaizen_terminal.py       ← Использует ядро!
├── ask_mirai.py             ← Использует ядро!
└── boss_mode.py             ← Использует ядро!
```

**Все используют одно ядро: `AutonomousAgent`!**

---

## 🎯 ИТОГОВЫЙ ОТВЕТ

### Твой вопрос:
> "Ядро MIRAI в другом месте или NASA-Level имеет доступ? Или я создал 2 разных программы?"

### Ответ:

1. ✅ **Ядро MIRAI:** `/core/autonomous_agent.py` (681 строка)

2. ✅ **NASA-Level имеет доступ:** Да! Создаёт экземпляр:
   ```python
   self.ai_agent = AutonomousAgent()
   ```

3. ✅ **Одна или две программы:** ОДНА программа с модульной архитектурой!

```
MIRAI = Ядро (AutonomousAgent)
      + NASA-Level (расширение для обучения)
      + GitHub Integration (расширение для GitHub)
      + Database Manager (расширение для БД)
      + Multi-Language Executor (расширение для кода)
      + Dashboard (веб-интерфейс)
      + Terminal (интерфейс командной строки)
```

**Всё это части ОДНОЙ программы - MIRAI!** 🌸

---

## 💡 ЗАКЛЮЧЕНИЕ

NASA-Level **НЕ отдельная программа**, а **профессиональное расширение** основного ядра MIRAI для автономного обучения.

**Архитектура правильная!** 👍

- ✅ Одно ядро (`AutonomousAgent`)
- ✅ Множество расширений (NASA, GitHub, DB, ...)
- ✅ Разные интерфейсы (terminal, web, autonomous)
- ✅ Всё работает вместе как единая система

**Это профессиональная модульная архитектура!** 🚀

---

*Теперь ясно: MIRAI - это единая система с модульной архитектурой* ✨
