#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Structured Logger                                            ║
║  Production-Grade Logging with JSON Format & Rotation               ║
╚══════════════════════════════════════════════════════════════════════╝

Version: 2.0.0
Codename: Evolution

Features:
- ✅ Structured JSON logging (для машинной обработки)
- ✅ Log rotation (10 MB, 5 backups)
- ✅ Custom fields (model, tokens, latency, user_id)
- ✅ Performance tracking
- ✅ Integration with monitoring
- ✅ Graceful fallback to console
"""

import json
import logging
import logging.handlers
import os
import sys
import time
import traceback
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# ═══════════════════════════════════════════════════════════════════
# Custom JSON Formatter
# ═══════════════════════════════════════════════════════════════════


class JSONFormatter(logging.Formatter):
    """
    Форматтер для structured JSON logging

    Каждая запись - это JSON объект с полями:
    - timestamp
    - level
    - module
    - message
    - model (если указан)
    - tokens_in / tokens_out (если указаны)
    - latency_ms (если указан)
    - user_id (если указан)
    - error (если есть exception)
    - trace (если есть traceback)
    """

    def __init__(self, include_fields: Optional[list] = None):
        super().__init__()
        self.include_fields = include_fields or [
            "timestamp",
            "level",
            "module",
            "message",
            "model",
            "tokens_in",
            "tokens_out",
            "latency_ms",
            "attempt_number",
            "error_code",
            "user_id",
        ]

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        # Base fields
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        # Add custom fields if present
        for field in self.include_fields:
            if hasattr(record, field):
                value = getattr(record, field)
                if value is not None:
                    log_data[field] = value

        # Add exception info if present
        if record.exc_info:
            log_data["error"] = str(record.exc_info[1])
            log_data["error_type"] = (
                record.exc_info[0].__name__ if record.exc_info[0] else None
            )
            log_data["trace"] = self.formatException(record.exc_info)

        # Add extra fields from LoggerAdapter
        if hasattr(record, "_extra"):
            log_data.update(record._extra)

        return json.dumps(log_data, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════
# Custom Text Formatter (для человека)
# ═══════════════════════════════════════════════════════════════════


class ColoredFormatter(logging.Formatter):
    """
    Цветной форматтер для консоли

    Уровни:
    - DEBUG: серый
    - INFO: зелёный
    - WARNING: жёлтый
    - ERROR: красный
    - CRITICAL: красный + bold
    """

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[1;31m",  # Bold Red
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format with colors"""
        # Color for level
        level_color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]

        # Format: [TIME] LEVEL module.function: message
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")

        formatted = (
            f"[{timestamp}] "
            f"{level_color}{record.levelname:8}{reset} "
            f"{record.module}.{record.funcName}: "
            f"{record.getMessage()}"
        )

        # Add custom fields if present
        extras = []
        if hasattr(record, "model"):
            extras.append(f"model={record.model}")
        if hasattr(record, "tokens_in"):
            extras.append(f"tokens={record.tokens_in}")
        if hasattr(record, "latency_ms"):
            extras.append(f"latency={record.latency_ms}ms")

        if extras:
            formatted += f" ({', '.join(extras)})"

        # Add exception if present
        if record.exc_info:
            formatted += "\n" + self.formatException(record.exc_info)

        return formatted


# ═══════════════════════════════════════════════════════════════════
# MIRAI Logger
# ═══════════════════════════════════════════════════════════════════


class MiraiLogger:
    """
    MIRAI Production Logger

    Features:
    - JSON logging to file (structured)
    - Colored logging to console (human-readable)
    - Log rotation (size-based)
    - Custom fields (model, tokens, latency)
    - Performance tracking
    - Context managers for operations
    """

    def __init__(
        self,
        name: str = "mirai",
        log_file: Optional[str] = None,
        level: str = "INFO",
        format_type: str = "json",  # "json" or "text"
        rotate_max_bytes: int = 10 * 1024 * 1024,  # 10 MB
        rotate_backup_count: int = 5,
        console_output: bool = True,
    ):
        """
        Initialize MIRAI Logger

        Args:
            name: Logger name
            log_file: Path to log file (None = no file logging)
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format_type: "json" or "text"
            rotate_max_bytes: Max file size before rotation
            rotate_backup_count: Number of backup files
            console_output: Also log to console
        """
        self.name = name
        self.log_file = Path(log_file) if log_file else None
        self.level = getattr(logging, level.upper())
        self.format_type = format_type

        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        self.logger.handlers = []  # Clear existing handlers

        # Add file handler if log_file specified
        if self.log_file:
            self._add_file_handler(rotate_max_bytes, rotate_backup_count)

        # Add console handler
        if console_output:
            self._add_console_handler()

        # Performance tracking
        self._operation_start_times: Dict[str, float] = {}

    def _add_file_handler(self, max_bytes: int, backup_count: int):
        """Add rotating file handler"""
        # Create log directory if needed
        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Create rotating handler
        handler = logging.handlers.RotatingFileHandler(
            str(self.log_file),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        handler.setLevel(self.level)

        # Set formatter
        if self.format_type == "json":
            handler.setFormatter(JSONFormatter())
        else:
            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )

        self.logger.addHandler(handler)

    def _add_console_handler(self):
        """Add console handler with colors"""
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.level)
        handler.setFormatter(ColoredFormatter())
        self.logger.addHandler(handler)

    # ═══════════════════════════════════════════════════════════════
    # Basic Logging Methods
    # ═══════════════════════════════════════════════════════════════

    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, extra=kwargs)

    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, extra=kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, extra=kwargs)

    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, extra=kwargs)

    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message, extra=kwargs)

    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        self.logger.exception(message, extra=kwargs)

    # ═══════════════════════════════════════════════════════════════
    # Custom Logging Methods (MIRAI specific)
    # ═══════════════════════════════════════════════════════════════

    def log_ai_request(
        self,
        model: str,
        prompt: str,
        tokens_in: int,
        user_id: Optional[str] = None,
        **kwargs,
    ):
        """Log AI API request"""
        self.info(
            f"AI request: {prompt[:50]}...",
            model=model,
            tokens_in=tokens_in,
            user_id=user_id,
            **kwargs,
        )

    def log_ai_response(
        self,
        model: str,
        tokens_in: int,
        tokens_out: int,
        latency_ms: float,
        success: bool = True,
        error_code: Optional[str] = None,
        **kwargs,
    ):
        """Log AI API response"""
        level = self.info if success else self.error
        level(
            f"AI response: {tokens_out} tokens in {latency_ms:.0f}ms",
            model=model,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            latency_ms=latency_ms,
            error_code=error_code,
            **kwargs,
        )

    def log_memory_operation(
        self, operation: str, session_id: str, details: Optional[str] = None, **kwargs
    ):
        """Log memory operation"""
        message = f"Memory {operation}: {session_id}"
        if details:
            message += f" - {details}"
        self.debug(message, **kwargs)

    def log_task(self, task_id: int, status: str, description: str, **kwargs):
        """Log task status"""
        self.info(
            f"Task {task_id} {status}: {description[:50]}...",
            task_id=task_id,
            status=status,
            **kwargs,
        )

    def log_metric(self, metric_name: str, value: float, unit: str = "", **kwargs):
        """Log performance metric"""
        message = f"Metric {metric_name}: {value}"
        if unit:
            message += f" {unit}"
        self.info(message, metric=metric_name, value=value, unit=unit, **kwargs)

    # ═══════════════════════════════════════════════════════════════
    # Context Managers (для автоматического логирования)
    # ═══════════════════════════════════════════════════════════════

    @contextmanager
    def operation(self, operation_name: str, **context):
        """
        Context manager для логирования операции с timing

        Usage:
            with logger.operation("database_query", query="SELECT *"):
                # do work
                pass
        """
        start_time = time.time()
        self.debug(f"Starting {operation_name}", **context)

        try:
            yield
            latency_ms = (time.time() - start_time) * 1000
            self.info(f"Completed {operation_name}", latency_ms=latency_ms, **context)
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            self.error(
                f"Failed {operation_name}: {e}",
                latency_ms=latency_ms,
                error=str(e),
                **context,
            )
            raise

    @contextmanager
    def ai_call(self, model: str, prompt: str, **context):
        """
        Context manager для логирования AI вызова

        Usage:
            with logger.ai_call("gpt-4o-mini", "Hello"):
                response = call_openai()
        """
        start_time = time.time()

        # Log request
        self.log_ai_request(
            model=model,
            prompt=prompt,
            tokens_in=len(prompt.split()),  # Approximation
            **context,
        )

        try:
            yield
            latency_ms = (time.time() - start_time) * 1000
            self.debug(f"AI call completed in {latency_ms:.0f}ms")
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            self.error(f"AI call failed: {e}", latency_ms=latency_ms, error=str(e))
            raise

    # ═══════════════════════════════════════════════════════════════
    # Utility Methods
    # ═══════════════════════════════════════════════════════════════

    def set_level(self, level: str):
        """Change log level dynamically"""
        new_level = getattr(logging, level.upper())
        self.logger.setLevel(new_level)
        for handler in self.logger.handlers:
            handler.setLevel(new_level)
        self.info(f"Log level changed to {level.upper()}")

    def get_stats(self) -> Dict[str, Any]:
        """Get logger statistics"""
        stats = {
            "name": self.name,
            "level": logging.getLevelName(self.level),
            "handlers": len(self.logger.handlers),
            "format": self.format_type,
        }

        if self.log_file and self.log_file.exists():
            stats["log_file"] = str(self.log_file)
            stats["log_size_mb"] = self.log_file.stat().st_size / 1024 / 1024

        return stats


# ═══════════════════════════════════════════════════════════════════
# Global Logger Instance (singleton)
# ═══════════════════════════════════════════════════════════════════

_global_logger: Optional[MiraiLogger] = None


def get_logger(
    name: str = "mirai", log_file: Optional[str] = None, **kwargs
) -> MiraiLogger:
    """
    Get global MIRAI logger instance (singleton)

    Args:
        name: Logger name
        log_file: Path to log file
        **kwargs: Additional arguments for MiraiLogger

    Returns:
        MiraiLogger instance
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = MiraiLogger(name=name, log_file=log_file, **kwargs)
    return _global_logger


def setup_logger_from_config(config: Any) -> MiraiLogger:
    """
    Setup logger from MIRAI config

    Args:
        config: MiraiConfig object from config_loader

    Returns:
        Configured MiraiLogger
    """
    monitoring = config.monitoring
    logs = monitoring.logs

    # Create logger with config settings
    logger = MiraiLogger(
        name="mirai",
        log_file=logs.get("path", "/tmp/mirai.log"),
        level=logs.get("level", "INFO"),
        format_type=logs.get("format", "json"),
        rotate_max_bytes=logs.get("rotate", {}).get("max_bytes", 10485760),
        rotate_backup_count=logs.get("rotate", {}).get("backup_count", 5),
        console_output=True,
    )

    logger.info("Logger initialized from config", config_version=config.version)

    return logger


# ═══════════════════════════════════════════════════════════════════
# Main (Testing)
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║  MIRAI Logger Test                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()

    # Test 1: Basic logging
    print("1️⃣  Basic logging test")
    logger = MiraiLogger(
        name="test",
        log_file="/tmp/mirai_test.log",
        format_type="json",
        console_output=True,
    )

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    print()

    # Test 2: Custom fields
    print("2️⃣  Custom fields test")
    logger.log_ai_request(
        model="gpt-4o-mini", prompt="What is AI?", tokens_in=10, user_id="test_user"
    )

    logger.log_ai_response(
        model="gpt-4o-mini",
        tokens_in=10,
        tokens_out=50,
        latency_ms=1234.5,
        success=True,
    )
    print()

    # Test 3: Context manager
    print("3️⃣  Context manager test")
    with logger.operation("test_operation", test_param="value"):
        time.sleep(0.1)  # Simulate work
    print()

    # Test 4: Exception logging
    print("4️⃣  Exception logging test")
    try:
        raise ValueError("Test exception")
    except Exception as e:
        logger.exception("Caught an exception", error_type="ValueError")
    print()

    # Test 5: Metrics
    print("5️⃣  Metrics logging test")
    logger.log_metric("response_time", 123.45, "ms")
    logger.log_metric("tokens_used", 1000, "tokens")
    print()

    # Test 6: Memory operations
    print("6️⃣  Memory operations test")
    logger.log_memory_operation(
        operation="create_session", session_id="abc-123", details="New user session"
    )
    print()

    # Test 7: Task logging
    print("7️⃣  Task logging test")
    logger.log_task(
        task_id=1, status="completed", description="Implement logger module"
    )
    print()

    # Test 8: Stats
    print("8️⃣  Logger statistics")
    stats = logger.get_stats()
    for key, value in stats.items():
        print(f"   {key:20} {value}")
    print()

    # Test 9: JSON file check
    print("9️⃣  JSON log file check")
    log_file = Path("/tmp/mirai_test.log")
    if log_file.exists():
        print(f"   Log file: {log_file}")
        print(f"   Size: {log_file.stat().st_size} bytes")
        print()
        print("   Last 3 JSON entries:")
        with open(log_file, "r") as f:
            lines = f.readlines()
            for line in lines[-3:]:
                data = json.loads(line)
                print(f"   [{data['level']:8}] {data['message']}")
    print()

    print("✅ All tests passed!")
    print()
    print(f"Logs written to: {log_file}")
    print()
    print("To view JSON logs:")
    print(f"  tail -f {log_file} | jq .")
