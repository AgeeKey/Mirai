#!/usr/bin/env python3
"""
🧠 Reasoning Engine - Example Usage

Demonstrates the complete reasoning engine workflow.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.reasoning_engine import (
    DecisionMaker,
    ContextProcessor,
    IntelligentPlanner,
    RiskAssessor,
    PreferenceManager,
    MemoryContextIntegration,
    TaskStatus,
    ApplicationStatus,
)


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def example_decision_making():
    """Example: Decision Making"""
    print_section("🧠 DECISION MAKING")
    
    dm = DecisionMaker()
    
    # Make a decision
    task = "Open Chrome and search for Python documentation"
    print(f"\n📝 Task: {task}")
    
    decision = dm.make_decision(task)
    
    if decision['selected_action']:
        action = decision['selected_action']
        print(f"\n✅ Decision made:")
        print(f"   Action: {action.name}")
        print(f"   Type: {action.action_type}")
        print(f"   Confidence: {action.confidence:.2%}")
        print(f"   Rank: {action.rank:.3f}")
        print(f"   Safety score: {action.safety_score:.2%}")
        print(f"   Time estimate: {action.time_complexity:.1f}s")
        
        if decision['alternative_actions']:
            print(f"\n📋 Alternatives:")
            for alt in decision['alternative_actions'][:2]:
                print(f"   - {alt.name} (confidence: {alt.confidence:.2%})")
    else:
        print("❌ No action available")


def example_memory_system():
    """Example: Memory System"""
    print_section("💾 MEMORY SYSTEM")
    
    memory = MemoryContextIntegration(user_id="demo_user")
    
    # Record some events
    print("\n📝 Recording events...")
    
    events = [
        {
            "event": {"task": "search web", "query": "Python tutorials"},
            "action": {"type": "type", "target": "search_box"},
            "result": {"success": True, "results_found": 15},
            "success": True,
            "confidence": 0.9
        },
        {
            "event": {"task": "open browser"},
            "action": {"type": "click", "target": "chrome_icon"},
            "result": {"success": True, "startup_time": 3.2},
            "success": True,
            "confidence": 0.95
        },
        {
            "event": {"task": "type code"},
            "action": {"type": "type", "target": "editor"},
            "result": {"success": False, "error": "editor not focused"},
            "success": False,
            "confidence": 0.7
        }
    ]
    
    for event_data in events:
        memory.record_event_action_result(**event_data)
        print(f"   ✅ Recorded: {event_data['event']['task']}")
    
    # Get context
    print("\n📊 Current context:")
    context = memory.get_context("search tutorials")
    print(f"   Recent actions: {len(context['recent_actions'])}")
    print(f"   Recent observations: {len(context['recent_observations'])}")
    print(f"   Session events: {context['session_events']}")
    
    # Get metrics
    print("\n📈 Memory metrics:")
    metrics = memory.get_metrics()
    print(f"   Short-term actions: {metrics['short_term']['actions']}")
    print(f"   Session events: {metrics['session']['events']}")
    print(f"   Success rate: {metrics['session']['success_rate']:.1%}")


def example_risk_assessment():
    """Example: Risk Assessment"""
    print_section("⚠️ RISK ASSESSMENT")
    
    ra = RiskAssessor()
    
    # Assess different types of actions
    test_actions = [
        {"type": "click", "id": "click_1", "target": "button"},
        {"type": "delete", "id": "delete_1", "target": "important_file.txt"},
        {"type": "execute_code", "id": "exec_1", "code": "import os"},
    ]
    
    for action in test_actions:
        print(f"\n🔍 Assessing: {action['type']} on {action.get('target', action.get('code', 'unknown'))}")
        
        assessment = ra.assess_action(action, {})
        
        print(f"   Total risks: {assessment['total_risks']}")
        print(f"   Critical: {assessment['critical_risks']}, High: {assessment['high_risks']}")
        print(f"   Accepted: {'✅ Yes' if assessment['accepted'] else '❌ No'}")
        print(f"   Pre-checks passed: {'✅' if assessment['pre_checks']['all_passed'] else '❌'}")
        
        if assessment['risks']:
            print(f"   Top risk: {assessment['risks'][0].description}")


def example_preferences():
    """Example: Preference Management"""
    print_section("👤 USER PREFERENCES")
    
    pm = PreferenceManager(user_id="demo_user")
    
    # Learn some preferences
    print("\n📚 Learning preferences...")
    
    pm.learn_browser_preference("chrome", "Work Profile")
    print("   ✅ Browser: Chrome (Work Profile)")
    
    pm.learn_decision_preference("medium", "balanced")
    print("   ✅ Decision style: Medium risk, Balanced speed")
    
    pm.learn_time_preference(60, "patient")
    print("   ✅ Time preference: 60s deadline, Patient")
    
    # Simulate some interactions
    print("\n💻 Recording interactions...")
    for i in range(5):
        pm.record_interaction({"type": "click", "target": f"button_{i}"})
    pm.record_app_usage("chrome", "open")
    pm.record_app_usage("vscode", "open")
    pm.track_search_patterns("python tutorial", "programming")
    
    print(f"   Total interactions: {pm.profile.total_interactions}")
    
    # Show profile
    print("\n📋 User Profile:")
    print(f"   Browser: {pm.profile.preferred_browser} ({pm.profile.preferred_profile})")
    print(f"   Risk tolerance: {pm.profile.risk_tolerance}")
    print(f"   Click speed: {pm.profile.click_speed}")
    print(f"   Frequently used apps: {list(pm.profile.frequently_used_apps.keys())}")


def example_context_processing():
    """Example: Context Processing"""
    print_section("🖥️ CONTEXT PROCESSING")
    
    cp = ContextProcessor()
    
    # Update application states
    print("\n📱 Tracking applications...")
    
    cp.update_application_state("chrome", status=ApplicationStatus.READY, pid=1234)
    print("   ✅ Chrome: READY")
    
    cp.transition_app_state("vscode", ApplicationStatus.STARTING)
    print("   ⏳ VSCode: STARTING")
    
    cp.track_chrome_profile("Work Profile")
    print("   📊 Chrome profile: Work Profile")
    
    # Monitor resources
    print("\n💻 System resources:")
    resources = cp.monitor_system_resources()
    print(f"   CPU: {resources['cpu_percent']:.1f}%")
    print(f"   Memory: {resources['memory_percent']:.1f}%")
    print(f"   Available: {resources['memory_available_mb']:.0f} MB")
    
    # Get full context
    print("\n🌍 Full context:")
    context = cp.get_full_context()
    print(f"   Applications tracked: {len(context['applications'])}")
    print(f"   Running apps: {context['running_apps']}")
    print(f"   Network connected: {context['network_connected']}")


def example_intelligent_planning():
    """Example: Intelligent Planning"""
    print_section("📋 INTELLIGENT PLANNING")
    
    ip = IntelligentPlanner()
    
    # Create execution plan
    goal = "Search for Python AI tutorials and save top 3 results"
    print(f"\n🎯 Goal: {goal}")
    
    plan = ip.create_execution_plan(goal)
    
    print(f"\n📊 Execution Plan:")
    print(f"   Total tasks: {len(plan.tasks)}")
    print(f"   Estimated time: {plan.estimated_total_time:.1f}s")
    print(f"   Critical path: {len(plan.critical_path)} tasks")
    print(f"   Parallel groups: {len(plan.parallel_groups)}")
    
    print(f"\n📝 Task breakdown:")
    for i, task in enumerate(plan.tasks, 1):
        deps = f" (depends on: {', '.join(task.depends_on)})" if task.depends_on else ""
        print(f"   {i}. {task.name} - {task.estimated_time:.1f}s{deps}")
    
    # Simulate execution
    print(f"\n⚡ Simulating execution...")
    completed = set()
    
    for task in plan.tasks[:3]:  # Execute first 3 tasks
        ip.update_task_status(task.id, TaskStatus.IN_PROGRESS)
        print(f"   ▶️ Started: {task.name}")
        
        # Simulate completion
        ip.update_task_status(task.id, TaskStatus.COMPLETED, {"success": True})
        completed.add(task.id)
        print(f"   ✅ Completed: {task.name}")
    
    # Show progress
    progress = ip.get_plan_progress()
    print(f"\n📈 Progress:")
    print(f"   {progress['progress_percent']:.1f}% complete")
    print(f"   {progress['completed']}/{progress['total_tasks']} tasks done")


def example_full_workflow():
    """Example: Complete Workflow"""
    print_section("🔄 COMPLETE WORKFLOW")
    
    # Initialize all components
    print("\n🚀 Initializing reasoning engine...")
    dm = DecisionMaker()
    cp = ContextProcessor()
    ip = IntelligentPlanner()
    ra = RiskAssessor()
    pm = PreferenceManager(user_id="demo_user")
    memory = MemoryContextIntegration(user_id="demo_user")
    print("   ✅ All components initialized")
    
    # Define goal
    goal = "Open browser and search for AI news"
    print(f"\n🎯 Goal: {goal}")
    
    # Step 1: Create plan
    print("\n1️⃣ Creating execution plan...")
    plan = ip.create_execution_plan(goal)
    print(f"   📋 {len(plan.tasks)} tasks planned")
    
    # Step 2: Get context
    print("\n2️⃣ Gathering context...")
    context = cp.get_full_context()
    print(f"   🌍 Context retrieved")
    
    # Step 3: Execute with decision making
    print("\n3️⃣ Executing tasks...")
    
    for i, task in enumerate(plan.tasks[:2], 1):  # Execute first 2 tasks
        print(f"\n   Task {i}: {task.name}")
        
        # Make decision
        decision = dm.make_decision(task.description, context)
        print(f"      🧠 Decision: {decision['confidence']:.1%} confident")
        
        # Assess risks
        assessment = ra.assess_action(
            {"type": task.task_type, "id": task.id},
            context
        )
        print(f"      ⚠️ Risks: {assessment['total_risks']} identified, accepted: {assessment['accepted']}")
        
        if assessment['accepted']:
            # Execute (simulated)
            result = {"success": True}
            
            # Record
            memory.record_event_action_result(
                event={"task": task.name},
                action={"type": task.task_type},
                result=result,
                success=True,
                confidence=decision['confidence']
            )
            
            ip.update_task_status(task.id, TaskStatus.COMPLETED, result)
            print(f"      ✅ Completed and recorded")
        else:
            ip.update_task_status(task.id, TaskStatus.SKIPPED)
            print(f"      ⏭️ Skipped due to high risk")
    
    # Step 4: Review results
    print("\n4️⃣ Results:")
    progress = ip.get_plan_progress()
    metrics = memory.get_metrics()
    
    print(f"   Progress: {progress['progress_percent']:.1f}%")
    print(f"   Events recorded: {metrics['session']['events']}")
    print(f"   Success rate: {metrics['session']['success_rate']:.1%}")


def main():
    """Run all examples"""
    print("🧠 MIRAI REASONING ENGINE - EXAMPLES")
    print("Phase 2 Implementation Demonstration")
    
    examples = [
        ("Decision Making", example_decision_making),
        ("Memory System", example_memory_system),
        ("Risk Assessment", example_risk_assessment),
        ("User Preferences", example_preferences),
        ("Context Processing", example_context_processing),
        ("Intelligent Planning", example_intelligent_planning),
        ("Complete Workflow", example_full_workflow),
    ]
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            import traceback
            traceback.print_exc()
    
    print_section("✅ EXAMPLES COMPLETE")
    print("\nAll reasoning engine components demonstrated successfully!")
    print("For more details, see: core/reasoning_engine/README.md")


if __name__ == "__main__":
    main()
