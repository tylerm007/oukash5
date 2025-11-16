#!/bin/bash
#
# Script to identify how the backend is running
# Run this on 172.30.3.133 to find the deployment method
#

echo "=== Checking Backend Deployment Method ==="
echo ""

# Check for Docker containers
echo "1. Checking for Docker containers..."
if command -v docker &> /dev/null; then
    echo "Docker is installed. Checking for running containers:"
    sudo docker ps
    echo ""
    echo "All containers (including stopped):"
    sudo docker ps -a | grep -E "oukash|kashrus|api|logic|5656"
    echo ""
else
    echo "Docker not found"
fi
echo ""

# Check for processes running on port 5656
echo "2. Checking what's listening on port 5656..."
sudo lsof -i :5656 || sudo netstat -tlnp | grep 5656 || sudo ss -tlnp | grep 5656
echo ""

# Check for Python processes
echo "3. Checking for Python API processes..."
ps aux | grep -E "api_logic_server_run|python.*oukash" | grep -v grep
echo ""

# Check for systemd services
echo "4. Checking for systemd services..."
sudo systemctl list-units --type=service --all | grep -E "api|kashrus|oukash|logic" || echo "No matching systemd services found"
echo ""

# Check for docker-compose
echo "5. Checking for docker-compose..."
if [ -f "/home/tyler.band/oukash5/docker-compose.yml" ]; then
    echo "Found docker-compose.yml at /home/tyler.band/oukash5/"
    cat /home/tyler.band/oukash5/docker-compose.yml
elif [ -f "/home/tyler.band/docker-compose.yml" ]; then
    echo "Found docker-compose.yml at /home/tyler.band/"
    cat /home/tyler.band/docker-compose.yml
else
    echo "No docker-compose.yml found in common locations"
    find /home/tyler.band -name "docker-compose.yml" 2>/dev/null | head -5
fi
echo ""

# Check for Dockerfile
echo "6. Checking for Dockerfile..."
if [ -f "/home/tyler.band/oukash5/Dockerfile" ]; then
    echo "Found Dockerfile at /home/tyler.band/oukash5/"
    head -20 /home/tyler.band/oukash5/Dockerfile
else
    echo "No Dockerfile found in /home/tyler.band/oukash5/"
fi
echo ""

# Check screen sessions
echo "7. Checking for screen sessions..."
screen -ls 2>/dev/null || echo "No screen sessions or screen not installed"
echo ""

# Summary
echo "=== Summary ==="
echo "Backend path: /home/tyler.band/oukash5/"
echo ""
echo "Based on the above output, the backend is likely running via:"
if sudo docker ps 2>/dev/null | grep -q "5656"; then
    echo "  ✓ DOCKER CONTAINER"
    echo ""
    echo "To update and restart:"
    echo "  1. Update the file on the host: /home/tyler.band/oukash5/security/authentication_provider/cognito/auth_provider.py"
    echo "  2. Find the container name from 'docker ps' output above"
    echo "  3. Restart the container:"
    echo "     sudo docker restart <container-name>"
    echo "  OR if using docker-compose:"
    echo "     cd /home/tyler.band/oukash5"
    echo "     sudo docker-compose restart"
elif ps aux | grep -q "[a]pi_logic_server_run"; then
    echo "  ✓ DIRECT PYTHON PROCESS"
    echo ""
    echo "To update and restart:"
    echo "  1. Update the file: /home/tyler.band/oukash5/security/authentication_provider/cognito/auth_provider.py"
    echo "  2. Restart with: sudo systemctl restart <service-name>"
    echo "  OR manually: pkill -f api_logic_server_run && cd /home/tyler.band/oukash5 && python api_logic_server_run.py &"
else
    echo "  ? UNABLE TO DETERMINE"
    echo "  Check the output above for clues"
fi
echo ""
