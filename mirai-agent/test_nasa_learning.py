#!/usr/bin/env python3
"""
NASA-Level Learning System - Integration Test
Тестирование полного цикла обучения
"""

import os
import sys

# Add to path
sys.path.insert(0, "/root/mirai/mirai-agent")

from core.autonomous_agent import AutonomousAgent
from core.nasa_level.advanced_learning import AdvancedLearningEngine
from core.nasa_level.quality_analyzer import CodeQualityAnalyzer
from core.nasa_level.sandbox_executor import SandboxExecutor


def main():
    print("\n" + "=" * 80)
    print("🚀 NASA-LEVEL LEARNING SYSTEM - INTEGRATION TEST")
    print("=" * 80)

    print("\n📦 Initializing components...")

    # Initialize components
    try:
        print("  ✅ Creating AI Agent...")
        ai_agent = AutonomousAgent()

        print("  ✅ Creating Sandbox Executor...")
        sandbox = SandboxExecutor()

        print("  ✅ Creating Quality Analyzer...")
        quality_analyzer = CodeQualityAnalyzer()

        print("  ✅ Creating Learning Engine...")
        learning_engine = AdvancedLearningEngine(ai_agent, sandbox, quality_analyzer)

        print("\n✨ All components initialized successfully!")

    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        return 1

    # Test learning
    print("\n" + "=" * 80)
    print("🧪 TEST: Learning a simple technology")
    print("=" * 80)

    technology = "JSON"

    try:
        result = learning_engine.learn_technology(technology, depth="basic")

        print("\n" + "=" * 80)
        print("📊 LEARNING RESULTS")
        print("=" * 80)
        print(f"Technology: {result.technology}")
        print(f"Success: {'✅' if result.success else '❌'}")
        print(f"Proficiency: {result.proficiency:.1%}")
        print(f"Quality Grade: {result.quality_grade}")
        print(f"Tests: {result.tests_passed}/{result.tests_total}")
        print(f"Execution Time: {result.execution_time:.2f}s")

        if result.errors:
            print(f"\nErrors:")
            for error in result.errors:
                print(f"  ❌ {error}")

        if result.suggestions:
            print(f"\nSuggestions:")
            for suggestion in result.suggestions:
                print(f"  💡 {suggestion}")

        print("\n" + "=" * 80)
        print("📝 LEARNING ARTIFACTS")
        print("=" * 80)
        for i, artifact in enumerate(result.artifacts, 1):
            print(f"\n{i}. {artifact.phase.value.upper()}")
            print(f"   Quality Score: {artifact.quality_score:.2f}")
            print(f"   Content length: {len(artifact.content)} chars")

        if result.success:
            print("\n🎉 SUCCESS! NASA-Level Learning System is operational!")
            return 0
        else:
            print("\n⚠️  Learning completed with issues. Review errors above.")
            return 1

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
