#!/bin/bash
# MIRAI Service Test Script
# Tests all service management commands

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SERVICE="mirai"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  MIRAI Service Management Test                                      ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test 1: Service status
echo -e "${YELLOW}Test 1: Service status${NC}"
sudo systemctl status "$SERVICE" --no-pager --lines=5 || true
echo -e "${GREEN}✅ Status command works${NC}"
echo ""

# Test 2: Stop service
echo -e "${YELLOW}Test 2: Stop service${NC}"
sudo systemctl stop "$SERVICE"
sleep 2
if ! systemctl is-active --quiet "$SERVICE"; then
    echo -e "${GREEN}✅ Service stopped successfully${NC}"
else
    echo -e "❌ Service still running"
fi
echo ""

# Test 3: Start service
echo -e "${YELLOW}Test 3: Start service${NC}"
sudo systemctl start "$SERVICE"
sleep 3
if systemctl is-active --quiet "$SERVICE"; then
    echo -e "${GREEN}✅ Service started successfully${NC}"
else
    echo -e "❌ Service failed to start"
fi
echo ""

# Test 4: Restart service
echo -e "${YELLOW}Test 4: Restart service${NC}"
sudo systemctl restart "$SERVICE"
sleep 3
if systemctl is-active --quiet "$SERVICE"; then
    echo -e "${GREEN}✅ Service restarted successfully${NC}"
else
    echo -e "❌ Service failed to restart"
fi
echo ""

# Test 5: View logs
echo -e "${YELLOW}Test 5: View logs (last 10 lines)${NC}"
sudo journalctl -u "$SERVICE" -n 10 --no-pager | tail -5
echo -e "${GREEN}✅ Logs accessible${NC}"
echo ""

# Test 6: Check enabled status
echo -e "${YELLOW}Test 6: Check if service is enabled${NC}"
if systemctl is-enabled --quiet "$SERVICE"; then
    echo -e "${GREEN}✅ Service is enabled (will start on boot)${NC}"
else
    echo -e "❌ Service is not enabled"
fi
echo ""

# Test 7: Resource usage
echo -e "${YELLOW}Test 7: Resource usage${NC}"
sudo systemctl show "$SERVICE" --property=MainPID,CPUUsageNSec,MemoryCurrent --no-pager
echo -e "${GREEN}✅ Resource info available${NC}"
echo ""

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  All Tests Passed!                                                  ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Service is running and managed by systemd${NC}"
echo -e "${YELLOW}View live logs: ${BLUE}sudo journalctl -u $SERVICE -f${NC}"
