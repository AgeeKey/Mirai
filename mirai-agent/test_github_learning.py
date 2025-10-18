#!/usr/bin/env python3
"""
🧪 Тест NASA Learning с GitHub Integration

Проверяет работу обновлённой системы обучения:
- Автоматический поиск репозиториев на GitHub
- Чтение README из топовых проектов
- Интеграция примеров в процесс обучения
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.autonomous_agent import AutonomousAgent
from core.nasa_level.orchestrator import NASALearningOrchestrator


def test_github_integration_learning():
    """Тест обучения с GitHub примерами"""

    print("=" * 80)
    print("🚀 TESTING: NASA Learning + GitHub Integration")
    print("=" * 80)

    # Создаём orchestrator (он сам создаст агента внутри)
    orchestrator = NASALearningOrchestrator()

    # Тестовая технология
    technology = "fastapi"

    print(f"\n📚 Learning technology: {technology}")
    print(f"   Expected: Search GitHub repos, read README, integrate examples\n")

    # Запускаем обучение
    result = orchestrator.learn_technology(technology=technology, depth="basic")

    print("\n" + "=" * 80)
    print("📊 RESULTS")
    print("=" * 80)

    print(f"\n✅ Success: {result.success}")
    print(f"📈 Proficiency: {result.proficiency:.2%}")
    print(f"⭐ Quality Grade: {result.quality_grade}")
    print(f"🧪 Tests: {result.tests_passed}/{result.tests_total} passed")
    print(f"⏱️  Time: {result.execution_time:.2f}s")

    if result.errors:
        print(f"\n❌ Errors:")
        for error in result.errors:
            print(f"   - {error}")

    if result.suggestions:
        print(f"\n💡 Suggestions:")
        for suggestion in result.suggestions:
            print(f"   - {suggestion}")

    # Проверяем GitHub integration
    print("\n" + "=" * 80)
    print("🔍 GITHUB INTEGRATION CHECK")
    print("=" * 80)

    research_artifact = None
    for artifact in result.artifacts:
        if artifact.phase.value == "research":
            research_artifact = artifact
            break

    if research_artifact:
        metadata = research_artifact.metadata
        print(f"\n📦 Research Artifact Metadata:")
        print(f"   - Content length: {metadata.get('length', 0)} chars")
        print(
            f"   - GitHub search attempted: {metadata.get('github_search_attempted', False)}"
        )
        print(f"   - Has GitHub examples: {metadata.get('has_github_examples', False)}")
        print(f"   - Quality score: {research_artifact.quality_score:.2f}")

        # Проверяем наличие GitHub данных в контенте
        content_lower = research_artifact.content.lower()
        has_github_mention = "github" in content_lower
        has_readme = "readme" in content_lower
        has_repository = "repository" in content_lower or "repo" in content_lower

        print(f"\n📝 Content Analysis:")
        print(f"   - Mentions GitHub: {has_github_mention}")
        print(f"   - Mentions README: {has_readme}")
        print(f"   - Mentions repositories: {has_repository}")

        if metadata.get("has_github_examples", False):
            print(f"\n✨ SUCCESS: GitHub integration is working!")
            print(f"   Research phase included real-world examples from GitHub")
        else:
            print(f"\n⚠️  WARNING: GitHub integration may not be working")
            print(f"   No GitHub examples found in research phase")
    else:
        print("\n❌ ERROR: No research artifact found")

    # Итоговая оценка
    print("\n" + "=" * 80)
    print("🎯 FINAL ASSESSMENT")
    print("=" * 80)

    success_criteria = [
        ("Learning completed successfully", result.success),
        ("Proficiency >= 50%", result.proficiency >= 0.5),
        ("Quality grade >= D", result.quality_grade in ["A+", "A", "B", "C", "D"]),
        (
            "GitHub search attempted",
            research_artifact
            and research_artifact.metadata.get("github_search_attempted", False),
        ),
        ("At least 1 test passed", result.tests_passed > 0),
    ]

    passed = 0
    total = len(success_criteria)

    for criterion, status in success_criteria:
        symbol = "✅" if status else "❌"
        print(f"{symbol} {criterion}")
        if status:
            passed += 1

    print(f"\n🏆 Score: {passed}/{total} criteria met ({passed/total*100:.0f}%)")

    if passed == total:
        print("\n🎉 PERFECT! All criteria passed!")
        print("   NASA Learning + GitHub Integration is working correctly!")
    elif passed >= total * 0.8:
        print("\n👍 GOOD! Most criteria passed!")
        print("   Minor issues may need attention")
    elif passed >= total * 0.6:
        print("\n⚠️  WARNING! Some criteria failed")
        print("   Review the errors above")
    else:
        print("\n❌ FAILURE! Integration not working properly")
        print("   Check GitHub authentication and code changes")

    return result


if __name__ == "__main__":
    print("\n🤖 MIRAI NASA Learning + GitHub Integration Test")
    print("   Testing enhanced learning with real-world code examples\n")

    try:
        result = test_github_integration_learning()

        print("\n" + "=" * 80)
        print("✅ Test completed!")
        print("=" * 80)

        # Возвращаем код выхода на основе результата
        if result.success and result.proficiency >= 0.5:
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
