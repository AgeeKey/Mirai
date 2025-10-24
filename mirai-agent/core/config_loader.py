"""Shim module that re-exports the shared MIRAI configuration loader.

The full implementation lives in ``core._config_loader_base`` so it can be
shared between the historical ``core`` package at the repository root and the
main agent package.  Keep all config loader logic in the base module; this file
should only contain re-export glue.
"""

from ._config_loader_base import *  # noqa: F401,F403

__all__ = [  # type: ignore[var-annotated]
    name for name in globals().keys() if not name.startswith("_")
]
