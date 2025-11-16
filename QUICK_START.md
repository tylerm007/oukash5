# Quick Start: Deploy Backend with Multi-Client Support

## What Changed?

Modified the backend to accept Cognito tokens from **any app client** in the same User Pool, not just one hardcoded Client ID.

**File Modified:** `security/authentication_provider/cognito/auth_provider.py`
**Change:** Line 961 changed from `"verify_aud": True` to `"verify_aud": False`

## Security Impact

✅ **Still validates:**
- Token signature (RS256 via Cognito JWKS)
- Token expiration
- Issuer (must be from User Pool: us-east-1_d38hiE2QM)
- Token format and claims

❌ **No longer validates:**
- Audience (client_id) - allows multiple frontend apps

This is **secure** because all tokens must still come from the same Cognito User Pool.

## Quick Deployment Steps

### Option 1: Using WinSCP (Easiest)

1. Open WinSCP and connect to **172.30.3.133**
2. Find the NewAPI directory (common locations: `/opt/NewAPI`, `/var/www/NewAPI`, `/home/username/NewAPI`)
3. Navigate to: `security/authentication_provider/cognito/`
4. Upload the modified `auth_provider.py` from `d:\NewAPI\security\authentication_provider\cognito\auth_provider.py`
5. Restart the backend:
   ```bash
   ssh your-username@172.30.3.133
   sudo systemctl restart kashrus-api  # or your service name
   ```

### Option 2: Using SCP (Command Line)

From Windows PowerShell:
```powershell
# Transfer the file
scp "d:\NewAPI\security\authentication_provider\cognito\auth_provider.py" your-username@172.30.3.133:/path/to/NewAPI/security/authentication_provider/cognito/auth_provider.py

# SSH in and restart
ssh your-username@172.30.3.133
sudo systemctl restart kashrus-api
```

### Option 3: Using Deployment Script

1. Transfer `deploy_backend.sh` to the server:
   ```powershell
   scp "d:\NewAPI\deploy_backend.sh" your-username@172.30.3.133:/tmp/
   ```

2. SSH in and run the script:
   ```bash
   ssh your-username@172.30.3.133
   chmod +x /tmp/deploy_backend.sh
   sudo /tmp/deploy_backend.sh /path/to/NewAPI
   ```

## Testing

### 1. Test Backend is Running

From 172.30.3.133:
```bash
# Check process
ps aux | grep api_logic_server_run.py

# Check port
sudo netstat -tlnp | grep 5656

# Test locally
curl http://localhost:5656/api/
# Should return JSON, not timeout
```

### 2. Test from Frontend Server

From 172.30.3.147:
```bash
curl http://172.30.3.133:5656/api/
# Should return JSON (401 or 422 is OK, just not timeout)
```

### 3. Test Complete Flow

1. Open browser: **https://172.30.3.147**
2. Click "Sign In"
3. Login with Cognito credentials
4. Click "Companies" or another entity
5. **Should load data successfully!** (no more 422 errors)

## Troubleshooting

### Still Getting 422 Errors?

Check backend logs:
```bash
# If systemd service:
sudo journalctl -u kashrus-api -f

# If running manually:
tail -f /path/to/NewAPI/backend.log
```

Verify the file was updated:
```bash
grep "verify_aud.*False" /path/to/NewAPI/security/authentication_provider/cognito/auth_provider.py
```

### Backend Not Reachable?

Check security group allows port 5656 from 172.30.3.147:
```bash
# On the backend server
sudo iptables -L -n | grep 5656
```

Check backend is listening:
```bash
sudo lsof -i :5656
```

### Backend Won't Start?

Check Python dependencies:
```bash
cd /path/to/NewAPI
source venv/bin/activate  # if using venv
pip list | grep -E "(PyJWT|cryptography|flask)"
```

Check for errors:
```bash
cd /path/to/NewAPI
source venv/bin/activate
python api_logic_server_run.py
# Look for error messages
```

## Rollback

If you need to revert:

```bash
ssh your-username@172.30.3.133
cd /path/to/NewAPI/security/authentication_provider/cognito/
sudo cp auth_provider.py.backup auth_provider.py
sudo systemctl restart kashrus-api
```

## Success Indicators

✅ No 422 errors in browser console
✅ Companies page loads data
✅ No "alg value is not allowed" errors
✅ Backend logs show "Successfully validated Cognito token"

## What This Enables

Now you can have **multiple frontend apps** using the **same backend API**:
- **Kashrus App** (172.30.3.147) - Client ID: 3iec660aiv2evjdtn062s0ap22
- **testAPI App** - Client ID: 6o1m2bjh8bc8iihtufmhpq79gq
- **Future Apps** - Any new Client ID in the same User Pool

All apps authenticate through the same Cognito User Pool (us-east-1_d38hiE2QM) but can have different login experiences, branding, and callback URLs.

## Files Reference

- **DEPLOYMENT.md** - Detailed deployment guide with all scenarios
- **deploy_backend.sh** - Automated deployment script
- **QUICK_START.md** - This file (quick reference)
- **auth_provider.py** - The modified file (in `d:\NewAPI\security\authentication_provider\cognito/`)

## Support

For detailed instructions, see **DEPLOYMENT.md**.

For automated deployment, use **deploy_backend.sh**.
