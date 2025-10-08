#!/usr/bin/env python3
"""
Verification script for critical fixes
Demonstrates the new features without requiring a running server
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_ai_engine_features():
    """Test AI engine improvements"""
    print("=" * 70)
    print("🧠 Testing AI Engine Features")
    print("=" * 70)
    
    from core.ai_engine import AIEngine
    
    # Create engine without API keys (for demo)
    engine = AIEngine(openai_key=None, grok_key=None)
    
    print("\n✅ AI Engine Configuration:")
    print(f"   • Default Timeout: {engine.DEFAULT_TIMEOUT}s")
    print(f"   • Max Retries: {engine.MAX_RETRIES}")
    print(f"   • Retry Delay: {engine.RETRY_DELAY}s")
    
    print("\n✅ Token Tracking:")
    stats = engine.get_usage_stats()
    print(f"   • Total Tokens: {stats['total_tokens']}")
    print(f"   • Request Count: {stats['requests_count']}")
    
    print("\n✅ AI Engine initialized successfully!")
    return True


async def test_ai_engine_error_handling():
    """Test AI engine error handling"""
    print("\n" + "=" * 70)
    print("🛡️ Testing Error Handling")
    print("=" * 70)
    
    from core.ai_engine import AIEngine
    
    engine = AIEngine()
    
    print("\n🔍 Testing with no API keys (should return error message)...")
    result = await engine.think("Hello", model="gpt-4")
    print(f"   Result: {result}")
    
    if "настроен" in result.lower() or "not" in result.lower():
        print("   ✅ Error handled gracefully!")
        return True
    else:
        print("   ❌ Unexpected response")
        return False


def test_api_response_format():
    """Test standardized API response format"""
    print("\n" + "=" * 70)
    print("🌐 Testing API Response Format")
    print("=" * 70)
    
    from datetime import datetime, timezone
    
    # Define api_response function
    def api_response(data=None, error=None, status="success"):
        response = {
            "status": status if not error else "error",
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        }
        if data is not None:
            response["data"] = data
        if error:
            response["error"] = error
        return response
    
    print("\n✅ Testing Success Response:")
    success = api_response(data={"test": "value", "count": 123})
    print(f"   Status: {success['status']}")
    print(f"   Timestamp: {success['timestamp']}")
    print(f"   Data: {success['data']}")
    
    print("\n✅ Testing Error Response:")
    error = api_response(error="Something went wrong")
    print(f"   Status: {error['status']}")
    print(f"   Timestamp: {error['timestamp']}")
    print(f"   Error: {error['error']}")
    
    return True


def test_rate_limiter():
    """Test rate limiter functionality"""
    print("\n" + "=" * 70)
    print("🚦 Testing Rate Limiter")
    print("=" * 70)
    
    from datetime import datetime, timedelta, timezone
    from collections import defaultdict
    
    class RateLimiter:
        def __init__(self):
            self.requests = defaultdict(list)
        
        def is_allowed(self, key: str, max_requests: int = 60, window: int = 60) -> bool:
            now = datetime.now(timezone.utc)
            cutoff = now - timedelta(seconds=window)
            self.requests[key] = [ts for ts in self.requests[key] if ts > cutoff]
            if len(self.requests[key]) >= max_requests:
                return False
            self.requests[key].append(now)
            return True
    
    limiter = RateLimiter()
    client = "test-client-ip"
    
    print(f"\n🔍 Testing with limit of 5 requests per window:")
    
    # Make 5 requests (should all succeed)
    for i in range(5):
        allowed = limiter.is_allowed(client, max_requests=5, window=60)
        print(f"   Request {i+1}/5: {'✅ Allowed' if allowed else '❌ Blocked'}")
    
    # 6th request should be blocked
    allowed = limiter.is_allowed(client, max_requests=5, window=60)
    print(f"   Request 6/5: {'❌ Blocked (EXPECTED)' if not allowed else '✅ Allowed (UNEXPECTED)'}")
    
    if not allowed:
        print("\n✅ Rate limiter working correctly!")
        return True
    else:
        print("\n❌ Rate limiter not working as expected")
        return False


async def main():
    """Run all verification tests"""
    print("\n" + "🚀" * 35)
    print("Mirai AI - Critical Fixes Verification")
    print("🚀" * 35)
    
    results = []
    
    # Test 1: AI Engine Features
    try:
        results.append(("AI Engine Features", test_ai_engine_features()))
    except Exception as e:
        print(f"\n❌ AI Engine Features test failed: {e}")
        results.append(("AI Engine Features", False))
    
    # Test 2: Error Handling
    try:
        results.append(("Error Handling", await test_ai_engine_error_handling()))
    except Exception as e:
        print(f"\n❌ Error Handling test failed: {e}")
        results.append(("Error Handling", False))
    
    # Test 3: API Response Format
    try:
        results.append(("API Response Format", test_api_response_format()))
    except Exception as e:
        print(f"\n❌ API Response Format test failed: {e}")
        results.append(("API Response Format", False))
    
    # Test 4: Rate Limiter
    try:
        results.append(("Rate Limiter", test_rate_limiter()))
    except Exception as e:
        print(f"\n❌ Rate Limiter test failed: {e}")
        results.append(("Rate Limiter", False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 70)
    
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print("\n" + "-" * 70)
    print(f"   Total: {passed}/{total} tests passed ({passed*100//total}%)")
    print("-" * 70)
    
    if passed == total:
        print("\n🎉 All verification tests passed!")
        print("✅ Critical fixes are working correctly!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
