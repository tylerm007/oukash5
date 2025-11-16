#!/bin/bash
#
# Quick Deployment Script for NewAPI Backend
# This script helps deploy the modified auth_provider.py to the backend server
#
# Usage: ./deploy_backend.sh [backend-path]
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_PATH="${1:-/opt/NewAPI}"  # Default path, can be overridden
SERVICE_NAME="${2:-kashrus-api}"  # Default service name, can be overridden

echo -e "${GREEN}=== NewAPI Backend Deployment Script ===${NC}"
echo -e "Backend Path: ${YELLOW}$BACKEND_PATH${NC}"
echo -e "Service Name: ${YELLOW}$SERVICE_NAME${NC}"
echo ""

# Check if running on the backend server
if [ ! -f "/etc/hostname" ] || ! grep -q "172.30.3.133" /etc/hosts 2>/dev/null; then
    echo -e "${YELLOW}Warning: This script should be run on the backend server (172.30.3.133)${NC}"
    echo -e "${YELLOW}If you're on a different machine, use WinSCP or SCP to transfer the file${NC}"
    echo ""
fi

# Step 1: Check if backend directory exists
echo -e "${BLUE}Step 1: Checking backend directory...${NC}"
if [ ! -d "$BACKEND_PATH" ]; then
    echo -e "${RED}Error: Backend directory not found at $BACKEND_PATH${NC}"
    echo -e "${YELLOW}Common locations to check:${NC}"
    echo -e "  - /opt/NewAPI"
    echo -e "  - /var/www/NewAPI"
    echo -e "  - /home/\$USER/NewAPI"
    echo -e "  - /srv/NewAPI"
    echo ""
    echo -e "${YELLOW}Searching for api_logic_server_run.py...${NC}"
    find / -name "api_logic_server_run.py" 2>/dev/null | head -5
    exit 1
fi
echo -e "${GREEN}✓ Backend directory found${NC}"
echo ""

# Step 2: Backup original file
echo -e "${BLUE}Step 2: Backing up original auth_provider.py...${NC}"
AUTH_FILE="$BACKEND_PATH/security/authentication_provider/cognito/auth_provider.py"
if [ ! -f "$AUTH_FILE" ]; then
    echo -e "${RED}Error: auth_provider.py not found at $AUTH_FILE${NC}"
    exit 1
fi

BACKUP_FILE="$AUTH_FILE.backup.$(date +%Y%m%d_%H%M%S)"
cp "$AUTH_FILE" "$BACKUP_FILE"
echo -e "${GREEN}✓ Backup created at $BACKUP_FILE${NC}"
echo ""

# Step 3: Check if file needs updating
echo -e "${BLUE}Step 3: Checking if file needs updating...${NC}"
if grep -q '"verify_aud": False' "$AUTH_FILE"; then
    echo -e "${GREEN}✓ File already has the correct modification${NC}"
    echo -e "${YELLOW}Skipping update step${NC}"
else
    echo -e "${YELLOW}File needs to be updated${NC}"
    echo -e "${RED}Please update the file manually or use SCP to transfer it${NC}"
    echo -e "${YELLOW}The modification should change line ~960 from:${NC}"
    echo -e '    "verify_aud": True,'
    echo -e "${YELLOW}to:${NC}"
    echo -e '    "verify_aud": False,  # Skip audience check'
    echo ""
    echo -e "${YELLOW}You can edit it now with:${NC}"
    echo -e "    sudo nano $AUTH_FILE"
    exit 1
fi
echo ""

# Step 4: Check Python environment
echo -e "${BLUE}Step 4: Checking Python environment...${NC}"
cd "$BACKEND_PATH"

if [ -d "venv" ]; then
    VENV_PATH="venv"
elif [ -d ".venv" ]; then
    VENV_PATH=".venv"
else
    echo -e "${YELLOW}Warning: No virtual environment found${NC}"
    VENV_PATH=""
fi

if [ -n "$VENV_PATH" ]; then
    echo -e "${GREEN}✓ Virtual environment found at $VENV_PATH${NC}"
    source "$VENV_PATH/bin/activate"
    echo -e "Python version: $(python --version)"
else
    echo -e "${YELLOW}Using system Python: $(python3 --version)${NC}"
fi
echo ""

# Step 5: Verify required packages
echo -e "${BLUE}Step 5: Verifying required packages...${NC}"
PYTHON_CMD="python"
if [ -z "$VENV_PATH" ]; then
    PYTHON_CMD="python3"
fi

$PYTHON_CMD -c "import jwt; import cryptography; import flask" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Required packages are installed${NC}"
else
    echo -e "${RED}Warning: Some required packages may be missing${NC}"
    echo -e "${YELLOW}Run: pip install PyJWT cryptography flask${NC}"
fi
echo ""

# Step 6: Check if service is running
echo -e "${BLUE}Step 6: Checking if backend service is running...${NC}"
if systemctl list-units --type=service --all | grep -q "$SERVICE_NAME"; then
    echo -e "${GREEN}✓ Found systemd service: $SERVICE_NAME${NC}"
    USE_SYSTEMD=true
elif pgrep -f "api_logic_server_run.py" > /dev/null; then
    echo -e "${YELLOW}Backend is running as a process (not systemd service)${NC}"
    USE_SYSTEMD=false
else
    echo -e "${YELLOW}Backend does not appear to be running${NC}"
    USE_SYSTEMD=false
fi
echo ""

# Step 7: Restart the backend
echo -e "${BLUE}Step 7: Restarting backend...${NC}"
if [ "$USE_SYSTEMD" = true ]; then
    echo -e "${YELLOW}Restarting systemd service...${NC}"
    sudo systemctl restart "$SERVICE_NAME"
    sleep 2
    sudo systemctl status "$SERVICE_NAME" --no-pager
    echo ""
    echo -e "${GREEN}✓ Service restarted${NC}"
else
    echo -e "${YELLOW}Manual restart required${NC}"
    echo -e "To restart manually:"
    echo -e "  1. Stop: pkill -f api_logic_server_run.py"
    echo -e "  2. Start in screen:"
    echo -e "     screen -S kashrus-api"
    echo -e "     cd $BACKEND_PATH"
    if [ -n "$VENV_PATH" ]; then
        echo -e "     source $VENV_PATH/bin/activate"
    fi
    echo -e "     python api_logic_server_run.py"
    echo -e "     # Press Ctrl+A, D to detach"
    echo ""

    # Offer to restart now
    read -p "Would you like to restart now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pkill -f api_logic_server_run.py
        sleep 1
        if [ -n "$VENV_PATH" ]; then
            source "$VENV_PATH/bin/activate"
        fi
        nohup python api_logic_server_run.py > backend.log 2>&1 &
        echo -e "${GREEN}✓ Backend started in background${NC}"
        echo -e "${YELLOW}Logs: tail -f $BACKEND_PATH/backend.log${NC}"
    fi
fi
echo ""

# Step 8: Verify backend is running
echo -e "${BLUE}Step 8: Verifying backend is responding...${NC}"
sleep 2
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5656/api/ | grep -q "401\|422\|200"; then
    echo -e "${GREEN}✓ Backend is responding on port 5656${NC}"
else
    echo -e "${RED}Warning: Backend may not be responding correctly${NC}"
    echo -e "${YELLOW}Check logs with: tail -f $BACKEND_PATH/backend.log${NC}"
fi
echo ""

# Step 9: Test from frontend server
echo -e "${BLUE}Step 9: Testing connectivity from frontend server...${NC}"
echo -e "${YELLOW}From 172.30.3.147, run:${NC}"
echo -e "    curl http://172.30.3.133:5656/api/"
echo ""

# Final summary
echo -e "${GREEN}=== Deployment Complete! ===${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo -e "  1. Test from browser: ${BLUE}https://172.30.3.147${NC}"
echo -e "  2. Login with Cognito credentials"
echo -e "  3. Navigate to Companies or other entities"
echo -e "  4. Should load data successfully (no 422 errors)"
echo ""
echo -e "${YELLOW}Backup Location:${NC}"
echo -e "  Original file backed up to: ${BLUE}$BACKUP_FILE${NC}"
echo ""
echo -e "${YELLOW}Rollback (if needed):${NC}"
echo -e "  sudo cp $BACKUP_FILE $AUTH_FILE"
if [ "$USE_SYSTEMD" = true ]; then
    echo -e "  sudo systemctl restart $SERVICE_NAME"
else
    echo -e "  pkill -f api_logic_server_run.py && cd $BACKEND_PATH && python api_logic_server_run.py &"
fi
echo ""
