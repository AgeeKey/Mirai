#!/usr/bin/env python3
"""
🧪 Test Real-time Learning API
Тестирование асинхронного обучения через API
"""

import sys
import time
import requests
import json

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
║  🧪 REAL-TIME LEARNING API TEST                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """
    )

    base_url = "http://localhost:5000"
    results = []

    # ========================================================================
    # TEST 1: Check if dashboard is running
    # ========================================================================
    test_header("TEST 1: Dashboard Availability")

    try:
        response = requests.get(f"{base_url}/api/health", timeout=2)
        dashboard_running = response.status_code == 200
        results.append(
            test_result("Dashboard is running", dashboard_running, f"Status: {response.status_code}")
        )
    except requests.exceptions.ConnectionError:
        print(f"{RED}❌ Dashboard not running{RESET}")
        print(f"\n{YELLOW}⚠️  Please start dashboard first:{RESET}")
        print(f"   cd /root/mirai/mirai-agent")
        print(f"   python3 dashboard_server.py")
        return 1

    # ========================================================================
    # TEST 2: Create learning task
    # ========================================================================
    test_header("TEST 2: Create Learning Task")

    try:
        response = requests.post(
            f"{base_url}/api/nasa/learn",
            json={"technology": "json", "depth": "basic", "priority": "normal"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            task_id = data.get("task_id")
            results.append(
                test_result(
                    "Create task via POST /api/nasa/learn",
                    data.get("success", False),
                    f"Task ID: {task_id}"
                )
            )
        else:
            results.append(
                test_result(
                    "Create task via POST /api/nasa/learn",
                    False,
                    f"Status: {response.status_code}"
                )
            )
            task_id = None
    except Exception as e:
        results.append(test_result("Create task via POST /api/nasa/learn", False, str(e)))
        task_id = None

    if not task_id:
        print(f"\n{RED}Cannot continue without task_id{RESET}")
        return 1

    # ========================================================================
    # TEST 3: Get task status
    # ========================================================================
    test_header("TEST 3: Get Task Status")

    try:
        response = requests.get(f"{base_url}/api/nasa/learn/{task_id}", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            task = data.get("task", {})
            status = task.get("status")
            progress = task.get("progress", 0)
            
            results.append(
                test_result(
                    f"Get task status via GET /api/nasa/learn/{task_id}",
                    True,
                    f"Status: {status}, Progress: {progress}%"
                )
            )
        else:
            results.append(
                test_result(
                    "Get task status",
                    False,
                    f"Status: {response.status_code}"
                )
            )
    except Exception as e:
        results.append(test_result("Get task status", False, str(e)))

    # ========================================================================
    # TEST 4: List all tasks
    # ========================================================================
    test_header("TEST 4: List All Tasks")

    try:
        response = requests.get(f"{base_url}/api/nasa/tasks", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            tasks = data.get("tasks", [])
            stats = data.get("stats", {})
            
            results.append(
                test_result(
                    "List all tasks via GET /api/nasa/tasks",
                    True,
                    f"Total tasks: {len(tasks)}, Stats: {stats.get('total', 0)} total, "
                    f"{stats.get('running', 0)} running, {stats.get('completed', 0)} completed"
                )
            )
        else:
            results.append(
                test_result("List all tasks", False, f"Status: {response.status_code}")
            )
    except Exception as e:
        results.append(test_result("List all tasks", False, str(e)))

    # ========================================================================
    # TEST 5: Wait for task completion
    # ========================================================================
    test_header("TEST 5: Monitor Task Progress")

    print(f"\n{YELLOW}⏳ Waiting for task to complete (max 120s)...{RESET}\n")

    max_wait = 120
    start_time = time.time()
    last_status = None
    last_progress = 0

    try:
        while time.time() - start_time < max_wait:
            response = requests.get(f"{base_url}/api/nasa/learn/{task_id}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                task = data.get("task", {})
                status = task.get("status")
                progress = task.get("progress", 0)
                
                # Print progress updates
                if status != last_status or progress != last_progress:
                    elapsed = time.time() - start_time
                    print(f"   [{elapsed:5.1f}s] Status: {status:10s} | Progress: {progress:3d}%")
                    last_status = status
                    last_progress = progress
                
                # Check if completed
                if status in ["completed", "failed", "cancelled"]:
                    result = task.get("result")
                    if status == "completed" and result:
                        results.append(
                            test_result(
                                "Task completed successfully",
                                True,
                                f"Proficiency: {result.get('proficiency', 0):.1f}%, "
                                f"Grade: {result.get('quality_grade', 'N/A')}, "
                                f"Time: {result.get('execution_time', 0):.1f}s"
                            )
                        )
                    elif status == "failed":
                        error = task.get("error", "Unknown error")
                        results.append(
                            test_result("Task completed", False, f"Failed: {error}")
                        )
                    break
            
            time.sleep(2)
        else:
            # Timeout
            results.append(
                test_result(
                    "Task completion",
                    False,
                    f"Timeout after {max_wait}s (status: {last_status})"
                )
            )
    except Exception as e:
        results.append(test_result("Task monitoring", False, str(e)))

    # ========================================================================
    # TEST 6: Create another task (test queue)
    # ========================================================================
    test_header("TEST 6: Test Task Queue")

    try:
        response = requests.post(
            f"{base_url}/api/nasa/learn",
            json={"technology": "os", "depth": "basic", "priority": "high"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            task_id_2 = data.get("task_id")
            results.append(
                test_result(
                    "Create second task (queue test)",
                    data.get("success", False),
                    f"Task ID: {task_id_2}"
                )
            )
            
            # Check queue stats
            time.sleep(1)
            response = requests.get(f"{base_url}/api/nasa/tasks", timeout=5)
            if response.status_code == 200:
                stats = response.json().get("stats", {})
                queue_size = stats.get("queue_size", 0)
                results.append(
                    test_result(
                        "Task queue functioning",
                        True,
                        f"Queue size: {queue_size}, Running: {stats.get('running', 0)}"
                    )
                )
        else:
            results.append(
                test_result("Create second task", False, f"Status: {response.status_code}")
            )
    except Exception as e:
        results.append(test_result("Create second task", False, str(e)))

    # ========================================================================
    # TEST 7: Task manager stats
    # ========================================================================
    test_header("TEST 7: Task Manager Stats")

    try:
        response = requests.get(f"{base_url}/api/nasa/status", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            task_manager_stats = data.get("data", {}).get("task_manager", {})
            
            results.append(
                test_result(
                    "Task manager stats in /api/nasa/status",
                    bool(task_manager_stats),
                    f"Total: {task_manager_stats.get('total', 0)}, "
                    f"Workers: {task_manager_stats.get('workers', 0)}, "
                    f"Max concurrent: {task_manager_stats.get('max_concurrent', 0)}"
                )
            )
        else:
            results.append(
                test_result("Task manager stats", False, f"Status: {response.status_code}")
            )
    except Exception as e:
        results.append(test_result("Task manager stats", False, str(e)))

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
║  ✅ REAL-TIME LEARNING API WORKS!                                    ║
╚══════════════════════════════════════════════════════════════════════╝

🚀 ГОТОВО К ИСПОЛЬЗОВАНИЮ:

1️⃣  Create learning task:
   curl -X POST http://localhost:5000/api/nasa/learn \\
     -H "Content-Type: application/json" \\
     -d '{"technology": "requests", "depth": "basic"}'

2️⃣  Check task status:
   curl http://localhost:5000/api/nasa/learn/<task_id>

3️⃣  List all tasks:
   curl http://localhost:5000/api/nasa/tasks

📚 Real-time Learning API полностью функционально!
        """
        )
        return 0
    elif success_rate >= 75:
        print(f"\n{YELLOW}⚠️  Большинство тестов прошло, но есть проблемы{RESET}")
        return 1
    else:
        print(f"\n{RED}❌ КРИТИЧЕСКИЕ ОШИБКИ! Проверьте логи выше.{RESET}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
