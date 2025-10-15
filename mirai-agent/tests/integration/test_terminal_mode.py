"""
Integration test for terminal mode
Tests the interactive terminal interface end-to-end
"""

import subprocess
import sys
import time
from pathlib import Path


def test_terminal_help():
    """Test that terminal mode shows help"""
    result = subprocess.run(
        [sys.executable, "mirai.py", "--mode", "terminal", "--help"],
        cwd=str(Path(__file__).parent.parent.parent.parent),
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0
    assert "MIRAI" in result.stdout or "terminal" in result.stdout.lower()
    print("✅ Terminal help works")


def test_terminal_version():
    """Test version command"""
    result = subprocess.run(
        [sys.executable, "mirai.py", "--version"],
        cwd=str(Path(__file__).parent.parent.parent.parent),
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0
    assert "2.0.0" in result.stdout or "version" in result.stdout.lower()
    print("✅ Version command works")


if __name__ == "__main__":
    print("🧪 Testing Terminal Mode...")
    test_terminal_help()
    test_terminal_version()
    print("🎉 All terminal tests passed!")
