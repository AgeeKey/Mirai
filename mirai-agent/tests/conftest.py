"""
Test configuration and utilities for Mirai Agent tests
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing"""
    original_env = os.environ.copy()
    
    # Set test environment variables
    test_env = {
        'OPENAI_API_KEY': 'test_openai_key',
        'GROK_API_KEY': 'test_grok_key',
        'BINANCE_API_KEY': 'test_binance_key',
        'BINANCE_SECRET_KEY': 'test_binance_secret',
        'TELEGRAM_BOT_TOKEN': 'test_telegram_token',
        'TELEGRAM_CHAT_ID_ADMIN': '123456789',
        'JWT_SECRET': 'test_jwt_secret',
        'DRY_RUN': 'true',
        'TESTNET': 'true',
    }
    
    os.environ.update(test_env)
    
    yield test_env
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_db_path(temp_dir):
    """Mock database path for testing"""
    return temp_dir / "test_agent_memory.db"


class MockBinanceClient:
    """Mock Binance client for testing"""
    
    def __init__(self, *args, **kwargs):
        self.dry_run = kwargs.get('dry_run', True)
        self.testnet = kwargs.get('testnet', True)
        
    def get_account(self):
        return {
            'totalWalletBalance': '1000.0',
            'availableBalance': '800.0',
            'totalUnrealizedProfit': '0.0'
        }
        
    def get_positions(self):
        return []
        
    def get_open_orders(self, symbol=None):
        return []


class MockAIEngine:
    """Mock AI engine for testing"""
    
    def __init__(self, *args, **kwargs):
        self.calls = []
        
    def think(self, prompt, context=None):
        self.calls.append(('think', prompt, context))
        return "Test AI response"
        
    def decide(self, market_data, analysis):
        self.calls.append(('decide', market_data, analysis))
        return {
            'action': 'hold',
            'confidence': 0.7,
            'reasoning': 'Test decision'
        }


def get_test_telegram_token():
    """Get test telegram token"""
    return os.getenv('TELEGRAM_BOT_TOKEN', 'test_token')
