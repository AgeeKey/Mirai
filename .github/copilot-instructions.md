# GitHub Copilot Instructions for MIRAI Project

This file helps GitHub Copilot understand the project context and generate better code.

## Project Overview

- **Name**: MIRAI AI Trading Agent
- **Purpose**: Autonomous AI agent for trading and continuous improvement
- **Key Agents**: KAIZEN (改善) and MIRAI (未来)

## Architecture

### Core Components

- `autonomous_agent.py` - Base AI agent using OpenAI GPT-4o-mini
- `autonomous_service.py` - Background service for KAIZEN × MIRAI collaboration
- `kaizen_terminal.py` - Interactive terminal interface
- `cicd_monitor.py` - GitHub Actions monitoring
- `dashboard_server.py` - Flask web dashboard

### Multi-Language Support

Supports 8 languages: Python, JavaScript, TypeScript, C, C++, Go, Rust, Bash

- Executor: `multi_language_executor.py`

### Database Support

- SQLite, PostgreSQL, MongoDB, Redis
- Manager: `database_manager.py`

### GitHub Integration

- Full GitHub API integration
- Token stored in `configs/api_keys.json`
- Integration: `github_integration.py`

## Coding Standards

### Python Style

- Use type hints
- Async/await for I/O operations
- Rich library for terminal output
- Logging to `/tmp/` for services
- Follow PEP 8

### AI Agent Patterns

```python
# Always use this pattern for AI calls
from core.autonomous_agent import AutonomousAgent

agent = AutonomousAgent()
response = agent.think("Your question", max_iterations=1)
```

### Error Handling

```python
# Graceful error handling with logging
try:
    result = risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    return None
```

### Async Operations

```python
# Use async for I/O
async def monitor_loop():
    while running:
        await check_status()
        await asyncio.sleep(60)
```

## File Locations

### Configuration

- API Keys: `/root/mirai/mirai-agent/configs/api_keys.json`
- Logs: `/tmp/kaizen_mirai.log`
- Metrics: `/tmp/kaizen_mirai_metrics.jsonl`

### Services

- Dashboard: `http://localhost:5000`
- Autonomous Service PID: `/tmp/autonomous_service.pid`

## Common Tasks

### Adding New Tool to Agent

```python
# In autonomous_agent.py, add to tools list:
{
    "type": "function",
    "function": {
        "name": "your_tool_name",
        "description": "What it does",
        "parameters": {
            "type": "object",
            "properties": {
                "param": {"type": "string"}
            }
        }
    }
}

# Implement method:
def your_tool_name(self, param: str) -> str:
    """Implementation"""
    pass
```

### Creating New Monitor

```python
# Use CICDMonitor as template
class NewMonitor:
    def __init__(self, config):
        self.config = config

    def check_health(self) -> Dict:
        """Return health status"""
        pass

    def generate_report(self) -> str:
        """Generate text report"""
        pass
```

### Adding Terminal Command

```python
# In kaizen_terminal.py:
def cmd_your_command(self):
    """Your command implementation"""
    self.console.print("[bold]Your output[/bold]")

# Add to process_command():
elif cmd == 'your_command':
    self.cmd_your_command()
```

## Naming Conventions

### Agents

- KAIZEN (改善) - Executor, implementation agent
- MIRAI (未来) - Advisor, strategic decision maker

### Files

- `*_agent.py` - AI agent implementations
- `*_monitor.py` - Monitoring systems
- `*_server.py` - Web servers
- `*_terminal.py` - Terminal interfaces

### Variables

- `kaizen` - KAIZEN agent instance
- `mirai` - MIRAI agent instance
- `monitor` - Monitoring instance
- `health` - Health check results
- `metrics` - Performance metrics

## Testing

### Run Tests

```bash
cd /root/mirai/mirai-agent
source venv/bin/activate
pytest tests/
```

### CI/CD

- Repository: `mirai-showcase`
- Workflows: `.github/workflows/ci-cd.yml`, `multi-language.yml`

## Special Instructions

### When creating new features:

1. Follow autonomous agent pattern
2. Add logging
3. Handle errors gracefully
4. Update this file with new patterns
5. Add terminal command if user-facing

### When working with AI:

- Always use `AutonomousAgent().think()`
- Set reasonable `max_iterations` (1-3)
- Log AI responses
- Handle API errors

### When adding integrations:

- Store credentials in `configs/api_keys.json`
- Create manager class (like `GitHubIntegration`)
- Add to `autonomous_agent.py` tools if needed

## Emojis Convention

- 🤖 KAIZEN
- 🌸 MIRAI
- ✅ Success
- ❌ Failure
- ⏳ In Progress
- 📊 Metrics/Data
- 🔍 Analysis
- 💡 Suggestion
- 🚀 Launch/Start
- 🛑 Stop

## Remember

- MIRAI works autonomously in background
- KAIZEN provides interactive terminal interface
- Always log important events
- Use rich/panel for beautiful terminal output
- Metrics go to `/tmp/kaizen_mirai_metrics.jsonl`
