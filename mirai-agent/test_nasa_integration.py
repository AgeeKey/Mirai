#!/usr/bin/env python3
"""
🧪 NASA-Level Integration Test
Тестирует все компоненты интеграции:
- autonomous_service с NASA обучением
- dashboard с NASA endpoints
- systemd готовность
"""

import sys
import time
import requests
from pathlib import Path

sys.path.insert(0, "/root/mirai/mirai-agent")

# Цветной вывод
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def test_header(title):
    print(f"\n{'='*70}")
    print(f"{BLUE}{title}{RESET}")
    print("=" * 70)


def test_result(name, success, details=""):
    icon = f"{GREEN}✅{RESET}" if success else f"{RED}❌{RESET}"
    print(f"{icon} {name}")
    if details:
        print(f"   {details}")
    return success


def main():
    print(
        """
╔══════════════════════════════════════════════════════════════════════╗
║  🧪 NASA-LEVEL INTEGRATION TEST                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """
    )

    results = []

    # ========================================================================
    # TEST 1: Imports & Initialization
    # ========================================================================
    test_header("TEST 1: Проверка импортов и инициализации")

    try:
        from core.nasa_level.orchestrator import NASALearningOrchestrator
        from core.autonomous_agent import AutonomousAgent

        results.append(
            test_result("Импорт NASALearningOrchestrator", True, "Модуль найден")
        )
    except ImportError as e:
        results.append(test_result("Импорт NASALearningOrchestrator", False, str(e)))
        return

    try:
        print("\n🚀 Инициализация NASA-Level системы...")
        nasa = NASALearningOrchestrator()
        results.append(test_result("Инициализация Orchestrator", True, "Создан успешно"))
    except Exception as e:
        results.append(test_result("Инициализация Orchestrator", False, str(e)))
        return

    # ========================================================================
    # TEST 2: Learning Functionality
    # ========================================================================
    test_header("TEST 2: Тестирование обучения")

    try:
        print("\n📚 Изучаем библиотеку 'os' (простой тест)...")
        result = nasa.learn_technology("os", depth="basic")

        if result.success:
            results.append(
                test_result(
                    "Обучение технологии 'os'",
                    True,
                    f"Proficiency: {result.proficiency:.1f}%, Grade: {result.quality_grade}",
                )
            )
        else:
            error_msg = result.errors[0] if result.errors else "Unknown error"
            results.append(test_result("Обучение технологии 'os'", False, error_msg))
    except Exception as e:
        results.append(test_result("Обучение технологии 'os'", False, str(e)))

    # ========================================================================
    # TEST 3: Knowledge Base
    # ========================================================================
    test_header("TEST 3: Проверка Knowledge Base")

    try:
        stats = nasa.knowledge_manager.get_stats()
        results.append(
            test_result(
                "Knowledge Base Stats",
                True,
                f"Entries: {stats['total_entries']}, Avg Proficiency: {stats.get('average_proficiency', 0):.1f}%",
            )
        )
    except Exception as e:
        results.append(test_result("Knowledge Base Stats", False, str(e)))

    try:
        technologies = nasa.get_learned_technologies()
        results.append(
            test_result(
                "Get Learned Technologies",
                len(technologies) > 0,
                f"Found {len(technologies)} technologies",
            )
        )
    except Exception as e:
        results.append(test_result("Get Learned Technologies", False, str(e)))

    # ========================================================================
    # TEST 4: Metrics
    # ========================================================================
    test_header("TEST 4: Проверка Metrics")

    try:
        status = nasa.get_status()
        metrics = status.get("metrics", {})
        results.append(
            test_result(
                "Metrics Summary",
                True,
                f"Success rate: {metrics.get('success_rate', 0):.1f}%",
            )
        )
    except Exception as e:
        results.append(test_result("Metrics Summary", False, str(e)))

    # ========================================================================
    # TEST 5: Dashboard Endpoints (если запущен)
    # ========================================================================
    test_header("TEST 5: Dashboard Endpoints (опционально)")

    print(
        "\n⚠️  Этот тест требует запущенный dashboard_server.py"
    )
    print("   Пропускаем если сервер не запущен...\n")

    dashboard_url = "http://localhost:5000"
    endpoints = [
        "/api/nasa/status",
        "/api/nasa/metrics",
        "/api/nasa/knowledge",
        "/api/nasa/report",
    ]

    try:
        # Проверяем доступность dashboard
        response = requests.get(f"{dashboard_url}/api/health", timeout=2)
        if response.status_code == 200:
            print(f"{GREEN}✓{RESET} Dashboard доступен!\n")

            for endpoint in endpoints:
                try:
                    resp = requests.get(f"{dashboard_url}{endpoint}", timeout=2)
                    success = resp.status_code == 200 and resp.json().get("success")
                    results.append(
                        test_result(
                            f"Endpoint {endpoint}", success, f"Status: {resp.status_code}"
                        )
                    )
                except Exception as e:
                    results.append(test_result(f"Endpoint {endpoint}", False, str(e)))
        else:
            print(f"{YELLOW}⊘{RESET} Dashboard не запущен, пропускаем endpoints")
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        print(f"{YELLOW}⊘{RESET} Dashboard не запущен, пропускаем endpoints")

    # ========================================================================
    # TEST 6: Systemd Files
    # ========================================================================
    test_header("TEST 6: Systemd Service Files")

    service_files = [
        Path("/root/mirai/mirai-agent/nasa-learning.service"),
        Path("/root/mirai/mirai-agent/nasa-dashboard.service"),
        Path("/root/mirai/mirai-agent/install_nasa_services.sh"),
    ]

    for file in service_files:
        exists = file.exists()
        results.append(test_result(f"File {file.name}", exists, str(file)))

    # ========================================================================
    # TEST 7: Autonomous Service Integration
    # ========================================================================
    test_header("TEST 7: Autonomous Service Integration")

    try:
        with open("/root/mirai/mirai-agent/autonomous_service.py") as f:
            content = f.read()
            has_import = "NASALearningOrchestrator" in content
            has_init = "self.nasa_learning" in content
            has_method = "def autonomous_learning" in content

            results.append(
                test_result(
                    "NASALearningOrchestrator импортирован",
                    has_import,
                    "Found in autonomous_service.py",
                )
            )
            results.append(
                test_result(
                    "NASA система инициализирована",
                    has_init,
                    "self.nasa_learning создан",
                )
            )
            results.append(
                test_result(
                    "Метод autonomous_learning() создан",
                    has_method,
                    "Найден в коде",
                )
            )
    except Exception as e:
        results.append(test_result("Autonomous Service Integration", False, str(e)))

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 70)
    print(f"{BLUE}📊 ИТОГОВАЯ СТАТИСТИКА{RESET}")
    print("=" * 70)

    total = len(results)
    passed = sum(results)
    failed = total - passed
    success_rate = (passed / total * 100) if total > 0 else 0

    print(f"\n✅ Passed: {GREEN}{passed}{RESET}")
    print(f"❌ Failed: {RED}{failed}{RESET}")
    print(f"📊 Success Rate: {success_rate:.1f}%")

    if success_rate == 100:
        print(f"\n{GREEN}🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!{RESET}")
        print(
            """
╔══════════════════════════════════════════════════════════════════════╗
║  ✅ NASA-LEVEL INTEGRATION COMPLETE                                  ║
╚══════════════════════════════════════════════════════════════════════╝

🚀 ГОТОВО К ИСПОЛЬЗОВАНИЮ:

1️⃣  Autonomous Service с NASA обучением:
   python3 autonomous_service.py --interval 600

2️⃣  Dashboard с NASA endpoints:
   python3 dashboard_server.py
   
3️⃣  Systemd Services:
   sudo ./install_nasa_services.sh

📚 NASA-Level Learning System полностью интегрирована!
        """
        )
        return 0
    elif success_rate >= 75:
        print(
            f"\n{YELLOW}⚠️  Большинство тестов прошло, но есть проблемы{RESET}"
        )
        return 1
    else:
        print(f"\n{RED}❌ КРИТИЧЕСКИЕ ОШИБКИ! Проверьте логи выше.{RESET}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
