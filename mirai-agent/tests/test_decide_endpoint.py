"""Тест API эндпоинта /trader/decide."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os

# Добавляем путь к модулям проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.api.server import APIServer


@pytest.fixture
def mock_agent():
    """Создает мок агента для тестов."""
    mock = MagicMock()
    mock.ai = MagicMock()
    mock.ai.think = AsyncMock()
    mock.memory = MagicMock()
    mock.memory.store_memory = MagicMock()
    mock.tasks = []
    mock._save_tasks = MagicMock()
    mock.state = {"tasks_completed": 10, "learning_sessions": 5}
    return mock


@pytest.fixture
def mock_trader():
    """Создает мок трейдера для тестов."""
    mock = MagicMock()
    mock.balance = 1000.0
    mock.positions = []
    mock.mode = "dry_run"
    return mock


@pytest.fixture
def client(mock_agent, mock_trader):
    """Создает тестового клиента с мок-объектами."""
    api_server = APIServer(mock_agent, mock_trader, MagicMock())
    return TestClient(api_server.app)


@pytest.mark.parametrize(
    "ai_response,expected_action",
    [
        ("LONG - Bitcoin looks bullish", "long"),
        ("SHORT - Bitcoin is overbought", "short"),
        ("HOLD - Market is sideways", "hold"),
        ("I'm not sure about the market", "hold"),  # Fallback to hold
    ],
)
@pytest.mark.asyncio
async def test_trader_decide_endpoint(client, mock_agent, ai_response, expected_action):
    """Test trader/decide endpoint parses AI response correctly."""
    # Устанавливаем возвращаемое значение для асинхронного метода think
    mock_agent.ai.think.return_value = ai_response
    
    # Отправляем запрос к эндпоинту
    response = client.post(
        "/trader/decide",
        json={"symbol": "BTCUSDT", "budget": 100, "leverage": 2, "dry_run": True},
    )
    
    # Проверяем результат
    assert response.status_code == 200
    data = response.json()
    assert data["action"] == expected_action
    assert data["symbol"] == "BTCUSDT"
    assert data["budget"] == 100
    assert data["leverage"] == 2
    assert data["dry_run"] is True
    assert "reason" in data
    assert "ts" in data
    
    # Проверяем, что AI think был вызван с правильными параметрами
    mock_agent.ai.think.assert_called_once()
    assert "BTCUSDT" in mock_agent.ai.think.call_args[0][0]
    
    # Проверяем, что решение сохранено в памяти
    mock_agent.memory.store_memory.assert_called_once_with(
        "trading_decision", 
        f"BTCUSDT: {expected_action}", 
        metadata={"payload": {"symbol": "BTCUSDT", "budget": 100, "leverage": 2, "dry_run": True}, 
                  "reason": ai_response[:500]},
        importance=0.6,
    )


@pytest.mark.asyncio
async def test_trader_decide_error_handling(client, mock_agent):
    """Test error handling in trader/decide endpoint."""
    # Эмулируем ошибку в AI
    mock_agent.ai.think.side_effect = Exception("API unavailable")
    
    # Отправляем запрос к эндпоинту
    response = client.post(
        "/trader/decide",
        json={"symbol": "ETHUSDT", "budget": 50},
    )
    
    # Проверяем, что получили ожидаемый код ошибки
    assert response.status_code == 502
    assert "AI error" in response.json()["detail"]