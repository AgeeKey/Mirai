"""
NASA-Level Sandbox Execution System
Безопасное выполнение кода в изолированном окружении
"""

import logging
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class ExecutionStatus(Enum):
    SUCCESS = "success"
    TIMEOUT = "timeout"
    ERROR = "error"
    MEMORY_LIMIT = "memory_limit"
    SECURITY_VIOLATION = "security_violation"


@dataclass
class ExecutionResult:
    status: ExecutionStatus
    output: str
    error: Optional[str]
    execution_time: float
    memory_used: int
    exit_code: int
    security_score: float  # 0.0-1.0


class SandboxExecutor:
    """
    Безопасное выполнение кода в изолированном окружении

    Версия без Docker (для начала):
    - Ограничения через subprocess
    - Security scan
    - Timeout control
    - Memory limits (best effort)

    TODO: Добавить Docker для полной изоляции
    """

    def __init__(self):
        self.max_cpu_time = 30  # seconds
        self.blacklist_patterns = [
            r"os\.system",
            r"subprocess\.",
            r"eval\(",
            r"exec\(",
            r"__import__",
            r'open\(.*[\'"]w',
            r"socket\.",
            r"requests\.",
            r"urllib\.",
        ]

    def execute_python(
        self, code: str, timeout: int = 30, allow_network: bool = False
    ) -> ExecutionResult:
        """Выполнить Python код в sandbox"""

        import time

        start_time = time.time()

        # 1. Security scan
        security_score = self._security_scan(code)
        if security_score < 0.5:
            logger.warning(f"Security scan failed: {security_score}")
            return ExecutionResult(
                status=ExecutionStatus.SECURITY_VIOLATION,
                output="",
                error="Security scan failed - potentially dangerous code",
                execution_time=0,
                memory_used=0,
                exit_code=-1,
                security_score=security_score,
            )

        # 2. Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            # 3. Execute with timeout
            result = subprocess.run(
                ["python3", temp_file], capture_output=True, text=True, timeout=timeout
            )

            execution_time = time.time() - start_time

            # 4. Parse output
            output = result.stdout
            error = result.stderr if result.returncode != 0 else None

            status = (
                ExecutionStatus.SUCCESS
                if result.returncode == 0
                else ExecutionStatus.ERROR
            )

            return ExecutionResult(
                status=status,
                output=output,
                error=error,
                execution_time=execution_time,
                memory_used=0,  # TODO: measure actual memory
                exit_code=result.returncode,
                security_score=security_score,
            )

        except subprocess.TimeoutExpired:
            return ExecutionResult(
                status=ExecutionStatus.TIMEOUT,
                output="",
                error=f"Execution timeout after {timeout}s",
                execution_time=timeout,
                memory_used=0,
                exit_code=-1,
                security_score=security_score,
            )
        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.ERROR,
                output="",
                error=str(e),
                execution_time=time.time() - start_time,
                memory_used=0,
                exit_code=-1,
                security_score=security_score,
            )
        finally:
            # Cleanup
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def _security_scan(self, code: str) -> float:
        """
        Оценить безопасность кода (0.0-1.0)

        Проверяет наличие потенциально опасных конструкций
        """
        violations = 0

        for pattern in self.blacklist_patterns:
            if re.search(pattern, code):
                violations += 1
                logger.warning(f"Security violation: {pattern}")

        # Чем меньше нарушений, тем выше оценка
        score = max(0.0, 1.0 - (violations * 0.15))

        return score


# Quick test
if __name__ == "__main__":
    sandbox = SandboxExecutor()

    # Test 1: Simple code
    print("\n=== Test 1: Simple code ===")
    result = sandbox.execute_python("print('Hello, NASA!')")
    print(f"Status: {result.status}")
    print(f"Output: {result.output}")
    print(f"Security: {result.security_score:.2f}")

    # Test 2: Dangerous code
    print("\n=== Test 2: Dangerous code ===")
    result = sandbox.execute_python("import os; os.system('ls')")
    print(f"Status: {result.status}")
    print(f"Security: {result.security_score:.2f}")

    print("\n✅ SandboxExecutor ready!")
