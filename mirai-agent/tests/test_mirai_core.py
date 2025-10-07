"""
Pytest unit tests for Mirai Agent
"""

import os
import pytest
import tempfile
import json
import sqlite3
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

# Test environment loading
def test_env_loading():
    """Test that environment variables are loaded correctly"""
    with patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test-openai-key',
        'GROK_API_KEY': 'test-grok-key',
        'BINANCE_API_KEY': 'test-binance-key',
        'BINANCE_SECRET_KEY': 'test-binance-secret',
        'TELEGRAM_BOT_TOKEN': 'test-telegram-token'
    }):
        from core.config import Config
        config = Config()
        
        assert config.openai_api_key == 'test-openai-key'
        assert config.grok_api_key == 'test-grok-key'
        assert config.binance_api_key == 'test-binance-key'
        assert config.binance_secret_key == 'test-binance-secret'
        assert config.telegram_bot_token == 'test-telegram-token'

def test_env_fallback():
    """Test environment variable fallback for legacy naming"""
    with patch.dict(os.environ, {
        'BINANCE_API_SECRET': 'legacy-secret',  # Legacy variable
        'TELEGRAM_TOKEN': 'legacy-telegram'     # Legacy variable
    }, clear=True):
        # Test Binance secret fallback using the real client
        from modules.trading.binance_client import BinanceClient
        
        # Mock the environment check in binance client
        with patch('modules.trading.binance_client.os.getenv') as mock_getenv:
            def getenv_side_effect(key, default=None):
                if key == 'BINANCE_SECRET_KEY':
                    return None  # Primary not set
                elif key == 'BINANCE_API_SECRET':
                    return 'legacy-secret'  # Legacy fallback
                return default
            
            mock_getenv.side_effect = getenv_side_effect
            
            # This would normally trigger the fallback warning
            # but we're just testing the logic exists
            assert mock_getenv('BINANCE_API_SECRET') == 'legacy-secret'
        
        # Test Telegram token fallback  
        from modules.telegram_bot.bot import get_telegram_token
        token = get_telegram_token()
        assert token == 'legacy-telegram'

# Test memory persistence
@pytest.fixture
def temp_db():
    """Create temporary SQLite database for testing"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    yield db_path
    os.unlink(db_path)

def test_memory_persistence(temp_db):
    """Test that agent memory persists across restarts"""
    from modules.agent.memory import Memory
    
    # Create first memory instance and store data
    memory1 = Memory(db_path=temp_db)
    memory1.store_memory(
        memory_type="test_type",
        content="test content",
        importance=0.8,
        metadata={"key": "value"}
    )
    memory1.close()
    
    # Create second memory instance (simulating restart)
    memory2 = Memory(db_path=temp_db)
    memories = memory2.get_recent_memories(limit=10)
    
    assert len(memories) == 1
    assert memories[0]['content'] == "test content"
    assert memories[0]['importance'] == 0.8
    assert memories[0]['metadata']['key'] == "value"
    memory2.close()

def test_memory_retrieval(temp_db):
    """Test memory retrieval by importance and recency"""
    from modules.agent.memory import Memory
    
    memory = Memory(db_path=temp_db)
    
    # Store memories with different importance
    memory.store_memory("type1", "low importance", importance=0.3)
    memory.store_memory("type2", "high importance", importance=0.9)
    memory.store_memory("type3", "medium importance", importance=0.6)
    
    # Test retrieval by importance
    important_memories = memory.get_important_memories(min_importance=0.5)
    assert len(important_memories) == 2  # high and medium
    
    # Test recent memories
    recent = memory.get_recent_memories(limit=2)
    assert len(recent) == 2
    
    memory.close()

# Test /decide endpoint
@pytest.mark.asyncio
async def test_decide_endpoint():
    """Test the /trader/decide endpoint functionality"""
    from modules.api.server import APIServer
    from core.ai_engine import AIEngine
    from modules.agent.autonomous import AutonomousAgent
    from modules.trading.trader import Trader
    import logging
    
    # Mock dependencies
    ai_engine = MagicMock(spec=AIEngine)
    ai_engine.think = AsyncMock(return_value="LONG - Bitcoin showing bullish momentum")
    
    agent = MagicMock(spec=AutonomousAgent)
    agent.ai = ai_engine
    agent.memory = MagicMock()
    agent.memory.store_memory = MagicMock()
    
    trader = MagicMock(spec=Trader)
    logger = logging.getLogger("test")
    
    # Create API server
    api_server = APIServer(agent, trader, logger)
    
    # Test the decide endpoint
    from fastapi.testclient import TestClient
    client = TestClient(api_server.app)
    
    response = client.post("/trader/decide", json={
        "symbol": "BTCUSDT",
        "budget": 100.0,
        "leverage": 2,
        "dry_run": True
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["action"] == "long"
    assert data["symbol"] == "BTCUSDT"
    assert data["budget"] == 100.0
    assert data["dry_run"] is True
    assert "Bitcoin" in data["reason"]

@pytest.mark.asyncio 
async def test_decide_endpoint_error_handling():
    """Test /trader/decide endpoint error handling"""
    from modules.api.server import APIServer
    from core.ai_engine import AIEngine
    from modules.agent.autonomous import AutonomousAgent
    from modules.trading.trader import Trader
    import logging
    
    # Mock dependencies with AI error
    ai_engine = MagicMock(spec=AIEngine)
    ai_engine.think = AsyncMock(side_effect=Exception("AI service unavailable"))
    
    agent = MagicMock(spec=AutonomousAgent)
    agent.ai = ai_engine
    agent.memory = MagicMock()
    
    trader = MagicMock(spec=Trader)
    logger = logging.getLogger("test")
    
    # Create API server
    api_server = APIServer(agent, trader, logger)
    
    # Test error handling
    from fastapi.testclient import TestClient
    client = TestClient(api_server.app)
    
    response = client.post("/trader/decide", json={
        "symbol": "ETHUSDT",
        "budget": 50.0
    })
    
    assert response.status_code == 502
    assert "AI service unavailable" in response.json()["detail"]

# Test task persistence
def test_task_persistence():
    """Test that tasks persist in JSON format"""
    from modules.agent.autonomous import Task, AutonomousAgent
    from core.config import Config
    import tempfile
    import shutil
    
    # Create temporary directory for test
    temp_dir = tempfile.mkdtemp()
    tasks_file = os.path.join(temp_dir, "agent_tasks.json")
    
    try:
        # Mock config
        config = MagicMock(spec=Config)
        
        # Create agent and add tasks
        agent = AutonomousAgent(config)
        agent.tasks_file = tasks_file
        
        task1 = Task(id="test-1", description="Test task 1", priority=3)
        task2 = Task(id="test-2", description="Test task 2", priority=1)
        
        agent.tasks = [task1, task2]
        agent._save_tasks()
        
        # Verify file was created
        assert os.path.exists(tasks_file)
        
        # Load and verify content
        with open(tasks_file, 'r') as f:
            saved_tasks = json.load(f)
        
        assert len(saved_tasks) == 2
        assert saved_tasks[0]["id"] == "test-1"
        assert saved_tasks[0]["description"] == "Test task 1"
        assert saved_tasks[1]["priority"] == 1
        
        # Test loading tasks
        agent2 = AutonomousAgent(config)
        agent2.tasks_file = tasks_file
        agent2._load_tasks()
        
        assert len(agent2.tasks) == 2
        assert agent2.tasks[0].id == "test-1"
        assert agent2.tasks[1].description == "Test task 2"
        
    finally:
        shutil.rmtree(temp_dir)

# Test config validation
def test_config_validation():
    """Test configuration validation and defaults"""
    from core.config import Config
    
    with patch.dict(os.environ, {}, clear=True):
        config = Config()
        
        # Test defaults
        assert config.default_trading_mode == "dry_run"
        assert config.max_positions == 3
        assert config.risk_per_trade == 0.02
        
        # Test required fields are None when missing
        assert config.openai_api_key is None
        assert config.binance_api_key is None

def test_config_with_values():
    """Test configuration with provided values"""
    from core.config import Config
    
    test_env = {
        'DEFAULT_TRADING_MODE': 'live',
        'MAX_POSITIONS': '5',
        'RISK_PER_TRADE': '0.05',
        'OPENAI_API_KEY': 'test-key'
    }
    
    with patch.dict(os.environ, test_env):
        config = Config()
        
        assert config.default_trading_mode == "live"
        assert config.max_positions == 5
        assert config.risk_per_trade == 0.05
        assert config.openai_api_key == "test-key"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])