# 🏗️ MIRAI - Logical Architecture

**Version:** 1.0  
**Date:** October 2025  
**Status:** Phase 0 - Discovery

---

## 📐 System Overview

MIRAI is designed as a modular, event-driven autonomous agent system with clear separation of concerns. The architecture supports both local and cloud deployment, with emphasis on scalability, security, and maintainability.

---

## 🎯 Architectural Principles

1. **Modularity** - Components are loosely coupled and independently deployable
2. **Security First** - Sandboxing, policy enforcement, audit logging at every layer
3. **Observable** - Comprehensive logging, metrics, and tracing
4. **Resilient** - Circuit breakers, retries, graceful degradation
5. **Scalable** - Horizontal scaling via queue-based architecture
6. **Extensible** - Plugin system for custom integrations

---

## 🧩 High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              MIRAI SYSTEM                                     │
└──────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACES                                     │
├──────────────┬──────────────┬──────────────┬──────────────┬────────────────┤
│  Terminal    │   Web UI     │  REST API    │   CLI        │   Webhooks     │
│   (Rich)     │  (Flask)     │  (FastAPI)   │              │                │
└──────┬───────┴──────┬───────┴──────┬───────┴──────┬───────┴────────┬───────┘
       │              │              │              │                │
       └──────────────┴──────────────┴──────────────┴────────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │    API Gateway Layer        │
                      │  - Auth & Authorization     │
                      │  - Rate Limiting            │
                      │  - Request Validation       │
                      └──────────────┬──────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
        │         CORE INTELLIGENCE LAYER                         │
        │                                                          │
┌───────▼───────────┐    ┌─────────────────┐    ┌────────────────▼────────┐
│   Agent Core      │    │  Policy Engine  │    │   Orchestrator          │
│ ──────────────────│    │ ─────────────────│    │ ───────────────────────│
│ • Task Planning   │◄───┤ • Rule Evaluation│───►│ • Workflow Engine       │
│ • LLM Integration │    │ • Approval Flow  │    │ • State Machine         │
│ • Tool Calling    │    │ • Audit Log      │    │ • Error Handling        │
│ • Memory Context  │    │ • Risk Scoring   │    │ • Retry Logic           │
└─────────┬─────────┘    └──────────────────┘    └──────────┬──────────────┘
          │                                                   │
          │              ┌────────────────────┐              │
          └──────────────►  Task Queue        │◄─────────────┘
                         │  (SQLite/Redis)    │
                         │ ───────────────────│
                         │ • Priority Queue   │
                         │ • DLQ (Failed)     │
                         │ • Status Tracking  │
                         └──────────┬─────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
┌───────▼────────┐   ┌──────────────▼───────┐   ┌─────────────▼──────────┐
│  Operator      │   │   Executor Layer     │   │  Integration Layer     │
│  (Browser/RPA) │   │  ──────────────────  │   │  ─────────────────────│
│ ──────────────│   │                      │   │                        │
│ • Playwright   │   │ • Python Executor    │   │ • GitHub API           │
│ • CDP Protocol │   │ • JS/TS Executor     │   │ • Database Connectors  │
│ • pyautogui    │   │ • Go/Rust/C++ Exec   │   │ • Web Search           │
│ • Selectors    │   │ • Bash Executor      │   │ • Email/Calendar       │
│ • Sessions     │   │ • Sandbox/Docker     │   │ • Custom APIs          │
└────────┬───────┘   └──────────┬───────────┘   └─────────┬──────────────┘
         │                      │                          │
         └──────────────────────┴──────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────────┐
        │                       │                           │
┌───────▼──────────┐  ┌─────────▼────────┐  ┌─────────────▼──────────┐
│ Memory System    │  │  Knowledge Base  │  │  Monitoring & Logs     │
│ ─────────────────│  │  ────────────────│  │  ─────────────────────│
│ • SQLite DB      │  │ • Vector Store   │  │ • Structured Logging   │
│ • Sessions       │  │ • Embeddings     │  │ • Metrics (Prometheus) │
│ • Messages       │  │ • RAG Engine     │  │ • Tracing              │
│ • User Prefs     │  │ • Documents      │  │ • Health Checks        │
│ • Task History   │  │ • Semantic       │  │ • Alerting             │
└──────────────────┘  └──────────────────┘  └────────────────────────┘
```

---

## 📦 Component Details

### 1. User Interfaces Layer

#### Terminal UI (Rich)
- Interactive command-line interface
- Real-time task monitoring
- Rich formatted output
- Session management

#### Web Dashboard (Flask)
- Task submission and monitoring
- Visual workflow builder
- Health status dashboard
- Configuration management

#### REST API (FastAPI)
- RESTful endpoints for all operations
- OpenAPI documentation
- Async request handling
- WebSocket support for real-time updates

---

### 2. API Gateway Layer

**Responsibilities:**
- Authentication & Authorization (JWT tokens)
- Rate limiting per user/tenant
- Request validation and sanitization
- API versioning
- CORS handling

**Technology:**
- FastAPI middleware
- JWT tokens with rotation
- Redis for rate limiting

---

### 3. Agent Core (Intelligence Layer)

#### Task Planning Engine
```python
class TaskPlanner:
    """
    Decomposes high-level tasks into executable steps
    """
    def plan(task: str) -> List[Step]:
        # 1. Analyze task requirements
        # 2. Identify required tools
        # 3. Generate step sequence
        # 4. Estimate resources and time
        # 5. Return execution plan
```

#### LLM Integration
```python
class LLMEngine:
    """
    Manages communication with AI models
    """
    models = {
        'fast': 'gpt-3.5-turbo',      # Quick responses
        'main': 'gpt-4o-mini',         # Standard tasks
        'heavy': 'gpt-4o'              # Complex reasoning
    }
    
    def select_model(task_complexity: int) -> str:
        # Route based on complexity
```

#### Tool Calling Framework
```python
class ToolRegistry:
    """
    Registry of available tools/functions
    """
    tools = {
        'web_search': WebSearchTool(),
        'code_exec': CodeExecutor(),
        'file_ops': FileOperations(),
        'browser': BrowserAutomation(),
        'database': DatabaseConnector(),
    }
```

---

### 4. Policy Engine (Security & Governance)

```yaml
# policy.yaml
version: "1.0"

rules:
  - name: "file_deletion"
    action: "delete_file"
    requires_approval: true
    risk_level: high
    
  - name: "web_browsing"
    action: "open_url"
    requires_approval: false
    risk_level: low
    blacklist:
      - "*.onion"
      - "malware-db.com"
      
  - name: "code_execution"
    action: "execute_code"
    requires_approval: false
    risk_level: medium
    sandbox: true
    timeout: 30
```

**Components:**
- Rule Evaluator - Evaluates policies in <50ms
- Approval Flow - User confirmation UI
- Audit Logger - Immutable log of all decisions
- Risk Scorer - Assigns risk levels to actions

---

### 5. Task Queue (Orchestration)

**Queue Types:**
- **Main Queue** - Standard tasks (FIFO with priority)
- **High Priority** - Urgent tasks (processed first)
- **Scheduled** - Time-based execution
- **DLQ (Dead Letter)** - Failed tasks for review

**Task States:**
```
PENDING → QUEUED → RUNNING → [COMPLETED | FAILED | CANCELLED]
                      ↓
                   RETRYING (max 3 attempts)
                      ↓
                     DLQ
```

**Technology:**
- SQLite (MVP, local deployment)
- Redis (production, distributed)
- Celery (optional, for complex workflows)

---

### 6. Operator (Browser & RPA)

#### Browser Automation
```python
class BrowserOperator:
    """
    Controls browser via Playwright
    """
    def __init__(self):
        self.playwright = Playwright()
        self.context = None  # Browser context
        
    async def open_page(url: str):
        # Open URL with CDP
        
    async def click(selector: str):
        # Click element
        
    async def type_text(selector: str, text: str):
        # Type into input
        
    async def screenshot() -> bytes:
        # Capture screenshot
```

#### Desktop Automation
```python
class DesktopOperator:
    """
    Controls desktop apps via pyautogui
    """
    def click_at(x: int, y: int):
        # Click at coordinates
        
    def type_keys(text: str):
        # Type keyboard input
```

---

### 7. Executor Layer (Code Execution)

#### Multi-Language Support
```python
class MultiLanguageExecutor:
    """
    Executes code in multiple languages
    """
    executors = {
        'python': PythonExecutor(),
        'javascript': NodeExecutor(),
        'typescript': TypeScriptExecutor(),
        'go': GoExecutor(),
        'rust': RustExecutor(),
        'c': CExecutor(),
        'cpp': CppExecutor(),
        'bash': BashExecutor(),
    }
```

#### Sandboxing Strategy
- **Docker Containers** - Isolated execution environment
- **Resource Limits** - CPU/memory quotas
- **Network Isolation** - No external access by default
- **File System** - Read-only mounts except /tmp
- **Timeout Enforcement** - 30s default, 600s max

---

### 8. Integration Layer

#### GitHub Integration
```python
class GitHubIntegration:
    """
    GitHub API wrapper
    """
    def monitor_workflows(repo: str) -> List[WorkflowRun]:
        # Check CI/CD status
        
    def create_pr(title: str, body: str, branch: str):
        # Create pull request
        
    def create_issue(title: str, body: str):
        # Create issue
```

#### Database Connectors
- **SQLite** - Default, local storage
- **PostgreSQL** - Production relational DB
- **MongoDB** - Document storage
- **Redis** - Caching, queue, session store

---

### 9. Memory System (Persistence)

#### Database Schema
```sql
-- Sessions
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    session_id TEXT UNIQUE,
    user_id TEXT,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    summary TEXT
);

-- Messages (conversation history)
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    session_id TEXT,
    role TEXT,  -- user/assistant/system
    content TEXT,
    timestamp TIMESTAMP,
    tokens_used INTEGER
);

-- User Preferences
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    preference_key TEXT,
    preference_value TEXT,
    updated_at TIMESTAMP
);

-- Tasks History
CREATE TABLE tasks_history (
    id INTEGER PRIMARY KEY,
    task_id TEXT UNIQUE,
    title TEXT,
    description TEXT,
    status TEXT,
    result TEXT,
    created_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

---

### 10. Knowledge Base (RAG System)

#### Vector Storage
```python
class VectorStore:
    """
    Stores document embeddings for semantic search
    """
    def __init__(self):
        self.index = faiss.IndexFlatL2(dimension=1536)
        
    def add_documents(docs: List[str]):
        # Generate embeddings
        # Add to FAISS index
        
    def search(query: str, k: int = 5) -> List[Document]:
        # Semantic similarity search
```

#### RAG Pipeline
```
User Query
    ↓
Query Embedding (text-embedding-3-large)
    ↓
Vector Search (Top K=5 documents)
    ↓
Context Assembly (concatenate relevant docs)
    ↓
LLM Call (GPT-4o with context)
    ↓
Response with Citations
```

---

### 11. Monitoring & Observability

#### Structured Logging
```python
class StructuredLogger:
    """
    JSON-formatted logging
    """
    def log(level: str, message: str, **context):
        log_entry = {
            "timestamp": utcnow(),
            "level": level,
            "message": message,
            "context": context,
            "trace_id": get_trace_id(),
        }
        # Write to log file + stdout
```

#### Metrics (Prometheus)
```python
# Metrics to track
task_success_total = Counter('task_success_total')
task_failure_total = Counter('task_failure_total')
task_duration_seconds = Histogram('task_duration_seconds')
llm_tokens_used = Counter('llm_tokens_used')
llm_cost_usd = Counter('llm_cost_usd')
```

#### Health Checks
```python
def health_check() -> Dict:
    return {
        'status': 'healthy',
        'checks': {
            'database': check_database(),
            'llm_api': check_llm_api(),
            'queue': check_queue(),
            'memory': check_memory_usage(),
        }
    }
```

---

## 🔄 Data Flow Examples

### Example 1: Web Search Task

```
1. User: "Find latest React 19 features"
   ↓
2. API Gateway: Validate, authenticate
   ↓
3. Agent Core: Parse intent, create plan
   ↓
4. Policy Engine: Check if web search allowed
   ↓
5. Task Queue: Enqueue task
   ↓
6. Operator: Open browser, search Google
   ↓
7. Operator: Extract content from top 3 links
   ↓
8. Agent Core: Summarize findings (LLM)
   ↓
9. Memory: Save to session history
   ↓
10. Response: Return summary to user
```

### Example 2: Code Execution with Approval

```
1. User: "Execute: os.system('rm -rf /')"
   ↓
2. Policy Engine: ⚠️ DANGEROUS COMMAND DETECTED
   ↓
3. Policy Engine: Request user approval
   ↓
4. User: [Denied]
   ↓
5. Agent Core: Block execution, log denial
   ↓
6. Response: "Action blocked by policy"
```

---

## 🛡️ Security Architecture

### Defense in Depth

1. **Input Validation**
   - Sanitize all user inputs
   - Reject malicious patterns

2. **Authentication**
   - JWT tokens with expiration
   - API key rotation

3. **Authorization**
   - Role-based access control (RBAC)
   - Policy engine enforcement

4. **Sandboxing**
   - Docker isolation for code execution
   - Network restrictions

5. **Audit Logging**
   - Immutable logs
   - Tamper detection

6. **Secret Management**
   - Vault/KMS integration
   - No secrets in code/logs

---

## 📈 Scalability Strategy

### Vertical Scaling (Single Node)
- Increase CPU/RAM
- Use faster SSD for database
- Optimize SQLite settings

### Horizontal Scaling (Multi-Node)
```
        Load Balancer
             │
    ┌────────┼────────┐
    │        │        │
Agent1    Agent2   Agent3
    │        │        │
    └────────┼────────┘
             │
      Redis Queue (shared)
             │
      PostgreSQL (shared)
```

### Component Scaling
- **API Gateway**: N instances behind load balancer
- **Agent Core**: N workers polling Redis queue
- **Operator**: Pool of browser instances
- **Database**: Read replicas for queries, primary for writes

---

## 🔌 Extensibility (Plugin System)

### Plugin Architecture
```python
class Plugin(ABC):
    """
    Base plugin interface
    """
    @abstractmethod
    def initialize(self, config: Dict):
        pass
        
    @abstractmethod
    def execute(self, action: str, params: Dict) -> Any:
        pass
        
    @abstractmethod
    def cleanup(self):
        pass
```

### Example Plugin
```python
class SlackPlugin(Plugin):
    """
    Slack integration plugin
    """
    def execute(self, action: str, params: Dict):
        if action == 'send_message':
            return self.send_slack_message(
                channel=params['channel'],
                message=params['message']
            )
```

---

## 🚀 Deployment Architectures

### Local Deployment
```
Single machine:
- Agent Core
- SQLite database
- Browser pool
- All services on localhost
```

### Cloud Deployment (AWS Example)
```
- ECS/EKS for Agent containers
- RDS PostgreSQL for database
- ElastiCache Redis for queue
- S3 for file storage
- CloudWatch for monitoring
- ALB for load balancing
```

### Hybrid Deployment
```
- Agent Core on-premise (sensitive data)
- LLM API calls to cloud
- Cloud-based monitoring
- VPN for secure communication
```

---

## 📊 Technology Stack Summary

| Layer | Technology | Alternative |
|-------|-----------|-------------|
| Language | Python 3.10+ | - |
| API Framework | FastAPI | Flask |
| Async | asyncio | Twisted |
| Database | SQLite / PostgreSQL | MongoDB |
| Cache/Queue | Redis | RabbitMQ |
| LLM | OpenAI API | Local Ollama |
| Browser | Playwright | Selenium |
| Embeddings | text-embedding-3-large | sentence-transformers |
| Vector DB | FAISS | Chroma, Pinecone |
| Monitoring | Prometheus | Datadog |
| Logging | Python logging | ELK Stack |
| Orchestration | Kubernetes | Docker Swarm |

---

## ✅ Architectural Decisions

### ADR-001: SQLite for MVP, PostgreSQL for Production
**Context:** Need reliable database for memory and tasks  
**Decision:** Use SQLite for simplicity in MVP, migrate to PostgreSQL for production  
**Rationale:** SQLite is zero-config, PostgreSQL scales better and supports advanced features

### ADR-002: OpenAI API over Local Models (Initially)
**Context:** Need reliable LLM for agent intelligence  
**Decision:** Use OpenAI API for MVP, add local model support later  
**Rationale:** OpenAI provides best quality and reliability, local models add complexity

### ADR-003: Playwright over Selenium
**Context:** Need browser automation  
**Decision:** Use Playwright with CDP protocol  
**Rationale:** Playwright is faster, more reliable, better async support

### ADR-004: Docker Sandboxing for Code Execution
**Context:** Need safe code execution  
**Decision:** Use Docker containers for isolation  
**Rationale:** Industry standard, proven security, resource control

### ADR-005: Policy Engine as Separate Component
**Context:** Need flexible security controls  
**Decision:** Separate policy engine from agent core  
**Rationale:** Easier to update rules, clearer separation of concerns

---

**Document Version History:**
- v1.0 (2025-10) - Initial logical architecture
