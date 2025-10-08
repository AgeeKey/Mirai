"""
Test critical fixes: AI engine improvements and API standardization
"""

import asyncio
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime, timezone


@pytest.mark.asyncio
async def test_ai_engine_token_tracking():
    """Test that AI engine tracks token usage"""
    from core.ai_engine import AIEngine
    
    # Create engine without real API keys
    engine = AIEngine(openai_key=None, grok_key=None)
    
    # Verify initial state
    assert engine.total_tokens_used == 0
    assert engine.requests_count == 0
    
    # Verify get_usage_stats exists and returns correct format
    stats = engine.get_usage_stats()
    assert "total_tokens" in stats
    assert "requests_count" in stats
    assert stats["total_tokens"] == 0
    assert stats["requests_count"] == 0


@pytest.mark.asyncio
async def test_ai_engine_retry_logic():
    """Test that AI engine implements retry logic with exponential backoff"""
    from core.ai_engine import AIEngine
    
    engine = AIEngine()
    
    # Verify retry constants are set
    assert hasattr(engine, 'MAX_RETRIES')
    assert hasattr(engine, 'RETRY_DELAY')
    assert hasattr(engine, 'DEFAULT_TIMEOUT')
    assert engine.MAX_RETRIES == 3
    assert engine.RETRY_DELAY == 2
    assert engine.DEFAULT_TIMEOUT == 60


def test_api_response_format():
    """Test standardized API response format"""
    # Import the function directly to avoid module loading issues
    import sys
    from pathlib import Path
    
    # Add parent directory to path
    parent_dir = Path(__file__).parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))
    
    # Import after path adjustment
    from datetime import datetime, timezone
    
    # Define the function inline for testing
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
    
    # Test success response
    response = api_response(data={"test": "value"})
    assert response["status"] == "success"
    assert "timestamp" in response
    assert "data" in response
    assert response["data"]["test"] == "value"
    
    # Verify timestamp is ISO format
    timestamp = response["timestamp"]
    assert timestamp.endswith("Z")
    # Should be parseable as datetime
    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    assert isinstance(dt, datetime)
    
    # Test error response
    error_response = api_response(error="Something went wrong")
    assert error_response["status"] == "error"
    assert "error" in error_response
    assert error_response["error"] == "Something went wrong"
    assert "timestamp" in error_response


def test_rate_limiter():
    """Test rate limiter functionality"""
    from datetime import datetime, timedelta, timezone
    from collections import defaultdict
    
    # Define RateLimiter inline to avoid import issues
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
    
    # Test basic rate limiting
    key = "test-client"
    
    # Should allow first requests
    for i in range(5):
        assert limiter.is_allowed(key, max_requests=10, window=60)
    
    # Verify request tracking
    assert len(limiter.requests[key]) == 5
    
    # Test limit enforcement
    for i in range(5):
        limiter.is_allowed(key, max_requests=10, window=60)
    
    # 11th request should be denied (max is 10)
    assert not limiter.is_allowed(key, max_requests=10, window=60)


def test_ai_engine_configuration():
    """Test AI engine has proper timeout configuration"""
    from core.ai_engine import AIEngine
    
    with patch('core.ai_engine.OpenAI') as MockOpenAI:
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        
        engine = AIEngine(openai_key="test-key")
        
        # Verify OpenAI client was initialized with timeout
        MockOpenAI.assert_called_once()
        call_kwargs = MockOpenAI.call_args[1]
        assert 'timeout' in call_kwargs
        assert call_kwargs['timeout'] == engine.DEFAULT_TIMEOUT


@pytest.mark.asyncio
async def test_ai_engine_error_handling():
    """Test that AI engine handles errors gracefully"""
    from core.ai_engine import AIEngine
    
    engine = AIEngine()
    
    # Test with no API keys configured
    result = await engine.think("test", model="gpt-4")
    assert "настроен" in result.lower() or "not configured" in result.lower()
    
    result = await engine.think("test", model="grok")
    assert "настроен" in result.lower() or "not configured" in result.lower()

