#!/usr/bin/env python3
"""
🧪 Tests for Reasoning Engine - Phase 2

Tests for all components:
- Decision Maker
- Memory System
- Risk Assessor
- Preference Manager
- Context Processor
- Intelligent Planner
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.reasoning_engine import (
    DecisionMaker,
    ContextProcessor,
    IntelligentPlanner,
    ShortTermMemory,
    LongTermMemory,
    MemoryContextIntegration,
    RiskAssessor,
    PreferenceManager,
    Action,
    Task,
    TaskStatus,
    RiskCategory,
    ApplicationStatus,
)


def test_decision_maker():
    """Test Decision Maker component"""
    print("\n🧪 Testing Decision Maker...")
    
    dm = DecisionMaker()
    
    # Test situation analysis
    visual_context = dm.get_visual_context()
    assert isinstance(visual_context, dict)
    print("✅ Visual context capture works")
    
    # Test decision parameters preparation
    params = dm.prepare_decision_parameters("Open Chrome browser")
    assert params.user_intent == "Open Chrome browser"
    print("✅ Decision parameters preparation works")
    
    # Test constraint checking
    constraints = dm.check_constraints()
    assert "cpu_percent" in constraints
    assert "memory_percent" in constraints
    print("✅ Constraint checking works")
    
    # Test action evaluation
    test_action = Action(
        id="test_1",
        name="Test action",
        description="Test",
        action_type="click"
    )
    
    effectiveness = dm.score_effectiveness(test_action, {})
    assert 0.0 <= effectiveness <= 1.0
    print("✅ Action effectiveness scoring works")
    
    safety = dm.assess_safety(test_action)
    assert 0.0 <= safety <= 1.0
    print("✅ Safety assessment works")
    
    print("✅ Decision Maker tests passed!")
    return True


def test_memory_system():
    """Test Memory System components"""
    print("\n🧪 Testing Memory System...")
    
    # Test Short-Term Memory
    stm = ShortTermMemory()
    stm.add_action({"type": "click", "target": "button"})
    stm.add_observation({"screen": "chrome", "status": "ready"})
    
    recent = stm.get_recent_actions(1)
    assert len(recent) == 1
    print("✅ Short-term memory works")
    
    # Test Long-Term Memory
    ltm = LongTermMemory()
    from core.reasoning_engine.memory_system import EventActionResult
    from datetime import datetime
    
    ear = EventActionResult(
        event={"type": "user_request", "task": "search"},
        action={"type": "click", "target": "search_box"},
        result={"success": True},
        success=True,
        confidence=0.9
    )
    
    event_id = ltm.store_event_action_result(ear)
    assert event_id > 0
    print("✅ Long-term memory storage works")
    
    # Test Memory Integration
    mci = MemoryContextIntegration(user_id="test_user")
    mci.record_event_action_result(
        event={"task": "test"},
        action={"type": "click"},
        result={"success": True},
        success=True,
        confidence=0.8
    )
    
    context = mci.get_context("test task")
    assert "task" in context
    print("✅ Memory-Context integration works")
    
    metrics = mci.get_metrics()
    assert "short_term" in metrics
    print("✅ Memory metrics work")
    
    print("✅ Memory System tests passed!")
    return True


def test_risk_assessor():
    """Test Risk Assessor component"""
    print("\n🧪 Testing Risk Assessor...")
    
    ra = RiskAssessor()
    
    # Test risk categorization
    test_action = {"type": "delete", "target": "file.txt"}
    risks = ra.categorize_risks(test_action)
    assert len(risks) > 0
    assert any(r.category == RiskCategory.DATA for r in risks)
    print("✅ Risk categorization works")
    
    # Test mitigation strategies
    risks_with_mitigation = ra.develop_mitigation_strategies(risks)
    assert all(r.mitigation for r in risks_with_mitigation)
    print("✅ Mitigation strategy development works")
    
    # Test safety constraints
    constraints = ra.define_safety_constraints(test_action)
    assert constraints.require_confirmation == True
    print("✅ Safety constraints definition works")
    
    # Test pre-action checks
    pre_checks = ra.perform_pre_action_checks(test_action, {"completed_actions": []})
    assert "system_stable" in pre_checks
    print("✅ Pre-action checks work")
    
    # Test rollback planning
    rollback = ra.plan_rollback(test_action)
    assert rollback.action_id == test_action.get("id", "unknown")
    print("✅ Rollback planning works")
    
    # Test complete assessment
    assessment = ra.assess_action({"type": "click", "id": "test_click"}, {})
    assert "risks" in assessment
    assert "constraints" in assessment
    print("✅ Complete risk assessment works")
    
    print("✅ Risk Assessor tests passed!")
    return True


def test_preference_manager():
    """Test Preference Manager component"""
    print("\n🧪 Testing Preference Manager...")
    
    import time
    pm = PreferenceManager(user_id=f"test_user_{int(time.time())}")
    
    # Test browser preference learning
    pm.learn_browser_preference("chrome", "Profile 1")
    assert pm.profile.preferred_browser == "chrome"
    assert pm.profile.preferred_profile == "Profile 1"
    print("✅ Browser preference learning works")
    
    # Test interaction recording
    initial_count = pm.profile.total_interactions
    pm.record_interaction({"type": "click", "target": "button"})
    assert pm.profile.total_interactions == initial_count + 1
    print("✅ Interaction recording works")
    
    # Test app usage tracking
    pm.record_app_usage("chrome", "open")
    assert "chrome" in pm.profile.frequently_used_apps
    print("✅ App usage tracking works")
    
    # Test search pattern tracking
    pm.track_search_patterns("python tutorial", "programming")
    assert "programming" in pm.profile.search_categories
    print("✅ Search pattern tracking works")
    
    # Test decision preference learning
    pm.learn_decision_preference("medium", "balanced")
    assert pm.profile.risk_tolerance == "medium"
    print("✅ Decision preference learning works")
    
    # Test profile export/import
    profile_data = pm.export_profile()
    assert "user_id" in profile_data
    print("✅ Profile export works")
    
    print("✅ Preference Manager tests passed!")
    return True


def test_context_processor():
    """Test Context Processor component"""
    print("\n🧪 Testing Context Processor...")
    
    cp = ContextProcessor()
    
    # Test application state management
    cp.update_application_state("chrome", status=ApplicationStatus.READY, pid=1234)
    state = cp.get_application_state("chrome")
    assert state.status == ApplicationStatus.READY
    print("✅ Application state management works")
    
    # Test state transitions
    cp.transition_app_state("chrome", ApplicationStatus.LOADING)
    state = cp.get_application_state("chrome")
    assert state.status == ApplicationStatus.LOADING
    print("✅ State transitions work")
    
    # Test Chrome profile tracking
    cp.track_chrome_profile("Work Profile")
    assert cp.current_chrome_profile == "Work Profile"
    print("✅ Chrome profile tracking works")
    
    # Test resource monitoring
    resources = cp.monitor_system_resources()
    assert "cpu_percent" in resources
    assert "memory_percent" in resources
    print("✅ Resource monitoring works")
    
    # Test network state checking
    network = cp.check_network_state()
    assert "connected" in network
    print("✅ Network state checking works")
    
    # Test state snapshot
    snapshot = cp.create_state_snapshot()
    assert "applications" in snapshot
    assert "timestamp" in snapshot
    print("✅ State snapshot creation works")
    
    # Test full context
    context = cp.get_full_context()
    assert "applications" in context
    assert "resources" in context
    print("✅ Full context retrieval works")
    
    print("✅ Context Processor tests passed!")
    return True


def test_intelligent_planner():
    """Test Intelligent Planner component"""
    print("\n🧪 Testing Intelligent Planner...")
    
    ip = IntelligentPlanner()
    
    # Test task decomposition
    tasks = ip.hierarchical_task_breakdown("Search for Python tutorials")
    assert len(tasks) > 0
    print(f"✅ Task decomposition works ({len(tasks)} tasks created)")
    
    # Test dependency mapping
    dependencies = ip.map_dependencies(tasks)
    assert isinstance(dependencies, dict)
    print("✅ Dependency mapping works")
    
    # Test topological sort
    sorted_tasks = ip.topological_sort(tasks)
    assert len(sorted_tasks) == len(tasks)
    print("✅ Topological sort works")
    
    # Test critical path finding
    critical_path = ip.find_critical_path(tasks)
    assert len(critical_path) > 0
    print(f"✅ Critical path analysis works ({len(critical_path)} tasks on path)")
    
    # Test parallelization identification
    parallel_groups = ip.identify_parallelization(tasks)
    assert len(parallel_groups) > 0
    print(f"✅ Parallelization identification works ({len(parallel_groups)} groups)")
    
    # Test complete plan creation
    plan = ip.create_execution_plan("Open Chrome and search for AI news")
    assert plan.goal == "Open Chrome and search for AI news"
    assert len(plan.tasks) > 0
    assert plan.estimated_total_time > 0
    print(f"✅ Execution plan creation works ({len(plan.tasks)} tasks, {plan.estimated_total_time:.1f}s)")
    
    # Test task status updates
    if plan.tasks:
        first_task = plan.tasks[0]
        ip.update_task_status(first_task.id, TaskStatus.COMPLETED)
        assert first_task.status == TaskStatus.COMPLETED
        print("✅ Task status updates work")
    
    # Test progress tracking
    progress = ip.get_plan_progress()
    assert "total_tasks" in progress
    assert "completed" in progress
    print(f"✅ Progress tracking works ({progress['progress_percent']:.1f}% complete)")
    
    # Test plan export
    plan_dict = ip.export_plan()
    assert "goal" in plan_dict
    assert "tasks" in plan_dict
    print("✅ Plan export works")
    
    print("✅ Intelligent Planner tests passed!")
    return True


def test_integration():
    """Test integration between components"""
    print("\n🧪 Testing Integration...")
    
    # Create all components
    dm = DecisionMaker()
    cp = ContextProcessor()
    ip = IntelligentPlanner()
    ra = RiskAssessor()
    pm = PreferenceManager(user_id="test_integration")
    mci = MemoryContextIntegration(user_id="test_integration")
    
    # Simulate a complete workflow
    goal = "Search for Python documentation"
    
    # 1. Create execution plan
    plan = ip.create_execution_plan(goal)
    print(f"✅ Created plan with {len(plan.tasks)} tasks")
    
    # 2. Get application context
    context = cp.get_full_context()
    print(f"✅ Retrieved context with {len(context.get('applications', {}))} apps")
    
    # 3. Assess risks for first task
    if plan.tasks:
        first_task = plan.tasks[0]
        assessment = ra.assess_action(
            {"type": first_task.task_type, "id": first_task.id},
            context
        )
        print(f"✅ Risk assessment: {assessment['total_risks']} risks identified")
        
        # 4. Record in memory
        mci.record_event_action_result(
            event={"goal": goal, "task": first_task.name},
            action={"type": first_task.task_type},
            result={"success": True},
            success=True,
            confidence=0.85
        )
        print("✅ Recorded in memory")
        
        # 5. Update preferences
        pm.record_interaction({"type": "task_execution", "task": first_task.name})
        print("✅ Updated preferences")
    
    print("✅ Integration tests passed!")
    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 REASONING ENGINE TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Decision Maker", test_decision_maker),
        ("Memory System", test_memory_system),
        ("Risk Assessor", test_risk_assessor),
        ("Preference Manager", test_preference_manager),
        ("Context Processor", test_context_processor),
        ("Intelligent Planner", test_intelligent_planner),
        ("Integration", test_integration),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"❌ {name} test failed")
        except Exception as e:
            failed += 1
            print(f"❌ {name} test failed with exception: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
        return True
    else:
        print("⚠️ SOME TESTS FAILED")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
