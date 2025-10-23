"""
Docker Code Runner
Secure code execution in isolated Docker containers
"""

import json
import logging
import tempfile
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ExecutionStatus(Enum):
    """Execution status codes"""
    SUCCESS = "success"
    TIMEOUT = "timeout"
    ERROR = "error"
    MEMORY_LIMIT = "memory_limit"
    SECURITY_VIOLATION = "security_violation"
    DOCKER_ERROR = "docker_error"


@dataclass
class ExecutionResult:
    """Result of code execution"""
    status: ExecutionStatus
    output: str
    error: Optional[str]
    execution_time: float
    memory_used: int
    exit_code: int
    container_id: Optional[str] = None


class DockerCodeRunner:
    """
    Execute code in isolated Docker containers
    
    Features:
    - Network isolation (--network none)
    - Memory limits
    - CPU limits
    - Timeout enforcement
    - Automatic cleanup
    """

    def __init__(
        self,
        memory_limit: str = "256m",
        cpu_quota: int = 50000,  # 50% of one CPU
        timeout: int = 30,
        docker_available: bool = True,
    ):
        """
        Initialize Docker code runner

        Args:
            memory_limit: Memory limit (e.g., "256m", "1g")
            cpu_quota: CPU quota in microseconds per 100ms period
            timeout: Execution timeout in seconds
            docker_available: Whether Docker is available (set by check)
        """
        self.memory_limit = memory_limit
        self.cpu_quota = cpu_quota
        self.timeout = timeout
        self.docker_available = self._check_docker() if docker_available else False

        # Docker images for different languages
        self.images = {
            "python": "python:3.11-slim",
            "javascript": "node:18-slim",
            "typescript": "node:18-slim",
            "go": "golang:1.21-alpine",
            "rust": "rust:1.75-slim",
            "bash": "bash:5.2-alpine",
        }

        # Execution statistics
        self.stats = {
            "total_executions": 0,
            "successful": 0,
            "failed": 0,
            "timeouts": 0,
            "avg_execution_time": 0.0,
        }

    def _check_docker(self) -> bool:
        """Check if Docker is available"""
        try:
            import subprocess
            result = subprocess.run(
                ["docker", "version"],
                capture_output=True,
                timeout=5,
            )
            available = result.returncode == 0
            if available:
                logger.info("✅ Docker is available")
            else:
                logger.warning("⚠️ Docker not available")
            return available
        except Exception as e:
            logger.warning(f"⚠️ Docker check failed: {e}")
            return False

    def execute_python(
        self, code: str, timeout: Optional[int] = None
    ) -> ExecutionResult:
        """Execute Python code in Docker container"""
        return self._execute_in_docker(
            code=code,
            language="python",
            command=["python", "-c"],
            timeout=timeout or self.timeout,
        )

    def execute_javascript(
        self, code: str, timeout: Optional[int] = None
    ) -> ExecutionResult:
        """Execute JavaScript code in Docker container"""
        return self._execute_in_docker(
            code=code,
            language="javascript",
            command=["node", "-e"],
            timeout=timeout or self.timeout,
        )

    def execute_bash(
        self, code: str, timeout: Optional[int] = None
    ) -> ExecutionResult:
        """Execute Bash script in Docker container"""
        return self._execute_in_docker(
            code=code,
            language="bash",
            command=["bash", "-c"],
            timeout=timeout or self.timeout,
        )

    def _execute_in_docker(
        self,
        code: str,
        language: str,
        command: List[str],
        timeout: int,
    ) -> ExecutionResult:
        """Execute code in Docker container"""
        import subprocess

        if not self.docker_available:
            return ExecutionResult(
                status=ExecutionStatus.DOCKER_ERROR,
                output="",
                error="Docker is not available. Please install Docker.",
                execution_time=0.0,
                memory_used=0,
                exit_code=-1,
            )

        self.stats["total_executions"] += 1
        start_time = time.time()

        # Get Docker image
        image = self.images.get(language, "python:3.11-slim")

        # Pull image if not present (with timeout)
        try:
            subprocess.run(
                ["docker", "pull", image],
                capture_output=True,
                timeout=120,
                check=True,
            )
        except subprocess.TimeoutExpired:
            logger.warning(f"Docker pull timeout for {image}")
        except subprocess.CalledProcessError:
            logger.warning(f"Failed to pull {image}, assuming it exists locally")
        except Exception as e:
            logger.error(f"Docker pull error: {e}")

        # Create temporary file for code
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=f".{language}", delete=False
        ) as f:
            f.write(code)
            code_file = f.name

        try:
            # Build Docker run command
            docker_cmd = [
                "docker",
                "run",
                "--rm",
                "--network", "none",  # No network access
                "--memory", self.memory_limit,
                "--cpu-quota", str(self.cpu_quota),
                "--security-opt", "no-new-privileges",
                "--cap-drop", "ALL",
                "-v", f"{code_file}:/tmp/code:ro",  # Mount as read-only
                image,
            ]

            # Add execution command
            if language == "python":
                docker_cmd.extend(["python", "/tmp/code"])
            elif language == "javascript":
                docker_cmd.extend(["node", "/tmp/code"])
            elif language == "bash":
                docker_cmd.extend(["bash", "/tmp/code"])
            else:
                docker_cmd.extend(command + [code])

            # Execute
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                timeout=timeout,
                text=True,
            )

            execution_time = time.time() - start_time

            # Update stats
            self.stats["avg_execution_time"] = (
                self.stats["avg_execution_time"] * (self.stats["total_executions"] - 1)
                + execution_time
            ) / self.stats["total_executions"]

            # Determine status
            if result.returncode == 0:
                status = ExecutionStatus.SUCCESS
                self.stats["successful"] += 1
            else:
                status = ExecutionStatus.ERROR
                self.stats["failed"] += 1

            return ExecutionResult(
                status=status,
                output=result.stdout,
                error=result.stderr if result.stderr else None,
                execution_time=execution_time,
                memory_used=0,  # Would need Docker stats API for accurate value
                exit_code=result.returncode,
            )

        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            self.stats["timeouts"] += 1
            self.stats["failed"] += 1

            return ExecutionResult(
                status=ExecutionStatus.TIMEOUT,
                output="",
                error=f"Execution timeout ({timeout}s)",
                execution_time=execution_time,
                memory_used=0,
                exit_code=-1,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self.stats["failed"] += 1

            return ExecutionResult(
                status=ExecutionStatus.ERROR,
                output="",
                error=str(e),
                execution_time=execution_time,
                memory_used=0,
                exit_code=-1,
            )

        finally:
            # Cleanup temporary file
            try:
                Path(code_file).unlink()
            except:
                pass

    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        return {
            **self.stats,
            "success_rate": (
                (self.stats["successful"] / self.stats["total_executions"] * 100)
                if self.stats["total_executions"] > 0
                else 0.0
            ),
        }

    def cleanup_containers(self):
        """Clean up any dangling containers"""
        import subprocess
        
        try:
            # Remove stopped containers
            subprocess.run(
                ["docker", "container", "prune", "-f"],
                capture_output=True,
                timeout=30,
            )
            logger.info("🧹 Cleaned up Docker containers")
        except Exception as e:
            logger.error(f"Failed to cleanup containers: {e}")


# Fallback: Non-Docker executor for systems without Docker
class SubprocessCodeRunner:
    """
    Fallback executor using subprocess (less secure)
    Use only when Docker is not available
    """

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.stats = {
            "total_executions": 0,
            "successful": 0,
            "failed": 0,
        }

    def execute_python(self, code: str, timeout: Optional[int] = None) -> ExecutionResult:
        """Execute Python code using subprocess"""
        import subprocess

        self.stats["total_executions"] += 1
        start_time = time.time()

        try:
            result = subprocess.run(
                ["python3", "-c", code],
                capture_output=True,
                timeout=timeout or self.timeout,
                text=True,
            )

            execution_time = time.time() - start_time

            if result.returncode == 0:
                status = ExecutionStatus.SUCCESS
                self.stats["successful"] += 1
            else:
                status = ExecutionStatus.ERROR
                self.stats["failed"] += 1

            return ExecutionResult(
                status=status,
                output=result.stdout,
                error=result.stderr if result.stderr else None,
                execution_time=execution_time,
                memory_used=0,
                exit_code=result.returncode,
            )

        except subprocess.TimeoutExpired:
            self.stats["failed"] += 1
            return ExecutionResult(
                status=ExecutionStatus.TIMEOUT,
                output="",
                error=f"Timeout ({timeout or self.timeout}s)",
                execution_time=time.time() - start_time,
                memory_used=0,
                exit_code=-1,
            )
        except Exception as e:
            self.stats["failed"] += 1
            return ExecutionResult(
                status=ExecutionStatus.ERROR,
                output="",
                error=str(e),
                execution_time=time.time() - start_time,
                memory_used=0,
                exit_code=-1,
            )

    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        return self.stats


if __name__ == "__main__":
    # Test the Docker code runner
    print("🧪 Testing Docker Code Runner...")

    runner = DockerCodeRunner()

    if runner.docker_available:
        # Test Python execution
        print("\n1. Testing Python execution:")
        result = runner.execute_python("print('Hello from Docker!')")
        print(f"   Status: {result.status.value}")
        print(f"   Output: {result.output}")
        print(f"   Time: {result.execution_time:.3f}s")

        # Test with error
        print("\n2. Testing error handling:")
        result = runner.execute_python("1/0")
        print(f"   Status: {result.status.value}")
        print(f"   Error: {result.error}")

        # Test timeout
        print("\n3. Testing timeout:")
        result = runner.execute_python("import time; time.sleep(5)", timeout=2)
        print(f"   Status: {result.status.value}")
        print(f"   Error: {result.error}")

        # Stats
        print(f"\n✅ Stats: {runner.get_stats()}")
    else:
        print("⚠️ Docker not available, skipping tests")
        print("   Install Docker to use isolated code execution")
