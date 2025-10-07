"""Настройки pytest для запуска тестов."""

import os
import sys
from pathlib import Path


# Добавляем корневую директорию проекта в PYTHONPATH
# для корректного импорта модулей в тестах
sys.path.insert(0, str(Path(__file__).parent.parent))