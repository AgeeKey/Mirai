"""Тест модуля конфигурации и загрузки переменных окружения."""

import os
from pathlib import Path
from unittest import mock
import sys

import pytest
import yaml

# Добавляем путь к модулям проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import Config, TradingConfig


def test_env_loading_from_env():
    """Test loading API keys from environment variables."""
    with mock.patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "GROK_API_KEY": "test-grok-key"
    }), mock.patch("pathlib.Path.open", mock.mock_open(read_data="""
    trading:
      exchange: binance
      api_key: test-key
      api_secret: test-secret
      max_position_size: 100
      risk_per_trade: 0.01
    paths:
      data: data
      logs: logs
    server:
      host: 0.0.0.0
      port: 8000
    """)), mock.patch("yaml.safe_load", return_value={
        "trading": {
            "exchange": "binance",
            "api_key": "test-key",
            "api_secret": "test-secret",
            "max_position_size": 100,
            "risk_per_trade": 0.01
        },
        "paths": {
            "data": "data",
            "logs": "logs"
        },
        "server": {
            "host": "0.0.0.0",
            "port": 8000
        }
    }):
        config = Config.load()
        
        # Проверки для ключей из окружения
        assert config.openai_key == "test-openai-key"
        assert config.grok_key == "test-grok-key"
        assert isinstance(config.trading, TradingConfig)
        assert config.trading.exchange == "binance"


def test_env_loading_from_file():
    """Test loading API keys from file when not in environment."""
    with mock.patch.dict(os.environ, {}, clear=True), mock.patch("pathlib.Path.exists", return_value=True), mock.patch("pathlib.Path.open", mock.mock_open(read_data='{"openai": "file-openai-key", "grok": "file-grok-key"}')), mock.patch("yaml.safe_load", return_value={
        "trading": {
            "exchange": "binance",
            "api_key": "test-key",
            "api_secret": "test-secret",
            "max_position_size": 100,
            "risk_per_trade": 0.01
        },
        "paths": {
            "data": "data",
            "logs": "logs"
        },
        "server": {
            "host": "0.0.0.0",
            "port": 8000
        }
    }), mock.patch("json.load", return_value={"openai": "file-openai-key", "grok": "file-grok-key"}):
        config = Config.load()
        
        # Проверки для ключей из файла
        assert config.openai_key == "file-openai-key"
        assert config.grok_key == "file-grok-key"


def test_env_loading_legacy_keys():
    """Test loading API keys from legacy environment variables."""
    with mock.patch.dict(os.environ, {
        "XAI_API_KEY": "legacy-grok-key"
    }), mock.patch("pathlib.Path.open", mock.mock_open(read_data="""
    trading:
      exchange: binance
      api_key: test-key
      api_secret: test-secret
      max_position_size: 100
      risk_per_trade: 0.01
    paths:
      data: data
      logs: logs
    server:
      host: 0.0.0.0
      port: 8000
    """)), mock.patch("yaml.safe_load", return_value={
        "trading": {
            "exchange": "binance",
            "api_key": "test-key",
            "api_secret": "test-secret",
            "max_position_size": 100,
            "risk_per_trade": 0.01
        },
        "paths": {
            "data": "data",
            "logs": "logs"
        },
        "server": {
            "host": "0.0.0.0",
            "port": 8000
        }
    }):
        config = Config.load()
        
        # Проверка наличия ключа от XAI как альтернативы GROK
        assert config.grok_key == "legacy-grok-key"


def test_env_loading_binance_keys():
    """Test loading Binance API keys."""
    with mock.patch.dict(os.environ, {
        "BINANCE_API_KEY": "env-binance-key",
        "BINANCE_SECRET_KEY": "env-binance-secret"
    }), mock.patch("pathlib.Path.open", mock.mock_open(read_data="""
    trading:
      exchange: binance
      api_key: file-key
      api_secret: file-secret
      max_position_size: 100
      risk_per_trade: 0.01
    paths:
      data: data
      logs: logs
    server:
      host: 0.0.0.0
      port: 8000
    """)), mock.patch("yaml.safe_load", return_value={
        "trading": {
            "exchange": "binance", 
            "api_key": "file-key",
            "api_secret": "file-secret",
            "max_position_size": 100,
            "risk_per_trade": 0.01
        },
        "paths": {
            "data": "data",
            "logs": "logs"
        },
        "server": {
            "host": "0.0.0.0",
            "port": 8000
        }
    }):
        # Конфигурация из файла должна сохраниться, 
        # т.к. мы не переопределяем поведение через env
        config = Config.load()
        
        assert config.trading.api_key == "file-key"
        assert config.trading.api_secret == "file-secret"