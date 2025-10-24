"""Compatibility proxy for the MIRAI configuration loader.

Historically code imported ``core.config_loader`` from the repository root.
The actual implementation now lives in ``core/_config_loader_base.py`` but
this module keeps a relaxed fallback path that still works when the full
``mirai-agent`` tree is not present.
"""

from __future__ import annotations

import logging
import sys
from importlib import import_module
from pathlib import Path

logger = logging.getLogger(__name__)

_MIRAI_AGENT_ROOT = Path(__file__).resolve().parent.parent / "mirai-agent"


def _load_shared_module():
    try:
        return import_module("core._config_loader_base")
    except ModuleNotFoundError:
        if _MIRAI_AGENT_ROOT.exists():
            sys.path.insert(0, str(_MIRAI_AGENT_ROOT))
            try:
                return import_module("core._config_loader_base")
            except ModuleNotFoundError as exc:  # pragma: no cover
                raise ImportError(
                    "Unable to import the MIRAI config loader implementation; "
                    "ensure either core/_config_loader_base.py or the mirai-agent "
                    "package is available."
                ) from exc
        raise


_shared = _load_shared_module()

# Re-export everything from the shared module.
__all__ = getattr(_shared, "__all__", [])
if not __all__:
    __all__ = [name for name in dir(_shared) if not name.startswith("_")]

globals().update({name: getattr(_shared, name) for name in __all__})
