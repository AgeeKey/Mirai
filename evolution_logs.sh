#!/bin/bash
# 📊 Логи МИРАЙ в реальном времени

echo "📊 Логи МИРАЙ (Ctrl+C для выхода)"
echo "=================================="
echo ""

tail -f /tmp/mirai_autonomous.log
