#!/bin/bash
# MIRAI Systemd Service Installation Script
# Installs and configures MIRAI as a system service

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVICE_NAME="mirai"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
SOURCE_SERVICE="$(dirname "$0")/mirai.service"
HEALTHCHECK="/root/mirai/scripts/healthcheck.sh"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  MIRAI Systemd Service Installation                                 ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ This script must be run as root${NC}"
    echo -e "${YELLOW}   Please run: sudo $0${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Pre-installation checks...${NC}"

# Check if service file exists
if [ ! -f "$SOURCE_SERVICE" ]; then
    echo -e "${RED}❌ Service file not found: $SOURCE_SERVICE${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Service file found${NC}"

# Check if healthcheck exists
if [ ! -f "$HEALTHCHECK" ]; then
    echo -e "${RED}❌ Health check script not found: $HEALTHCHECK${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Health check script found${NC}"

# Make healthcheck executable
chmod +x "$HEALTHCHECK"
echo -e "${GREEN}✅ Health check script is executable${NC}"

# Run health check
echo -e "\n${YELLOW}🏥 Running health check...${NC}"
if "$HEALTHCHECK" --quiet; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${RED}❌ Health check failed${NC}"
    echo -e "${YELLOW}   Run: $HEALTHCHECK --verbose${NC}"
    echo -e "${YELLOW}   Do you want to continue anyway? (y/N)${NC}"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Stop existing service if running
echo -e "\n${YELLOW}🛑 Stopping existing service (if running)...${NC}"
if systemctl is-active --quiet "$SERVICE_NAME"; then
    systemctl stop "$SERVICE_NAME"
    echo -e "${GREEN}✅ Service stopped${NC}"
else
    echo -e "${BLUE}ℹ️  Service not running${NC}"
fi

# Copy service file
echo -e "\n${YELLOW}📄 Installing service file...${NC}"
cp "$SOURCE_SERVICE" "$SERVICE_FILE"
echo -e "${GREEN}✅ Service file installed: $SERVICE_FILE${NC}"

# Set permissions
chmod 644 "$SERVICE_FILE"
echo -e "${GREEN}✅ Permissions set${NC}"

# Reload systemd
echo -e "\n${YELLOW}🔄 Reloading systemd daemon...${NC}"
systemctl daemon-reload
echo -e "${GREEN}✅ Systemd daemon reloaded${NC}"

# Enable service
echo -e "\n${YELLOW}⚙️  Enabling service...${NC}"
systemctl enable "$SERVICE_NAME"
echo -e "${GREEN}✅ Service enabled (will start on boot)${NC}"

# Service status
echo -e "\n${BLUE}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Installation Complete!                                             ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Service installed successfully!${NC}"
echo ""
echo -e "${YELLOW}📝 Available commands:${NC}"
echo -e "   ${BLUE}Start service:${NC}     sudo systemctl start $SERVICE_NAME"
echo -e "   ${BLUE}Stop service:${NC}      sudo systemctl stop $SERVICE_NAME"
echo -e "   ${BLUE}Restart service:${NC}   sudo systemctl restart $SERVICE_NAME"
echo -e "   ${BLUE}Service status:${NC}    sudo systemctl status $SERVICE_NAME"
echo -e "   ${BLUE}View logs:${NC}         sudo journalctl -u $SERVICE_NAME -f"
echo -e "   ${BLUE}Recent logs:${NC}       sudo journalctl -u $SERVICE_NAME -n 50"
echo -e "   ${BLUE}Disable service:${NC}   sudo systemctl disable $SERVICE_NAME"
echo ""
echo -e "${YELLOW}❓ Do you want to start the service now? (Y/n)${NC}"
read -r response

if [[ "$response" =~ ^[Nn]$ ]]; then
    echo -e "${BLUE}ℹ️  Service not started. Start it manually when ready.${NC}"
else
    echo -e "\n${YELLOW}🚀 Starting service...${NC}"
    systemctl start "$SERVICE_NAME"
    sleep 2
    
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        echo -e "${GREEN}✅ Service started successfully!${NC}"
        echo ""
        echo -e "${YELLOW}📊 Service status:${NC}"
        systemctl status "$SERVICE_NAME" --no-pager || true
    else
        echo -e "${RED}❌ Service failed to start${NC}"
        echo -e "${YELLOW}   Check logs: sudo journalctl -u $SERVICE_NAME -n 50${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}🎉 MIRAI is now running as a system service!${NC}"
