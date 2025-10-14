#!/usr/bin/env python3
"""
🧪 Phase 3.3 Analytics Engine Tests
"""

import json

import requests

BASE_URL = "http://localhost:5000"


def test_analytics_trends():
    """Test learning trends endpoint"""
    print("\n" + "=" * 60)
    print("🧪 TEST: Analytics Trends")
    print("=" * 60)

    # Test week trends
    response = requests.get(
        f"{BASE_URL}/api/nasa/analytics/trends?period=week", timeout=5
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"]

    print(f"✅ Trends retrieved")
    print(f"   Trends count: {len(data.get('trends', []))}")

    if data.get("trends"):
        for trend in data["trends"][:2]:
            print(
                f"   • {trend['metric']}: {trend['trend_direction']} (confidence: {trend['confidence']:.2f})"
            )

    return True


def test_analytics_recommendations():
    """Test technology recommendations"""
    print("\n" + "=" * 60)
    print("🧪 TEST: Technology Recommendations")
    print("=" * 60)

    response = requests.get(
        f"{BASE_URL}/api/nasa/analytics/recommendations?limit=5&level=intermediate",
        timeout=5,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"]

    recommendations = data.get("recommendations", [])
    print(f"✅ Recommendations retrieved")
    print(f"   Total: {len(recommendations)}")

    for i, rec in enumerate(recommendations[:3], 1):
        print(f"   {i}. {rec['technology']} (score: {rec['score']:.2f})")
        print(f"      {rec['reason']}")
        print(
            f"      Difficulty: {rec['estimated_difficulty']}, Est. time: {rec['estimated_time_hours']}h"
        )

    return recommendations


def test_analytics_predictions():
    """Test proficiency predictions"""
    print("\n" + "=" * 60)
    print("🧪 TEST: Proficiency Predictions")
    print("=" * 60)

    technology = "typescript"
    response = requests.get(
        f"{BASE_URL}/api/nasa/analytics/predictions?technology={technology}&level=intermediate",
        timeout=5,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"]

    prediction = data["prediction"]
    print(f"✅ Prediction for {technology}")
    print(f"   Predicted proficiency: {prediction['predicted_proficiency']:.1%}")
    print(f"   Confidence: {prediction['confidence']:.1%}")
    print(f"   Estimated attempts: {prediction['estimated_attempts']}")
    print(f"   Success probability: {prediction['success_probability']:.1%}")

    print(f"\n   Contributing factors:")
    for factor, value in prediction["factors"].items():
        print(f"   • {factor}: {value:.3f}")

    return prediction


def test_analytics_insights():
    """Test performance insights"""
    print("\n" + "=" * 60)
    print("🧪 TEST: Performance Insights")
    print("=" * 60)

    response = requests.get(f"{BASE_URL}/api/nasa/analytics/insights", timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data["success"]

    insights = data.get("insights", [])
    print(f"✅ Insights retrieved")
    print(f"   Total insights: {len(insights)}")

    for insight in insights[:3]:
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}[
            insight["priority"]
        ]
        print(f"\n   {priority_emoji} {insight['title']} ({insight['category']})")
        print(f"      {insight['description']}")
        print(f"      💡 {insight['recommendation']}")

    return insights


def main():
    print("\n" + "=" * 70)
    print("🧠 PHASE 3.3 ANALYTICS ENGINE TEST SUITE")
    print("=" * 70)

    results = {}

    try:
        # Test 1: Trends
        results["trends"] = test_analytics_trends()

        # Test 2: Recommendations
        recommendations = test_analytics_recommendations()
        results["recommendations"] = bool(recommendations)

        # Test 3: Predictions
        prediction = test_analytics_predictions()
        results["predictions"] = bool(prediction)

        # Test 4: Insights
        insights = test_analytics_insights()
        results["insights"] = bool(insights)

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
    print(f"Results: {passed}/{total} tests passed ({passed / total * 100:.0f}%)")
    print("=" * 70)

    if passed == total:
        print("\n🎉 ALL ANALYTICS TESTS PASSED!")
        print("\n📊 Analytics Engine Features:")
        print("   ✅ Learning trends analysis")
        print("   ✅ AI-powered recommendations")
        print("   ✅ Success predictions")
        print("   ✅ Performance insights")
        return 0
    else:
        print("\n⚠️ Some tests failed")
        return 1


if __name__ == "__main__":
    exit(main())
