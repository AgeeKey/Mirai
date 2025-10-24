# GitHub Copilot Instructions for MIRAI Project

This file helps GitHub Copilot understand the project context and generate better code.

## Project Overview

- **Name**: MIRAI V3 SUPERAGENT
- **Purpose**: Autonomous AI agent with vision, reasoning, planning, execution, browser automation, application control, and learning capabilities
- **Architecture**: 7-phase modular system (Vision → Reasoning → Planning → Execution → Browser → Apps → Memory)
- **Original Legacy**: Trading agent KAIZEN (改善) and MIRAI (未来)

## Architecture

### MIRAI V3 SUPERAGENT - 7 Phase System

The project is organized into **7 complete phases**, each with 100-150 implementation steps:

**Phase 1: Vision System** (`MIRAI_V3_SUPERAGENT/01_VISION_SYSTEM/`)
- Screenshot capture and analysis using GPT-4 Vision API
- Element detection (buttons, inputs, menus) with OpenCV
- Problem detection (ads, popups, errors)
- Scene understanding and recommendations
- Main modules: `vision_complete.py`, `vision_tests.py`
- 8 files, ~5,400 lines of code

**Phase 2: Reasoning Engine** (`mirai-agent/core/reasoning_engine/`)
- Context processing and decision making
- Intelligent planning with preference management
- Risk assessment and memory system
- Main modules: `decision_maker.py`, `context_processor.py`, `intelligent_planner.py`
- 6 modules, ~3,900 lines

**Phase 3: Task Planning** (`mirai-agent/core/task_planning/`)
- Task decomposition into atomic steps
- Sequential and parallel planning strategies
- Optimization and validation
- Main modules: `task_decomposition.py`, `sequential_planning.py`, `main_planner.py`
- 6 modules, ~4,200 lines

**Phase 4: Action Execution** (`mirai-agent/core/action_execution/`)
- Multi-platform action execution (keyboard, mouse, filesystem)
- Browser and application actions
- Error recovery and rollback system
- Safety guards and performance tracking
- Main modules: `action_executor.py`, `browser_actions.py`, `file_system_actions.py`
- 14 modules, ~3,100 lines

**Phase 5: Browser Automation** (`mirai-agent/core/browser_automation/`)
- Multi-browser support (Chrome, Firefox, Edge, Brave, Opera)
- Profile management and session persistence
- CDP-based navigation
- Main modules: `browser_detection.py`, `navigation.py`, `profile_management.py`
- 4 modules, ~2,800 lines

**Phase 6: Application Control** (`mirai-agent/core/phase6/`)
- Desktop application management (VSCode, CapCut, File Explorer, System apps)
- Application detection, launch, and monitoring
- Error handling and auto-recovery
- Multi-app coordination
- Main modules: `application_manager.py`, `vscode_controller.py`, `capcut_controller.py`
- 12 modules, ~4,200 lines

**Phase 7: Memory & Learning** (`MIRAI_V3_SUPERAGENT/07_MEMORY_AND_LEARNING/`)
- 6 types of memory: Short-term, Long-term, Episodic, Semantic, Procedural, Working
- Experience recording and pattern detection
- Learning engine and knowledge graph
- Memory consolidation and retrieval
- Main modules: `memory_complete.py`, `memory_tests.py`
- 7 modules, ~5,500 lines

### Legacy Components (Trading Agent)

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

### Working with Vision System (Phase 1)

```python
from MIRAI_V3_SUPERAGENT.vision_complete import initialize_vision_system

# Initialize vision system
vision = initialize_vision_system()

# Capture and analyze screen
result = vision.analyze_screen()
print(f"Scene: {result['scene_description']}")
print(f"Elements detected: {len(result['elements'])}")
```

### Working with Reasoning Engine (Phase 2)

```python
from mirai-agent.core.reasoning_engine import DecisionMaker, ContextProcessor

# Initialize reasoning
decision_maker = DecisionMaker()
context_processor = ContextProcessor()

# Process context and make decision
context = context_processor.process_user_input("Open browser and search")
decision = decision_maker.make_decision(context)
```

### Working with Task Planning (Phase 3)

```python
from mirai-agent.core.task_planning import TaskDecomposer, SequentialPlanner

# Decompose task into steps
decomposer = TaskDecomposer()
steps = decomposer.decompose("Create Python script and test it")

# Create sequential plan
planner = SequentialPlanner()
plan = planner.create_plan(steps)
```

### Working with Action Execution (Phase 4)

```python
from mirai-agent.core.action_execution import ActionExecutor

# Execute actions
executor = ActionExecutor()
result = executor.execute_action({
    "type": "file_system",
    "action": "create_file",
    "params": {"path": "test.py", "content": "print('hello')"}
})
```

### Working with Browser Automation (Phase 5)

```python
from mirai-agent.core.browser_automation import BrowserDetector, NavigationController

# Detect and launch browser
detector = BrowserDetector()
browsers = detector.detect_browsers()
browser = detector.launch_browser("chrome", headless=False)

# Navigate
nav = NavigationController(browser)
nav.navigate_to("https://example.com")
```

### Working with Application Control (Phase 6)

```python
from mirai-agent.core.phase6 import ApplicationManager, VSCodeController

# Detect and launch application
app_manager = ApplicationManager()
vscode = app_manager.get_controller("vscode")
vscode.launch()
vscode.open_file("script.py")
vscode.run_code()
```

### Working with Memory & Learning (Phase 7)

```python
from MIRAI_V3_SUPERAGENT.memory_complete import initialize_memory_system

# Initialize memory
memory = initialize_memory_system()

# Record experience
memory.experience_recorder.record_experience(
    event={"type": "user_request"},
    action={"type": "open_browser"},
    result={"success": True}
)

# Learn from experience
memory.learning_engine.learn_from_patterns()
```

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
