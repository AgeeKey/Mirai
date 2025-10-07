"""Helpers for accessing agent configuration."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from core.config import Config


def load_agent_settings() -> Dict[str, Any]:
    """Return agent settings as a dictionary sourced from core config."""
    config = Config.load()
    return asdict(config.agent_settings)


def get_advisor_config() -> Dict[str, Any]:
    """Shortcut returning advisor-specific thresholds."""
    settings = Config.load().agent_settings
    return {
        "ADVISOR_THRESHOLD": settings.advisor_threshold,
        "RECOVERY_THRESHOLD": settings.recovery_threshold,
        "RECOVERY_MAX_TRIES": settings.recovery_max_tries,
    }
