"""Proxy module that loads the shared configuration loader implementation.

Keeps the mirai-agent package backward compatible while delegating the real
logic to the repository-level ``core/_config_loader_base.py`` file.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_shared_module():
    shared_path = Path(__file__).resolve().parents[2] / "core" / "_config_loader_base.py"
    if not shared_path.exists():
        raise ImportError(
            "Shared config loader implementation not found. "
            "Expected at {}".format(shared_path)
        )

    spec = importlib.util.spec_from_file_location(
        "mirai_shared_config_loader", shared_path
    )
    if spec is None or spec.loader is None:
        raise ImportError("Failed to create module spec for config loader")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    return module


_shared = _load_shared_module()

# Re-export everything defined in the shared module
__all__ = getattr(_shared, "__all__", [])
if not __all__:
    __all__ = [name for name in dir(_shared) if not name.startswith("_")]

globals().update({name: getattr(_shared, name) for name in __all__})
