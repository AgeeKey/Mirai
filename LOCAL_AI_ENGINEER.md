# 🤖 MIRAI Local AI Engineer

## Overview

MIRAI Local AI Engineer is a fully autonomous AI system that can plan tasks, search for information, write and fix code, execute scripts in sandboxes, document steps, and learn from mistakes — all without external API dependencies (when using Ollama), fast and secure.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 MIRAI Local AI Engineer                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐        ┌──────────────┐             │
│  │   Ollama     │        │   OpenAI     │             │
│  │   (Local)    │        │   (Cloud)    │             │
│  └──────┬───────┘        └──────┬───────┘             │
│         └────────┬───────────────┘                      │
│                  │                                      │
│         ┌────────▼─────────┐                           │
│         │  ReAct Controller │                          │
│         │ (Reason + Act)    │                          │
│         └────────┬──────────┘                          │
│                  │                                      │
│    ┌─────────────┼─────────────┐                      │
│    │             │             │                       │
│ ┌──▼───┐  ┌─────▼─────┐  ┌───▼────┐                 │
│ │FAISS │  │   Docker   │  │Browser │                 │
│ │ RAG  │  │   Runner   │  │  Auto  │                 │
│ └──────┘  └────────────┘  └────────┘                 │
│                                                        │
│         ┌──────────────────┐                          │
│         │ Self-Reflection  │                          │
│         │    System        │                          │
│         └──────────────────┘                          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Ollama Client (`core/ollama_client.py`)

Local LLM inference without external API calls.

**Features:**
- Supports Mistral, Llama2, and other Ollama models
- Function calling support via prompt injection
- Automatic model pulling
- Configurable temperature and max tokens

**Usage:**
```python
from core.ollama_client import OllamaClient

client = OllamaClient(model="mistral:7b")

# Simple generation
response = client.generate("What is Python?")

# Chat with function calling
messages = [
    {"role": "user", "content": "Calculate 5 + 3"}
]
result = client.chat(messages, tools=tools)
```

**Installation:**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull mistral:7b
# or
ollama pull llama2:7b
```

### 2. FAISS RAG System (`core/faiss_rag.py`)

Fast, local vector storage for knowledge retrieval.

**Features:**
- Local embeddings (sentence-transformers, no API)
- Efficient similarity search with FAISS
- Automatic chunking with overlap
- Hit@k metrics for quality tracking
- Persistent storage

**Usage:**
```python
from core.faiss_rag import FAISSRAGSystem

# Initialize
rag = FAISSRAGSystem(
    collection_name="mirai_knowledge",
    embedding_model="all-MiniLM-L6-v2",
    chunk_size=512,
)

# Index knowledge base
rag.add_documents_from_directory("knowledge_base/", pattern="*.md")

# Search
results = rag.search("How to use MIRAI?", top_k=5)
for doc, score in results:
    print(f"{score:.3f}: {doc['text'][:100]}...")

# Get context for LLM
context = rag.get_relevant_context(
    "AI agent capabilities",
    max_chunks=5,
    max_tokens=2000
)

# Get stats
stats = rag.get_stats()
print(f"Hit@5 rate: {stats['hit_rate_5']:.1f}%")
```

**Installation:**
```bash
pip install faiss-cpu sentence-transformers
```

### 3. Docker Code Runner (`core/docker_runner.py`)

Secure code execution in isolated containers.

**Features:**
- Network isolation (`--network none`)
- Memory and CPU limits
- Timeout enforcement
- Multi-language support (Python, JavaScript, Bash, Go, Rust)
- Automatic cleanup
- Fallback to subprocess when Docker unavailable

**Usage:**
```python
from core.docker_runner import DockerCodeRunner

runner = DockerCodeRunner(
    memory_limit="256m",
    cpu_quota=50000,  # 50% of one CPU
    timeout=30
)

# Execute Python
result = runner.execute_python("""
print("Hello from Docker!")
x = 2 + 2
print(f"2 + 2 = {x}")
""")

print(f"Status: {result.status.value}")
print(f"Output: {result.output}")
print(f"Time: {result.execution_time:.3f}s")

# Execute JavaScript
result = runner.execute_javascript("console.log('Hello from Node!')")

# Get statistics
stats = runner.get_stats()
print(f"Success rate: {stats['success_rate']:.1f}%")
```

**Installation:**
```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
```

### 4. Browser Automation (`core/browser_automation.py`)

Lightweight browser automation using Chrome/Chromium.

**Features:**
- Headless browsing
- Page content extraction
- Text extraction (without HTML)
- Link extraction
- Screenshot capture
- Google search integration

**Usage:**
```python
from core.browser_automation import BrowserAutomation

browser = BrowserAutomation(headless=True)

# Fetch page
html = browser.fetch_url("https://example.com")

# Get text content
text = browser.get_page_text("https://example.com")
print(text)

# Extract links
links = browser.get_links("https://example.com")
print(f"Found {len(links)} links")

# Take screenshot
browser.screenshot("https://example.com", "/tmp/screenshot.png")

# Search Google
results = browser.search_google("Python tutorials", num_results=10)
for result in results:
    print(f"{result['title']}: {result['url']}")
```

**Installation:**
```bash
# Install Chromium
sudo apt install chromium-browser
# or
sudo apt install google-chrome-stable
```

### 5. ReAct Controller (`core/react_controller.py`)

Autonomous task execution using Reason + Act pattern.

**Features:**
- Multi-step reasoning
- Autonomous tool selection
- Error recovery
- Progress tracking
- Statistics collection

**Usage:**
```python
from core.react_controller import ReActController, Task
from core.autonomous_agent import AutonomousAgent

# Create agent
agent = AutonomousAgent()

# Create controller
controller = ReActController(
    llm_client=agent.client,
    tools=agent.tools,
    max_steps=10,
    verbose=True
)

# Register tool handlers
controller.register_tool_handler("execute_python", agent.execute_python)
controller.register_tool_handler("search_web", agent.search_web)
controller.register_tool_handler("read_file", agent.read_file)

# Create task
task = Task(
    id="task_1",
    description="Write a Python script to calculate fibonacci numbers",
    goal="Create and test the script",
    max_steps=10
)

# Execute
success, steps, answer = controller.execute_task(task)

print(f"Success: {success}")
print(f"Steps: {len(steps)}")
print(f"Answer: {answer}")

# Get stats
stats = controller.get_stats()
print(f"Success rate: {stats['success_rate']:.1f}%")
```

### 6. Self-Reflection System (`core/self_reflection.py`)

Tracks execution history and learns from mistakes.

**Features:**
- SQLite-based storage
- Success/failure tracking
- KPI calculation
- LoRA training data export
- Metrics tracking

**Usage:**
```python
from core.self_reflection import SelfReflectionSystem

system = SelfReflectionSystem(db_path="data/reflections.db")

# Add reflection after task
system.add_reflection(
    task_id="task_1",
    task_description="Calculate fibonacci",
    status="success",
    what_worked="Recursive approach worked well",
    what_failed="",
    lessons_learned="Recursion is good for small numbers",
    tool_calls=[
        {"tool": "execute_python", "args": {"code": "..."}}
    ],
    execution_time=5.2,
    tokens_used=150,
    hallucination_detected=False
)

# Get metrics
metrics = system.calculate_metrics()
print(f"Task Success Rate: {metrics.task_success_rate:.1f}% (target ≥70%)")
print(f"Mean Time to Result: {metrics.mean_time_to_result:.2f} min (target <10 min)")
print(f"Hallucination Rate: {metrics.hallucination_rate:.1f}% (target →0%)")
print(f"Tool Use Accuracy: {metrics.tool_use_accuracy:.1f}% (target ≥90%)")

# Export for LoRA training
system.export_training_data("/tmp/training_data.jsonl", status="success")

# Get summary
summary = system.get_summary()
print(summary)
```

### 7. Tool Validator (`core/tool_validator.py`)

Validates LLM tool calls for correctness.

**Features:**
- Schema validation
- Type checking
- Required parameter validation
- Accuracy tracking

**Usage:**
```python
from core.tool_validator import ToolValidator

validator = ToolValidator(tools)

# Validate single call
is_valid, error = validator.validate_tool_call(
    "execute_python",
    {"code": "print('hello')"}
)

if is_valid:
    print("✅ Valid tool call")
else:
    print(f"❌ Invalid: {error}")

# Get accuracy
accuracy = validator.get_accuracy()
print(f"Tool use accuracy: {accuracy:.1f}%")
```

## Dashboard API

### Task Runner Endpoints

**1. Execute Task**
```bash
POST /api/tasks/run
Content-Type: application/json

{
  "description": "Write a Python script to calculate prime numbers",
  "goal": "Create and test the script",
  "max_steps": 10
}

Response:
{
  "success": true,
  "task_id": "task_abc123",
  "message": "Task started successfully"
}
```

**2. List Tasks**
```bash
GET /api/tasks/list

Response:
{
  "success": true,
  "tasks": [
    {
      "task_id": "task_abc123",
      "description": "Write a Python script...",
      "status": "running",
      "steps_count": 5,
      "created_at": 1234567890
    }
  ],
  "total": 1
}
```

**3. Get Task Details**
```bash
GET /api/tasks/{task_id}

Response:
{
  "success": true,
  "task": {
    "task_id": "task_abc123",
    "description": "...",
    "status": "completed",
    "steps": [...],  // Last 20 steps
    "answer": "Script created and tested successfully",
    "execution_time": 45.2
  }
}
```

**4. Stop Task**
```bash
POST /api/tasks/{task_id}/stop

Response:
{
  "success": true,
  "message": "Task stopped"
}
```

**5. Stream Logs (SSE)**
```bash
GET /api/tasks/stream/{task_id}

# Server-Sent Events stream
data: {"timestamp": 123, "level": "info", "message": "Starting task..."}
data: {"timestamp": 124, "level": "info", "message": "Executing step 1..."}
data: {"status": "complete", "final_status": "completed"}
```

### Reflection Endpoints

**1. Get Reflections**
```bash
GET /api/reflections?status=success&limit=50

Response:
{
  "success": true,
  "reflections": [
    {
      "task_id": "task_abc123",
      "description": "...",
      "status": "success",
      "what_worked": "...",
      "what_failed": "...",
      "lessons_learned": "...",
      "execution_time": 45.2,
      "timestamp": "2025-10-23T12:00:00Z"
    }
  ],
  "total": 50
}
```

**2. Get Metrics**
```bash
GET /api/reflections/metrics

Response:
{
  "success": true,
  "metrics": {
    "task_success_rate": 75.5,
    "target_success_rate": 70.0,
    "mean_time_to_result": 8.2,
    "target_mtr": 10.0,
    "hallucination_rate": 2.1,
    "target_hallucination": 0.0,
    "tool_use_accuracy": 92.3,
    "target_tool_accuracy": 90.0
  },
  "summary": {
    "total_reflections": 100,
    "successful": 75,
    "failed": 25
  }
}
```

## KPIs and Targets

| Metric | Target | Description |
|--------|--------|-------------|
| Task Success Rate | ≥70% | Percentage of tasks completed without manual intervention |
| Mean Time to Result (MTR) | <10 min | Average time from task start to completion |
| Tool Use Accuracy | ≥90% | Percentage of correct tool calls on first attempt |
| Hallucination Rate | →0% | Percentage of incorrect/hallucinatedinformation in reports |
| RAG Hit@5 | >80% | Percentage of queries where relevant docs are in top 5 results |

## Installation

### 1. Install Dependencies

```bash
cd mirai-agent

# Core dependencies
pip install -r requirements.txt

# Optional: FAISS RAG
pip install faiss-cpu sentence-transformers

# Optional: Browser automation
pip install beautifulsoup4 pypdf

# Optional: Playwright (alternative to Chrome)
pip install playwright
playwright install chromium
```

### 2. Install Ollama (Optional, for local LLM)

```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull mistral:7b
# or
ollama pull llama2:7b

# Verify
ollama list
```

### 3. Install Docker (Optional, for secure code execution)

```bash
# Linux
curl -fsSL https://get.docker.com | sh

# Verify
docker --version
```

### 4. Install Chrome/Chromium (Optional, for browser automation)

```bash
# Ubuntu/Debian
sudo apt install chromium-browser

# Or Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

## Running Tests

```bash
cd mirai-agent

# Run integration tests
python3 test_integration.py

# Run specific component tests
python3 core/tool_validator.py
python3 core/faiss_rag.py
python3 core/docker_runner.py
python3 core/browser_automation.py
python3 core/react_controller.py
python3 core/self_reflection.py
```

## Starting the Dashboard

```bash
cd mirai-agent

# Start dashboard server
python3 dashboard_server.py

# Access at http://localhost:5000
```

## Usage Examples

### Example 1: Execute Task via API

```python
import requests

# Start task
response = requests.post("http://localhost:5000/api/tasks/run", json={
    "description": "Create a Python function to check if a number is prime",
    "goal": "Write, test, and document the function",
    "max_steps": 10
})

task_id = response.json()["task_id"]
print(f"Task started: {task_id}")

# Check status
response = requests.get(f"http://localhost:5000/api/tasks/{task_id}")
task = response.json()["task"]
print(f"Status: {task['status']}")
print(f"Steps: {task['total_steps']}")
```

### Example 2: Index Knowledge Base

```python
from core.faiss_rag import FAISSRAGSystem

# Create RAG system
rag = FAISSRAGSystem()

# Index all markdown files
chunks_added = rag.add_documents_from_directory("knowledge_base/", "*.md")
print(f"Indexed {chunks_added} chunks")

# Save index
rag.save_index()
```

### Example 3: Execute Code Securely

```python
from core.docker_runner import DockerCodeRunner

runner = DockerCodeRunner()

# Execute untrusted code in isolated container
code = """
import sys
print(f"Python version: {sys.version}")
print("Hello from Docker!")
"""

result = runner.execute_python(code)

if result.status.value == "success":
    print(result.output)
else:
    print(f"Error: {result.error}")
```

### Example 4: Autonomous Task Execution

```python
from core.react_controller import ReActController, Task
from core.autonomous_agent import AutonomousAgent

# Create agent and controller
agent = AutonomousAgent()
controller = ReActController(agent.client, agent.tools)

# Register tools
controller.register_tool_handler("execute_python", agent.execute_python)
controller.register_tool_handler("search_web", agent.search_web)

# Execute task
task = Task(
    id="task_1",
    description="Find the weather in Paris and convert it to Fahrenheit",
    goal="Get current temperature in °F",
    max_steps=5
)

success, steps, answer = controller.execute_task(task)
print(f"Answer: {answer}")
```

## Security Considerations

1. **Docker Isolation**: Code runs in containers with no network access
2. **Memory Limits**: Prevents resource exhaustion
3. **Timeout Enforcement**: Prevents infinite loops
4. **Input Validation**: All tool calls are validated
5. **Sandbox Execution**: No direct filesystem access

## Troubleshooting

### Ollama Connection Failed
```bash
# Start Ollama service
systemctl start ollama

# Or run manually
ollama serve
```

### Docker Permission Denied
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Chrome/Chromium Not Found
```bash
# Install Chromium
sudo apt install chromium-browser

# Or set custom path
export CHROME_BIN=/usr/bin/chromium-browser
```

### FAISS Not Available
```bash
# Install FAISS
pip install faiss-cpu

# For GPU support (optional)
pip install faiss-gpu
```

## Future Enhancements

- [ ] LoRA fine-tuning pipeline
- [ ] Multi-agent collaboration
- [ ] Advanced error recovery
- [ ] Proactive task suggestions
- [ ] Code generation from specifications
- [ ] Automated testing generation
- [ ] Performance optimization suggestions
- [ ] Security vulnerability detection

## License

MIT License - See LICENSE file for details.

## Support

- Issues: [GitHub Issues](https://github.com/AgeeKey/Mirai/issues)
- Documentation: This file
- Dashboard: http://localhost:5000
