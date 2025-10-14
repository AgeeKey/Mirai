#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI - Unified Entry Point                                        ║
║  Single Command-Line Interface for All Operational Modes           ║
╚══════════════════════════════════════════════════════════════════════╝

Version: 2.0.0
Codename: Evolution

Этот файл объединяет все режимы работы MIRAI:
- 🤖 Terminal (KAIZEN) - Interactive CLI
- 📊 Dashboard - Web UI
- 🔄 Autonomous - Background service
- 💬 Ask - Single question mode

Usage:
    python3 mirai.py --mode terminal
    python3 mirai.py --mode dashboard --port 5000
    python3 mirai.py --mode autonomous
    python3 mirai.py --mode ask "What is AI?"
    python3 mirai.py --version
    python3 mirai.py --health
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
mirai_agent_root = project_root / "mirai-agent"
sys.path.insert(0, str(mirai_agent_root))
sys.path.insert(0, str(project_root))

# Import core modules
try:
    from core.autonomous_agent import AutonomousAgent
    from core.config_loader import get_api_key, get_config
except ImportError as e:
    print(f"❌ Error: core modules not found: {e}")
    print("Make sure you're in the mirai-agent directory")
    sys.exit(1)

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Добавить путь к модулям
sys.path.insert(0, str(Path(__file__).parent / "mirai-agent"))

# ASCII Art Banner
BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ███╗   ███╗██╗██████╗  █████╗ ██╗                             ║
║   ████╗ ████║██║██╔══██╗██╔══██╗██║                             ║
║   ██╔████╔██║██║██████╔╝███████║██║                             ║
║   ██║╚██╔╝██║██║██╔══██╗██╔══██║██║                             ║
║   ██║ ╚═╝ ██║██║██║  ██║██║  ██║██║                             ║
║   ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝                             ║
║                                                                  ║
║   🌸 Autonomous AI Agent with Memory & Self-Evolution           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

VERSION = "2.0.0"
CODENAME = "Evolution"


def load_identity():
    """Загрузить информацию о MIRAI"""
    identity_file = (
        Path(__file__).parent / "mirai-agent" / "data" / "mirai_identity.json"
    )

    if identity_file.exists():
        with open(identity_file, "r") as f:
            return json.load(f)

    # Дефолтная идентичность
    return {
        "name": "MIRAI",
        "version": VERSION,
        "codename": CODENAME,
        "created_at": datetime.now().isoformat(),
        "capabilities": [
            "multi_language_coding",
            "autonomous_operation",
            "github_integration",
            "database_management",
            "long_term_memory",
            "self_evolution",
        ],
    }


def show_version():
    """Показать версию и информацию о MIRAI"""
    identity = load_identity()

    print(BANNER)
    print(f"Version: {identity['version']}")
    print(f"Codename: {identity['codename']}")
    print(f"Created: {identity.get('created_at', 'Unknown')}")
    print()
    print("Capabilities:")
    for cap in identity.get("capabilities", []):
        print(f"  • {cap.replace('_', ' ').title()}")
    print()
    print("Modes:")
    print("  • terminal   - Interactive terminal (KAIZEN)")
    print("  • dashboard  - Web dashboard (port 5000)")
    print("  • autonomous - Background service")
    print("  • ask        - Single question mode")
    print()


def run_terminal():
    """Запустить интерактивный терминал"""
    print(BANNER)
    print("🌸 Starting MIRAI Terminal (KAIZEN Mode)...")
    print()

    # Импорт и запуск kaizen_terminal
    try:
        from kaizen_terminal import KaizenTerminal

        terminal = KaizenTerminal()
        terminal.run()
    except ImportError as e:
        print(f"❌ Error: Failed to import kaizen_terminal: {e}")
        print("📝 Make sure you're in the correct directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting terminal: {e}")
        sys.exit(1)


def run_dashboard(host="0.0.0.0", port=5000):
    """Запустить веб-дашборд"""
    print(BANNER)
    print(f"🌸 Starting MIRAI Dashboard on http://{host}:{port}")
    print()

    try:
        from dashboard_server import app

        app.run(host=host, port=port, debug=False)
    except ImportError as e:
        print(f"❌ Error: Failed to import dashboard_server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        sys.exit(1)


def run_autonomous():
    """Запустить автономный режим"""
    print(BANNER)
    print("🌸 Starting MIRAI Autonomous Service...")
    print()

    try:
        from autonomous_service import AutonomousService

        service = AutonomousService()
        service.run()
    except ImportError as e:
        print(f"❌ Error: Failed to import autonomous_service: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting autonomous mode: {e}")
        sys.exit(1)


def ask_question(question: str):
    """Задать разовый вопрос"""
    print(BANNER)
    print(f"🌸 Question: {question}")
    print()

    try:
        from core.autonomous_agent import AutonomousAgent

        agent = AutonomousAgent()

        print("🤔 Thinking...")
        response = agent.think(question, max_iterations=1)

        print()
        print("🌸 MIRAI Answer:")
        print("─" * 70)
        print(response)
        print("─" * 70)

    except ImportError as e:
        print(f"❌ Error: Failed to import AutonomousAgent: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error processing question: {e}")
        sys.exit(1)


def check_health():
    """Проверить состояние системы"""
    print(BANNER)
    print("🔍 MIRAI System Health Check")
    print("=" * 70)
    print()

    checks = []

    # Check 1: Python version
    import sys

    py_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    checks.append(("Python", py_version, True))

    # Check 2: Core modules
    try:
        from core.autonomous_agent import AutonomousAgent

        checks.append(("Core Module", "AutonomousAgent", True))
    except:
        checks.append(("Core Module", "AutonomousAgent", False))

    # Check 3: OpenAI API Key (using new config loader)
    try:
        api_key = get_api_key()
        if api_key:
            source = "env" if os.getenv("OPENAI_API_KEY") else "config"
            checks.append(("API Key", f"Set ({source})", True))
        else:
            checks.append(("API Key", "Not found", False))
    except Exception as e:
        checks.append(("API Key", f"Error: {e}", False))

    # Check 4: Config file (new unified config)
    try:
        config = get_config()
        checks.append(("Config", f"v{config.version} ({config.codename})", True))
    except Exception as e:
        checks.append(("Config", f"Error: {e}", False))

    # Check 5: Memory database (using config + actual test)
    try:
        from core.memory_manager import MemoryManager

        config = get_config()
        db_file = Path(config.memory.db_path)

        # Try to initialize memory manager
        mm = MemoryManager(str(db_file))
        stats = mm.get_stats()

        checks.append(
            (
                "Memory DB",
                f"{stats['total_sessions']} sessions, {stats['total_messages']} msgs",
                True,
            )
        )
    except Exception as e:
        checks.append(("Memory DB", f"Error: {e}", False))

    # Check 6: Logger (new structured logger)
    try:
        from core.logger import MiraiLogger

        config = get_config()
        log_path = config.monitoring.logs.get("path", "/tmp/mirai.log")

        # Try to initialize logger
        test_logger = MiraiLogger(name="healthcheck", log_file=log_path, level="INFO")

        checks.append(("Logger", f"Ready ({Path(log_path).name})", True))
    except Exception as e:
        checks.append(("Logger", f"Error: {e}", False))

    # Print results
    all_ok = True
    for name, value, status in checks:
        icon = "✅" if status else "❌"
        print(f"{icon} {name:20} {value}")
        if not status:
            all_ok = False

    print()
    if all_ok:
        print("🎉 All systems operational!")
        return 0
    else:
        print("⚠️  Some components need attention")
        return 1


def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(
        description="MIRAI - Autonomous AI Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 mirai.py --mode terminal          # Interactive terminal
  python3 mirai.py --mode dashboard         # Web dashboard
  python3 mirai.py --mode autonomous        # Background service
  python3 mirai.py --mode ask "What is AI?" # Single question
  python3 mirai.py --version                # Show version
  python3 mirai.py --health                 # Health check
        """,
    )

    parser.add_argument(
        "--mode",
        choices=["terminal", "dashboard", "autonomous", "ask"],
        help="Operation mode",
    )

    parser.add_argument("question", nargs="?", help="Question for ask mode")

    parser.add_argument(
        "--version", action="store_true", help="Show version information"
    )

    parser.add_argument("--health", action="store_true", help="Run health check")

    parser.add_argument(
        "--host", default="0.0.0.0", help="Dashboard host (default: 0.0.0.0)"
    )

    parser.add_argument(
        "--port", type=int, default=5000, help="Dashboard port (default: 5000)"
    )

    args = parser.parse_args()

    # Show version
    if args.version:
        show_version()
        return 0

    # Health check
    if args.health:
        return check_health()

    # No mode specified
    if not args.mode:
        show_version()
        print("❌ Error: Please specify --mode")
        print()
        parser.print_help()
        return 1

    # Run modes
    if args.mode == "terminal":
        run_terminal()

    elif args.mode == "dashboard":
        run_dashboard(host=args.host, port=args.port)

    elif args.mode == "autonomous":
        run_autonomous()

    elif args.mode == "ask":
        if not args.question:
            print("❌ Error: Question required for ask mode")
            print('Example: python3 mirai.py --mode ask "What is AI?"')
            return 1
        ask_question(args.question)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n🌸 MIRAI shutting down... Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
