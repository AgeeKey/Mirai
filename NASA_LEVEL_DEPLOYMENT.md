# 🚀 NASA-Level Learning System - Deployment Guide

Complete guide for installing, configuring, and using the NASA-Level Learning System.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage Guide](#usage-guide)
5. [API Reference](#api-reference)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Topics](#advanced-topics)

---

## 🖥️ System Requirements

### Hardware

- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 10GB free space
- **Network**: Internet connection for AI API calls

### Software

- **OS**: Linux (Ubuntu 20.04+, Debian 11+, or compatible)
- **Python**: 3.10+ (tested on 3.12)
- **Docker**: 20.10+ (for sandbox execution)
- **SQLite**: 3.35+ (for FTS5 support)

### Required Python Packages

```
openai>=1.0.0
radon>=6.0.0
pylint>=3.0.0
prometheus-client>=0.19.0
```

---

## 📦 Installation

### Step 1: Clone Repository

```bash
cd /root
git clone https://github.com/AgeeKey/mirai.git
cd mirai/mirai-agent
```

### Step 2: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install openai radon pylint prometheus-client
```

### Step 3: Install Docker (if not already installed)

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Logout and login again for group changes to take effect
```

### Step 4: Configure API Keys

```bash
# Edit configs/api_keys.json
nano configs/api_keys.json
```

Add your OpenAI API key:

```json
{
  "openai_api_key": "sk-your-key-here"
}
```

### Step 5: Verify Installation

```bash
# Test all components
python3 test_complete_nasa_system.py
```

Expected output:
```
✅ SUCCESS! Learned in ~25s
   Proficiency: ~85%
   Quality Grade: B
   Tests Passed: 100%
```

---

## ⚙️ Configuration

### Database Locations

Default locations (can be customized):

```python
# Knowledge database
knowledge_db = "/tmp/nasa_knowledge.db"

# Metrics
metrics_file = "/tmp/nasa_metrics.jsonl"

# Pipeline state
pipeline_state = "/tmp/learning_pipeline_state.json"
```

### Learning Parameters

```python
# In orchestrator.py or your integration

# Concurrency
max_concurrent = 2  # Number of simultaneous learning tasks

# Retry settings
max_retries = 3     # Attempts before giving up
retry_delay = 2**n  # Exponential backoff (2, 4, 8 seconds)

# Quality threshold
min_quality = 0.6   # Minimum quality score to accept
```

### Docker Configuration

```python
# In sandbox_executor.py

# Resource limits
memory_limit = "512m"
cpu_limit = 1.0

# Execution timeout
timeout = 30  # seconds
```

---

## 📖 Usage Guide

### Command Line Interface

The orchestrator provides a CLI for manual control:

#### Learn Immediately

```bash
python3 core/nasa_level/orchestrator.py learn \
    --tech requests \
    --depth basic

# Depth options: basic, intermediate, advanced
```

#### Queue for Later

```bash
python3 core/nasa_level/orchestrator.py queue \
    --tech pandas \
    --priority high

# Priority: critical, high, normal, low
```

#### Check Status

```bash
python3 core/nasa_level/orchestrator.py status
```

Output:
```
📊 SYSTEM STATUS

Pipeline: {'running': False, 'queue_size': 0, 'completed': 3}
Knowledge: {'unique_technologies': 4, 'total_entries': 4}
Metrics: {'success_rate': 1.0, 'avg_proficiency': 0.849}
```

#### Generate Report

```bash
python3 core/nasa_level/orchestrator.py report
```

#### Search Knowledge

```bash
python3 core/nasa_level/orchestrator.py search --query "HTTP"
```

### Python API

#### Basic Usage

```python
from core.nasa_level import NASALearningOrchestrator

# Initialize
orchestrator = NASALearningOrchestrator()

# Learn a technology
result = orchestrator.learn_technology("requests", depth="basic")

if result.success:
    print(f"Learned! Proficiency: {result.proficiency:.1%}")
else:
    print(f"Failed: {result.errors}")
```

#### Async Pipeline

```python
import asyncio
from core.nasa_level import NASALearningOrchestrator, Priority

async def main():
    orchestrator = NASALearningOrchestrator()
    
    # Add tasks to queue
    orchestrator.queue_learning("requests", priority=Priority.HIGH)
    orchestrator.queue_learning("pandas", priority=Priority.NORMAL)
    orchestrator.queue_learning("flask", priority=Priority.LOW)
    
    # Process queue
    await orchestrator.start_pipeline()

asyncio.run(main())
```

#### Knowledge Search

```python
# Search knowledge base
results = orchestrator.search_knowledge("HTTP requests authentication")

for r in results:
    print(f"{r.technology} v{r.version}")
    print(f"Grade: {r.quality_grade}, Proficiency: {r.proficiency:.1%}")
    print(f"Code:\n{r.code}\n")
```

#### Export Knowledge

```python
# Export specific technology
data = orchestrator.knowledge_manager.export_knowledge("requests")

# Save to file
import json
with open("requests_knowledge.json", "w") as f:
    json.dump(data, f, indent=2)
```

#### Get Metrics

```python
# Get summary
summary = orchestrator.metrics.get_summary()
print(f"Success rate: {summary['overall_success_rate']:.1%}")

# Get top technologies
top = orchestrator.metrics.get_top_technologies(5)
for tech in top:
    print(f"{tech['technology']}: {tech['proficiency']:.1%}")

# Generate full report
report = orchestrator.metrics.generate_report()
print(report)
```

---

## 🔌 API Reference

### NASALearningOrchestrator

Main interface to the system.

#### Methods

##### `learn_technology(technology, depth='basic')`

Learn a single technology synchronously.

**Parameters:**
- `technology` (str): Technology name (e.g., "requests")
- `depth` (str): Learning depth - "basic", "intermediate", or "advanced"

**Returns:** `LearningResult` object

```python
result = orchestrator.learn_technology("requests")
print(result.proficiency)  # 0.85
print(result.quality_grade)  # "B"
print(result.tests_passed)  # 1
```

##### `queue_learning(technology, depth='basic', priority=Priority.NORMAL)`

Add technology to learning queue.

**Parameters:**
- `technology` (str): Technology name
- `depth` (str): Learning depth
- `priority` (Priority): CRITICAL, HIGH, NORMAL, or LOW

```python
from core.nasa_level import Priority

orchestrator.queue_learning("pandas", priority=Priority.HIGH)
```

##### `async start_pipeline()`

Start processing the learning queue (async).

```python
await orchestrator.start_pipeline()
```

##### `get_status()`

Get current system status.

**Returns:** Dict with pipeline, knowledge, and metrics status

```python
status = orchestrator.get_status()
print(status['metrics']['success_rate'])
```

##### `search_knowledge(query)`

Search knowledge base.

**Parameters:**
- `query` (str): Search query

**Returns:** List of `KnowledgeEntry` objects

```python
results = orchestrator.search_knowledge("HTTP")
```

##### `get_learned_technologies()`

Get list of all learned technologies.

**Returns:** List of technology names

```python
techs = orchestrator.get_learned_technologies()
```

##### `generate_report()`

Generate comprehensive system report.

**Returns:** String with formatted report

```python
report = orchestrator.generate_report()
print(report)
```

### LearningResult

Result object from learning operations.

**Attributes:**
- `technology` (str): Technology name
- `success` (bool): Whether learning succeeded
- `proficiency` (float): 0.0-1.0 proficiency score
- `quality_grade` (str): A, B, C, D, or F
- `tests_passed` (int): Number of tests passed
- `tests_total` (int): Total number of tests
- `execution_time` (float): Time taken in seconds
- `errors` (List[str]): List of errors if failed
- `suggestions` (List[str]): Improvement suggestions
- `artifacts` (List[LearningArtifact]): Learning artifacts from each phase

### Priority Enum

Priority levels for queued tasks.

```python
from core.nasa_level import Priority

Priority.CRITICAL  # 1 - Must learn immediately
Priority.HIGH      # 2 - Important features
Priority.NORMAL    # 3 - Regular learning
Priority.LOW       # 4 - Nice to have
```

---

## 📊 Monitoring

### Prometheus Integration

The system exports Prometheus metrics on port 8000 (configurable).

#### Start Metrics Server

```python
from prometheus_client import start_http_server

# Start metrics endpoint
start_http_server(8000)
```

#### Available Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `nasa_learning_attempts_total` | Counter | Total learning attempts |
| `nasa_learning_success_total` | Counter | Successful learnings |
| `nasa_learning_failures_total` | Counter | Failed attempts |
| `nasa_learning_duration_seconds` | Histogram | Learning duration |
| `nasa_proficiency_score` | Gauge | Current proficiency by tech |
| `nasa_quality_score` | Gauge | Current quality score |
| `nasa_active_learning_tasks` | Gauge | Currently active tasks |
| `nasa_knowledge_base_size` | Gauge | Total learned technologies |

#### Query Examples

```promql
# Success rate
rate(nasa_learning_success_total[5m]) / 
rate(nasa_learning_attempts_total[5m])

# Average learning time
rate(nasa_learning_duration_seconds_sum[5m]) / 
rate(nasa_learning_duration_seconds_count[5m])

# Top technologies by proficiency
topk(10, nasa_proficiency_score)
```

### Logging

Configure logging level:

```python
import logging

logging.basicConfig(
    level=logging.INFO,  # or DEBUG, WARNING, ERROR
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

Log locations:
- `/tmp/kaizen_mirai.log` - Service logs
- `/tmp/nasa_metrics.jsonl` - Metrics history
- `/tmp/learning_pipeline_state.json` - Pipeline state

---

## 🔧 Troubleshooting

### Problem: "Docker permission denied"

**Solution:**
```bash
sudo usermod -aG docker $USER
# Logout and login again
```

### Problem: "OpenAI API key not found"

**Solution:**
```bash
# Check config file
cat configs/api_keys.json

# Set environment variable
export OPENAI_API_KEY="sk-your-key-here"
```

### Problem: "Learning quality too low"

The system automatically retries if quality < 0.6. If still failing:

**Solutions:**
1. Try different depth: `--depth basic` (easier)
2. Check internet connection (AI needs to research)
3. Check OpenAI API status
4. Increase timeout in `sandbox_executor.py`

### Problem: "Docker not found"

**Solution:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Problem: "Database locked"

**Solution:**
```bash
# Close other connections
fuser /tmp/nasa_knowledge.db
# Or delete and recreate
rm /tmp/nasa_knowledge.db
```

### Problem: "Memory errors during learning"

**Solutions:**
1. Reduce `max_concurrent` in pipeline
2. Increase Docker memory limit
3. Clear old knowledge: `rm /tmp/nasa_knowledge.db`

### Enable Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will show:
- AI prompts and responses
- Sandbox execution details
- Quality analysis breakdown
- Pipeline state changes

---

## 🎓 Advanced Topics

### Custom Quality Thresholds

```python
# In advanced_learning.py, modify:
MIN_QUALITY_THRESHOLD = 0.7  # Stricter (default 0.6)
```

### Custom Security Patterns

```python
# In sandbox_executor.py, add to BLACKLIST_PATTERNS:
BLACKLIST_PATTERNS = [
    # ... existing patterns ...
    r'requests\.get\(',  # Block HTTP requests
    r'open\(.*[\'"]w',   # Block file writes
]
```

### Integration with Existing Code

```python
# In your autonomous_service.py

from core.nasa_level import NASALearningOrchestrator

class AutonomousService:
    def __init__(self):
        # ... existing init ...
        self.nasa_learning = NASALearningOrchestrator()
    
    def self_improve(self):
        """Replace old method with NASA system"""
        # Identify technology to learn
        technology = self.identify_learning_need()
        
        # Learn it
        result = self.nasa_learning.learn_technology(
            technology,
            depth="basic"
        )
        
        if result.success:
            self.log(f"Learned {technology}: {result.proficiency:.1%}")
        else:
            self.log(f"Failed to learn {technology}: {result.errors}")
        
        return result.success
```

### Custom Learning Phases

Extend `AdvancedLearningEngine` to add custom phases:

```python
from core.nasa_level import AdvancedLearningEngine

class CustomLearningEngine(AdvancedLearningEngine):
    def learn_technology(self, technology, depth):
        # Call parent
        result = super().learn_technology(technology, depth)
        
        # Add custom phase
        if result.success:
            self._custom_optimization_phase(result)
        
        return result
    
    def _custom_optimization_phase(self, result):
        # Your custom logic here
        pass
```

---

## 📝 Best Practices

### 1. Start with Basic Depth

Always start learning with `depth="basic"` before moving to intermediate/advanced.

### 2. Use Priorities Wisely

- `CRITICAL`: Security fixes, system failures
- `HIGH`: Core features needed soon
- `NORMAL`: Regular learning tasks
- `LOW`: Nice-to-have improvements

### 3. Monitor Metrics

Set up Prometheus + Grafana for visual dashboards:

```bash
# Install Grafana
docker run -d -p 3000:3000 grafana/grafana

# Configure datasource: http://localhost:8000
```

### 4. Regular Backups

```bash
# Backup knowledge base
cp /tmp/nasa_knowledge.db /backup/nasa_knowledge_$(date +%Y%m%d).db

# Backup metrics
cp /tmp/nasa_metrics.jsonl /backup/
```

### 5. Clean Old Data

```python
# Remove old versions, keep latest
orchestrator.knowledge_manager.cleanup_old_versions(keep=1)
```

---

## 🆘 Support

- **Documentation**: This file and NASA_LEVEL_ARCHITECTURE_PLAN.md
- **Issues**: GitHub Issues on mirai repository
- **Code**: All source in `core/nasa_level/`
- **Tests**: `test_nasa_learning.py`, `test_complete_nasa_system.py`

---

## 📄 License

Same as MIRAI project - see LICENSE file in root.

---

**Last Updated**: October 13, 2025  
**Version**: 1.0.0  
**Status**: Production Ready
