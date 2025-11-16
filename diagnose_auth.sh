#!/bin/bash
#
# Diagnose Authentication Configuration
# Run this on 172.30.3.133 to check auth configuration
#

echo "=== Backend Authentication Diagnostic ==="
echo ""

# Find Docker container
echo "1. Finding Docker container..."
CONTAINER=$(sudo docker ps --filter "publish=5656" --format "{{.Names}}" | head -1)

if [ -z "$CONTAINER" ]; then
    echo "❌ No container found publishing port 5656"
    echo "Checking all running containers:"
    sudo docker ps
    echo ""
    echo "Please provide the container name/ID manually"
    exit 1
fi

echo "✓ Found container: $CONTAINER"
echo ""

# Check environment variables
echo "2. Checking environment variables..."
echo ""
echo "SECURITY_PROVIDER:"
sudo docker inspect $CONTAINER | grep -A 1 "SECURITY_PROVIDER" || echo "  ❌ NOT SET (will default to SQL auth)"
echo ""
echo "SECURITY_ENABLED:"
sudo docker inspect $CONTAINER | grep -A 1 "SECURITY_ENABLED" || echo "  ✓ Not set (defaults to true)"
echo ""

# Check container logs for auth provider
echo "3. Checking what auth provider is actually loaded..."
echo ""
AUTH_LINE=$(sudo docker logs $CONTAINER 2>&1 | grep "using SECURITY_PROVIDER" | tail -1)
if [ -z "$AUTH_LINE" ]; then
    echo "❌ Could not find security provider in logs"
    echo "Showing last 30 lines of logs:"
    sudo docker logs $CONTAINER 2>&1 | tail -30
else
    echo "$AUTH_LINE"
    echo ""
    if echo "$AUTH_LINE" | grep -q "COGNITO"; then
        echo "✓ Using COGNITO authentication (correct!)"
    elif echo "$AUTH_LINE" | grep -q "SQL"; then
        echo "❌ Using SQL authentication (should be Cognito)"
        echo ""
        echo "FIX: Set environment variable SECURITY_PROVIDER=cognito"
    else
        echo "⚠ Using other authentication: $(echo $AUTH_LINE | grep -o '[A-Z_]*Authentication_Provider')"
    fi
fi
echo ""

# Check if auth_provider.py has our changes
echo "4. Checking if auth_provider.py has the verify_aud: False change..."
if sudo docker exec $CONTAINER grep -q '"verify_aud": False' /app/security/authentication_provider/cognito/auth_provider.py 2>/dev/null; then
    echo "✓ auth_provider.py has been updated with verify_aud: False"
elif [ -f "/home/tyler.band/oukash5/security/authentication_provider/cognito/auth_provider.py" ]; then
    if grep -q '"verify_aud": False' /home/tyler.band/oukash5/security/authentication_provider/cognito/auth_provider.py; then
        echo "✓ auth_provider.py has been updated on host (should be mounted in container)"
    else
        echo "❌ auth_provider.py has NOT been updated yet"
        echo "   Need to update: /home/tyler.band/oukash5/security/authentication_provider/cognito/auth_provider.py"
    fi
else
    echo "⚠ Could not check file (path may be different)"
fi
echo ""

# Check Cognito configuration
echo "5. Checking Cognito configuration..."
echo ""
echo "COGNITO_USER_POOL_ID:"
sudo docker inspect $CONTAINER | grep -A 1 "COGNITO_USER_POOL_ID" || echo "  ⚠ Using default from config.py"
echo ""
echo "COGNITO_REGION:"
sudo docker inspect $CONTAINER | grep -A 1 "COGNITO_REGION" || echo "  ⚠ Using default from config.py"
echo ""

# Provide recommendations
echo ""
echo "=== RECOMMENDATIONS ==="
echo ""

# Check if SECURITY_PROVIDER is set
if ! sudo docker inspect $CONTAINER | grep -q "SECURITY_PROVIDER"; then
    echo "❌ CRITICAL: SECURITY_PROVIDER is not set!"
    echo ""
    echo "The backend is using SQL authentication (default) instead of Cognito."
    echo ""
    echo "TO FIX:"
    echo "-------"
    echo ""

    # Check for docker-compose
    if [ -f "/home/tyler.band/oukash5/docker-compose.yml" ]; then
        echo "Option A: Edit docker-compose.yml"
        echo ""
        echo "  cd /home/tyler.band/oukash5"
        echo "  nano docker-compose.yml"
        echo ""
        echo "Add under 'environment:'"
        echo "  - SECURITY_PROVIDER=cognito"
        echo ""
        echo "Then restart:"
        echo "  sudo docker-compose restart"
    else
        echo "Option B: Restart container with environment variable"
        echo ""
        echo "  # Get the full docker run command:"
        echo "  sudo docker inspect $CONTAINER --format '{{.Config.Cmd}}'"
        echo ""
        echo "  # Stop and remove current container:"
        echo "  sudo docker stop $CONTAINER"
        echo "  sudo docker rm $CONTAINER"
        echo ""
        echo "  # Re-run with -e SECURITY_PROVIDER=cognito added"
        echo "  # (You'll need the full docker run command from above)"
    fi
    echo ""
    echo "Option C: Quick test (temporary, won't persist):"
    echo ""
    echo "  Create/edit .env file:"
    echo "  echo 'SECURITY_PROVIDER=cognito' > /home/tyler.band/oukash5/.env"
    echo "  sudo docker restart $CONTAINER"
    echo ""
fi

# Check if auth_provider.py is updated
if ! grep -q '"verify_aud": False' /home/tyler.band/oukash5/security/authentication_provider/cognito/auth_provider.py 2>/dev/null; then
    echo "❌ auth_provider.py needs to be updated"
    echo ""
    echo "TO FIX:"
    echo "-------"
    echo "Transfer the modified auth_provider.py from Windows to:"
    echo "  /home/tyler.band/oukash5/security/authentication_provider/cognito/auth_provider.py"
    echo ""
    echo "Then restart the container:"
    echo "  sudo docker restart $CONTAINER"
    echo ""
fi

echo ""
echo "=== CONTAINER INFO ==="
echo "Container name: $CONTAINER"
echo "Container ID: $(sudo docker ps --filter name=$CONTAINER --format '{{.ID}}')"
echo ""
echo "To view logs:"
echo "  sudo docker logs -f $CONTAINER"
echo ""
echo "To restart:"
echo "  sudo docker restart $CONTAINER"
echo ""

# Check if docker-compose exists
if [ -f "/home/tyler.band/oukash5/docker-compose.yml" ]; then
    echo "Docker Compose file found at: /home/tyler.band/oukash5/docker-compose.yml"
    echo ""
    echo "Current environment variables in docker-compose.yml:"
    grep -A 20 "environment:" /home/tyler.band/oukash5/docker-compose.yml | head -25
fi
