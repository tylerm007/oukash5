# Backend Deployment Instructions for 172.30.3.133

## Overview
This guide explains how to deploy the modified NewAPI backend with Cognito authentication that accepts tokens from any app client in the same User Pool.

## What Was Changed
Modified `security/authentication_provider/cognito/auth_provider.py` to skip audience validation:
- Changed `"verify_aud": False` to accept tokens from any Cognito app client
- Removed hardcoded audience check for single Client ID
- Still validates issuer to ensure tokens come from correct User Pool (us-east-1_d38hiE2QM)

## Prerequisites
- SSH access to 172.30.3.133
- Python 3.8+ installed on the server
- Virtual environment with required packages

## Deployment Steps

### Step 1: Transfer Modified File to Server

From your Windows machine with WinSCP or command line:

**Option A: Using WinSCP (GUI)**
1. Open WinSCP and connect to 172.30.3.133
2. Navigate to the NewAPI directory on the server (find where it's installed)
3. Navigate to `security/authentication_provider/cognito/`
4. Upload the modified `auth_provider.py` file
5. Overwrite the existing file when prompted

**Option B: Using SCP (Command Line)**
```bash
# From Windows (PowerShell or Command Prompt)
scp "d:\NewAPI\security\authentication_provider\cognito\auth_provider.py" your-username@172.30.3.133:/path/to/NewAPI/security/authentication_provider/cognito/auth_provider.py
```

**Option C: Using SSH and Text Editor**
```bash
# SSH into the server
ssh your-username@172.30.3.133

# Navigate to the backend directory
cd /path/to/NewAPI/security/authentication_provider/cognito/

# Backup the original file
sudo cp auth_provider.py auth_provider.py.backup

# Edit the file directly on the server
sudo nano auth_provider.py

# Find the jwt.decode() section (around line 952-966)
# Make the changes as shown in auth_provider.py
# Save and exit (Ctrl+X, Y, Enter)
```

### Step 2: Verify the Backend Directory

Find where NewAPI is installed on the server:
```bash
ssh your-username@172.30.3.133

# Common locations to check:
ls /var/www/
ls /opt/
ls /home/your-username/
ls /srv/

# Or search for it
find / -name "api_logic_server_run.py" 2>/dev/null
```

### Step 3: Check Python Virtual Environment

```bash
cd /path/to/NewAPI

# Check if virtual environment exists
ls -la venv/  # or .venv/

# If venv exists, activate it:
source venv/bin/activate  # or source .venv/bin/activate

# Verify Python version
python --version  # Should be 3.8+

# Verify required packages are installed
pip list | grep -E "(Flask|PyJWT|cryptography|requests)"
```

### Step 4: Restart the Backend Service

**Option A: If running as systemd service**
```bash
# Find the service name
sudo systemctl list-units --type=service | grep -i api
# or
sudo systemctl list-units --type=service | grep -i kashrus
# or
sudo systemctl list-units --type=service | grep -i logic

# Restart the service (replace 'service-name' with actual name)
sudo systemctl restart service-name
sudo systemctl status service-name

# View logs if needed
sudo journalctl -u service-name -f
```

**Option B: If running in screen/tmux session**
```bash
# List screen sessions
screen -ls

# Attach to the session
screen -r session-name

# Stop the server (Ctrl+C)
# Restart it
python api_logic_server_run.py

# Detach from screen (Ctrl+A, then D)
```

**Option C: If running directly (for testing)**
```bash
cd /path/to/NewAPI

# Activate virtual environment
source venv/bin/activate

# Stop any existing process
pkill -f api_logic_server_run.py

# Start the server
python api_logic_server_run.py

# Or run in background with nohup
nohup python api_logic_server_run.py > backend.log 2>&1 &

# Or run in screen session
screen -S kashrus-api
python api_logic_server_run.py
# Press Ctrl+A, then D to detach
```

### Step 5: Verify Backend is Running

```bash
# Check if process is running
ps aux | grep api_logic_server_run.py

# Check if port 5656 is listening
sudo netstat -tlnp | grep 5656
# or
sudo ss -tlnp | grep 5656

# Test the API locally (should return 401 or 422 for no auth, not 500)
curl http://localhost:5656/api/
```

### Step 6: Test from the Frontend Server

From 172.30.3.147:
```bash
# Test connectivity to backend
curl http://172.30.3.133:5656/api/

# Should return JSON response, not timeout or connection refused
```

### Step 7: Test the Complete Authentication Flow

1. Open browser and navigate to: `https://172.30.3.147`
2. Click "Sign In" - should redirect to Cognito login
3. Login with your credentials
4. Should redirect back to the application
5. Click "Companies" or another entity
6. Should successfully load data (no more 422 errors)

**Check browser console for any errors:**
- Press F12 to open Developer Tools
- Go to Console tab
- Look for any red error messages
- Go to Network tab and check API calls to `/api/` endpoints

## Troubleshooting

### Backend Not Starting

**Check Python environment:**
```bash
cd /path/to/NewAPI
source venv/bin/activate
python api_logic_server_run.py
# Look for error messages
```

**Check for missing dependencies:**
```bash
pip install -r requirements.txt  # if requirements.txt exists
```

**Check file permissions:**
```bash
ls -la security/authentication_provider/cognito/auth_provider.py
# Should be readable by the user running the service
```

### Still Getting 422 Errors

**Check backend logs:**
```bash
# If systemd service:
sudo journalctl -u service-name -n 100

# If running directly:
tail -f backend.log

# Look for JWT validation errors
```

**Verify the file was actually updated:**
```bash
cd /path/to/NewAPI/security/authentication_provider/cognito/
grep "verify_aud.*False" auth_provider.py
# Should show the line with verify_aud: False
```

### Backend Running But Not Accessible

**Check firewall rules:**
```bash
# Check if firewalld is running
sudo systemctl status firewalld

# If running, ensure port 5656 is open
sudo firewall-cmd --list-all
sudo firewall-cmd --add-port=5656/tcp --permanent
sudo firewall-cmd --reload
```

**Check security group settings:**
- In AWS Console, verify the security group allows traffic on port 5656
- The rule should allow traffic from 172.30.3.147 (frontend server)

### Authentication Errors in Browser

**Check network requests in browser:**
- F12 → Network tab
- Look for `/api/` requests
- Check the request headers (should have Authorization: Bearer ...)
- Check the response (look for specific error message)

**Check if token is being sent:**
- F12 → Console tab
- Type: `sessionStorage.getItem('cognito_access_token')`
- Should show a JWT token (long string)

**Check token format:**
- Copy the token from sessionStorage
- Go to https://jwt.io and paste the token
- Verify:
  - Header shows "RS256" algorithm
  - Payload shows iss: https://cognito-idp.us-east-1.amazonaws.com/us-east-1_d38hiE2QM
  - Payload has email, sub, and other claims

## Rollback (If Needed)

If you need to revert the changes:

```bash
cd /path/to/NewAPI/security/authentication_provider/cognito/
sudo cp auth_provider.py.backup auth_provider.py
sudo systemctl restart service-name  # or restart manually
```

## Security Notes

- **Issuer validation is still active** - Tokens must come from the correct Cognito User Pool
- **Signature validation is still active** - Tokens must be properly signed by Cognito
- **Expiration validation is still active** - Expired tokens are rejected
- Only the audience (client ID) validation is skipped
- This allows multiple frontend apps with different Client IDs to use the same backend
- All apps must still authenticate through the same User Pool (us-east-1_d38hiE2QM)

## Next Steps After Deployment

1. Test with the current frontend app (Client ID: 3iec660aiv2evjdtn062s0ap22)
2. Test with the testAPI frontend app (Client ID: 6o1m2bjh8bc8iihtufmhpq79gq)
3. Both should work with the same backend
4. Monitor backend logs for any issues
5. Consider adding the logout button to all pages

## Common Commands Reference

```bash
# Find backend process
ps aux | grep api_logic_server

# Stop backend
pkill -f api_logic_server_run.py

# Start backend in screen
screen -S kashrus-api
cd /path/to/NewAPI
source venv/bin/activate
python api_logic_server_run.py
# Ctrl+A, D to detach

# Reattach to screen
screen -r kashrus-api

# View backend logs in real-time
tail -f /path/to/NewAPI/backend.log

# Check what's listening on port 5656
sudo lsof -i :5656
```
