"""
CONFIG - Единая конфигурация проекта.
"""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class TradingConfig:
    """Конфигурация торговли."""

    exchange: str
    api_key: str
    api_secret: str
    max_position_size: float
    risk_per_trade: float


@dataclass
class AgentSettings:
    """Настройки автономного агента."""

    cycle_interval: int = 300
    max_goals: int = 5
    learning_sessions_limit: int = 3
    advisor_threshold: float = 0.7
    recovery_threshold: float = 0.8
    recovery_max_tries: int = 3


@dataclass
class TraderSettings:
    """Настройки торгового цикла."""

    cycle_interval: int = 600
    demo_mode: bool = True
    max_position_size: float = 1000.0
    stop_loss_percent: float = 0.02
    take_profit_percent: float = 0.04
    max_drawdown: float = 0.05


@dataclass
class Config:
    """Главная конфигурация."""

    openai_key: Optional[str]
    grok_key: Optional[str]
    trading: TradingConfig
    agent_settings: AgentSettings
    trader_settings: TraderSettings
    data_dir: Path
    logs_dir: Path
    host: str
    port: int

    @classmethod
    def load(cls, env: str = "production"):
        """Загрузка конфига из файлов."""

        # 1) Конфиг приложения
        config_file = Path(f"configs/{env}.yaml")
        with config_file.open(encoding="utf-8") as fh:
            settings = yaml.safe_load(fh)

        # 2) Ключи: сначала пробуем переменные окружения, затем (опционально) файл
        openai_key = os.getenv("OPENAI_API_KEY")
        grok_key = os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")

        keys_file = Path("configs/api_keys.json")
        if (not openai_key or not grok_key) and keys_file.exists():
            try:
                with keys_file.open(encoding="utf-8") as fh:
                    keys = json.load(fh)
                openai_key = openai_key or keys.get("openai")
                grok_key = grok_key or keys.get("grok")
            except Exception:
                # Игнорируем ошибки чтения файла ключей
                pass

        agent_raw = settings.get("agent", {})
        trader_raw = settings.get("trader", {})

        return cls(
            openai_key=openai_key,
            grok_key=grok_key,
            trading=TradingConfig(**settings["trading"]),
            agent_settings=AgentSettings(
                cycle_interval=agent_raw.get("cycle_interval", 300),
                max_goals=agent_raw.get("max_goals", 5),
                learning_sessions_limit=agent_raw.get("learning_sessions_limit", 3),
                advisor_threshold=agent_raw.get("advisor_threshold", 0.7),
                recovery_threshold=agent_raw.get("recovery_threshold", 0.8),
                recovery_max_tries=agent_raw.get("recovery_max_tries", 3),
            ),
            trader_settings=TraderSettings(
                cycle_interval=trader_raw.get("cycle_interval", 600),
                demo_mode=trader_raw.get("demo_mode", True),
                max_position_size=trader_raw.get("max_position_size", 1000.0),
                stop_loss_percent=trader_raw.get("stop_loss_percent", 0.02),
                take_profit_percent=trader_raw.get("take_profit_percent", 0.04),
                max_drawdown=trader_raw.get("max_drawdown", 0.05),
            ),
            data_dir=Path(settings["paths"]["data"]),
            logs_dir=Path(settings["paths"]["logs"]),
            host=settings["server"]["host"],
            port=settings["server"]["port"],
        )
