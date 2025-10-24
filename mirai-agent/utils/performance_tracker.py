"""Lightweight performance tracking utilities for MIRAI components.

The tracker aggregates execution timings for registered operations and stores
summary statistics under ``metrics/performance_metrics.json`` at the project
root.  The goal is to provide cheap observability without introducing heavy
dependencies or external services.
"""

from __future__ import annotations

import json
import threading
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, Generator, Optional

import atexit

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "metrics" / "performance_metrics.json"


class PerformanceTracker:
    """Collects basic timing metrics and persists them to disk."""

    def __init__(
        self,
        output_path: Path = DEFAULT_OUTPUT_PATH,
        auto_flush: bool = False,
    ):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.auto_flush = auto_flush
        self._lock = threading.Lock()
        self._metrics: Dict[str, Dict[str, Dict[str, float]]] = {}
        self._dirty = False
        self._load_existing()
        atexit.register(self.flush)

    # ------------------------------------------------------------------ utils
    def _load_existing(self) -> None:
        if self.output_path.exists():
            try:
                with self.output_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self._metrics = data
            except Exception:
                # Corrupted file: start fresh but do not crash the application.
                self._metrics = {}

    def _write(self) -> None:
        with self.output_path.open("w", encoding="utf-8") as f:
            json.dump(self._metrics, f, indent=2, ensure_ascii=False)
        self._dirty = False

    def _ensure_entry(self, component: str, operation: str) -> Dict[str, float]:
        component_metrics = self._metrics.setdefault(component, {})
        entry = component_metrics.get(operation)
        if entry is None:
            entry = {
                "count": 0,
                "total_ms": 0.0,
                "avg_ms": 0.0,
                "max_ms": 0.0,
                "min_ms": 0.0,
                "last_ms": 0.0,
                "last_timestamp": "",
            }
            component_metrics[operation] = entry
        return entry

    # ---------------------------------------------------------------- record
    def record(
        self,
        component: str,
        operation: str,
        duration_ms: float,
        metadata: Optional[Dict[str, str]] = None,
    ) -> None:
        """Store a measurement."""
        timestamp = datetime.utcnow().isoformat() + "Z"
        with self._lock:
            entry = self._ensure_entry(component, operation)
            entry["count"] += 1
            entry["total_ms"] += duration_ms
            entry["avg_ms"] = entry["total_ms"] / entry["count"]
            entry["max_ms"] = max(entry["max_ms"], duration_ms) if entry["count"] > 1 else duration_ms
            entry["min_ms"] = (
                min(entry["min_ms"], duration_ms) if entry["count"] > 1 else duration_ms
            )
            entry["last_ms"] = duration_ms
            entry["last_timestamp"] = timestamp
            if metadata:
                entry["metadata"] = metadata

            self._dirty = True
            if self.auto_flush:
                self.flush()

    # ---------------------------------------------------------------- context
    @contextmanager
    def track(
        self,
        component: str,
        operation: str,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Generator[None, None, None]:
        """Context manager that times the enclosed block."""
        start = time.perf_counter()
        try:
            yield
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            self.record(component, operation, duration_ms, metadata)

    # ---------------------------------------------------------------- export
    def snapshot(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        """Return a shallow copy of the current metrics."""
        with self._lock:
            return json.loads(json.dumps(self._metrics))

    def flush(self) -> None:
        """Persist metrics to disk if there were changes."""
        with self._lock:
            if self._dirty or not self.output_path.exists():
                self._write()


# Global tracker instance used by the application.
performance_tracker = PerformanceTracker()


__all__ = ["PerformanceTracker", "performance_tracker"]
