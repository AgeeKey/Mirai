#!/bin/bash
# Quick test runner for Mirai Agent

set -e

echo "🧪 Running Mirai Agent Tests"
echo "================================"

cd "$(dirname "$0")"

# Check if in virtual environment
if [[ -z "$VIRTUAL_ENV" && -f "../venv/bin/activate" ]]; then
    echo "🔄 Activating virtual environment..."
    source ../venv/bin/activate
fi

# Install test dependencies if needed
if ! python -c "import pytest" 2>/dev/null; then
    echo "📦 Installing test dependencies..."
    pip install -r tests/requirements-test.txt
fi

# Set PYTHONPATH to include the mirai-agent directory
export PYTHONPATH="$(pwd):$PYTHONPATH"

echo "🏃 Running tests..."
echo ""

# Run tests with verbose output
python -m pytest tests/ -v --tb=short

echo ""
echo "✅ Tests completed!"