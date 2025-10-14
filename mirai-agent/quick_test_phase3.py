#!/usr/bin/env python3
"""
🧪 Quick tests for Phase 3.1 and 3.2
"""

import json
import time

import requests

BASE_URL = "http://localhost:5000"


def test_1_health():
    """Test 1: Health endpoint"""
    print("\n" + "=" * 60)
    print("🧪 TEST 1: Health Endpoint")
    print("=" * 60)

    response = requests.get(f"{BASE_URL}/api/health", timeout=5)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert data["success"], "Health check failed"

    print("✅ Health check passed")
    print(f"   Status: {data['data']['status']}")
    print(f"   Grade: {data['data']['grade']}")
    print(f"   Success rate: {data['data']['metrics']['success_rate']}%")
    return True


def test_2_nasa_status():
    """Test 2: NASA Learning Status"""
    print("\n" + "=" * 60)
    print("🧪 TEST 2: NASA Learning Status")
    print("=" * 60)

    response = requests.get(f"{BASE_URL}/api/nasa/status", timeout=5)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()

    print("✅ NASA status retrieved")
    knowledge = data.get("data", {}).get("knowledge", {})
    metrics = data.get("data", {}).get("metrics", {})

    print(f"   Total learned: {knowledge.get('total_entries', 0)}")
    print(f"   Avg proficiency: {metrics.get('average_proficiency', 0)*100:.1f}%")
    print(f"   Success rate: {metrics.get('overall_success_rate', 0)*100:.1f}%")
    return True


def test_3_create_learning_task():
    """Test 3: Create Learning Task (Real-time API)"""
    print("\n" + "=" * 60)
    print("🧪 TEST 3: Create Learning Task")
    print("=" * 60)

    payload = {"technology": "requests", "depth": "basic", "priority": "high"}

    response = requests.post(f"{BASE_URL}/api/nasa/learn", json=payload, timeout=5)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert data["success"], "Task creation failed"

    task_id = data["task_id"]
    print(f"✅ Task created: {task_id}")
    print(f"   Technology: {payload['technology']}")
    print(f"   Depth: {payload['depth']}")
    print(f"   Priority: {payload['priority']}")

    return task_id


def test_4_get_task_status(task_id):
    """Test 4: Get Task Status"""
    print("\n" + "=" * 60)
    print("🧪 TEST 4: Get Task Status")
    print("=" * 60)

    response = requests.get(f"{BASE_URL}/api/nasa/learn/{task_id}", timeout=5)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert data["success"], "Get task failed"

    task = data["task"]
    print(f"✅ Task status retrieved")
    print(f"   Status: {task['status']}")
    print(f"   Progress: {task.get('progress', 0)}%")
    print(f"   Technology: {task['technology']}")

    return task


def test_5_list_all_tasks():
    """Test 5: List All Tasks"""
    print("\n" + "=" * 60)
    print("🧪 TEST 5: List All Tasks")
    print("=" * 60)

    response = requests.get(f"{BASE_URL}/api/nasa/tasks", timeout=5)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert data["success"], "List tasks failed"

    tasks = data["tasks"]
    print(f"✅ Tasks list retrieved")
    print(f"   Total tasks: {len(tasks)}")

    for task in tasks[:3]:  # Show first 3
        print(
            f"   • {task['technology']} - {task['status']} ({task.get('progress', 0)}%)"
        )

    return tasks


def test_6_web_ui():
    """Test 6: Web UI Dashboard"""
    print("\n" + "=" * 60)
    print("🧪 TEST 6: Web UI Dashboard")
    print("=" * 60)

    response = requests.get(f"{BASE_URL}/", timeout=5)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    html = response.text
    assert "NASA-Level Learning Dashboard" in html, "Dashboard title not found"
    assert "Chart.js" in html, "Chart.js not loaded"
    assert "dashboard.js" in html, "dashboard.js not loaded"

    print("✅ Web UI loaded successfully")
    print(f"   HTML size: {len(html)} bytes")
    print(f"   Contains Bootstrap: {'bootstrap' in html.lower()}")
    print(f"   Contains Charts: {'Chart.js' in html}")

    return True


def main():
    print("\n" + "=" * 70)
    print("🚀 PHASE 3 QUICK TEST SUITE")
    print("=" * 70)

    results = {}

    try:
        # Test 1: Health
        results["test_1"] = test_1_health()

        # Test 2: NASA Status
        results["test_2"] = test_2_nasa_status()

        # Test 3: Create Task
        task_id = test_3_create_learning_task()
        results["test_3"] = bool(task_id)

        # Wait a bit for task to start
        print("\n⏳ Waiting 3 seconds for task to process...")
        time.sleep(3)

        # Test 4: Get Task Status
        task = test_4_get_task_status(task_id)
        results["test_4"] = bool(task)

        # Test 5: List Tasks
        tasks = test_5_list_all_tasks()
        results["test_5"] = bool(tasks)

        # Test 6: Web UI
        results["test_6"] = test_6_web_ui()

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return 1

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for r in results.values() if r)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print("=" * 70)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("=" * 70)

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Phase 3.1 & 3.2 working perfectly!")
        print("\n📍 You can now open http://localhost:5000 in your browser")
        return 0
    else:
        print("\n⚠️ Some tests failed")
        return 1


if __name__ == "__main__":
    exit(main())
