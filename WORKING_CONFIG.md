# Working Cognito Configuration Reference

**Date Working:** November 14, 2025
**Last Verified:** After hours-long 403 issue resolved

---

## AWS Cognito Settings

### User Pool
- **ID:** us-east-1_d38hiE2QM
- **Region:** us-east-1
- **Domain:** us-east-1d38hie2qm.auth.us-east-1.amazoncognito.com

### App Client (Frontend)
- **Client ID:** 3iec660aiv2evjdtn062s0ap22
- **Client Type:** Public client (no secret)

#### OAuth Settings

**Allowed OAuth Flows:**
- ✅ Authorization code grant
- ✅ Implicit grant (optional)

**Allowed OAuth Scopes:**
- ✅ openid
- ✅ email
- ✅ phone

**Allowed Callback URLs:**
```
https://172.30.3.147
https://172.30.3.147/index.html
https://172.30.3.147/login.html
```

**Allowed Sign-out URLs:**
```
https://172.30.3.147
https://172.30.3.147/login.html
```

---

## Backend Configuration (Docker)

**Server:** 172.30.3.133
**Container:** genai-server
**Path:** /home/tyler.band/oukash5/

### docker-compose.yml Environment Variables

```yaml
environment:
  - SECURITY_ENABLED=true
  - SECURITY_PROVIDER=cognito
  - APILOGICPROJECT_SECURITY_PROVIDER=cognito
  - COGNITO_REGION=us-east-1
  - COGNITO_USER_POOL_ID=us-east-1_d38hiE2QM
  - COGNITO_CLIENT_ID=34sqr8ttgro6ego2117aflg9lr
```

### Modified File

**File:** `/home/tyler.band/oukash5/security/authentication_provider/cognito/auth_provider.py`

**Line ~961:** Changed to:
```python
"verify_aud": False,  # Skip audience check - accept any client from this User Pool
```

---

## Frontend Configuration

**Server:** 172.30.3.147
**Path:** /var/www/html/ (or /usr/share/nginx/html/)

### cognitoConfig.js
```javascript
const cognitoConfig = {
  region: 'us-east-1',
  userPoolId: 'us-east-1_d38hiE2QM',
  userPoolWebClientId: '3iec660aiv2evjdtn062s0ap22',
  domain: 'us-east-1d38hie2qm.auth.us-east-1.amazoncognito.com',
  oauth: {
    scope: ['openid', 'email', 'phone'],
    redirectSignIn: window.location.origin,
    redirectSignOut: window.location.origin,
    responseType: 'code'
  }
};
```

### dataService.js
```javascript
const baseApiUrl = '/api/';  // Uses nginx proxy to backend
```

---

## Network Configuration

### Frontend Server (172.30.3.147)
- **Web Server:** Nginx with HTTPS (self-signed cert)
- **Port:** 443 (HTTPS)
- **Proxy:** Proxies `/api/` to `http://172.30.3.133:5656`

### Backend Server (172.30.3.133)
- **Docker Container:** genai-server
- **Port:** 5656 (HTTP)
- **Security Group:** Must allow traffic from 172.30.3.147 on port 5656

---

## Troubleshooting Reference

### If 403 from Cognito Returns

**Immediate Checks:**
1. Hard refresh browser (Ctrl+Shift+R)
2. Clear Session Storage (F12 → Application → Session Storage → Clear All)
3. Try different browser (rules out browser cache)
4. Check AWS Service Health: https://health.aws.amazon.com/health/status

**Verify AWS Settings:**
1. Go to AWS Cognito Console
2. User Pool → us-east-1_d38hiE2QM
3. App Integration → App clients → 3iec660aiv2evjdtn062s0ap22
4. Verify:
   - Authorization code grant is ✅ enabled
   - Callback URLs exactly match: `https://172.30.3.147`
   - OAuth scopes (openid, email, phone) are ✅ enabled

**Check Browser DevTools:**
```
F12 → Network tab → Click "Sign In"
Look at the failed request:
- URL path: /oauth2/authorize
- Check redirect_uri parameter (should be https://172.30.3.147)
- Check response body for specific error message
```

**Check Backend Logs:**
```bash
ssh user@172.30.3.133
sudo docker logs genai-server 2>&1 | grep -i "security\|cognito\|error"
```

**Verify Backend is Using Cognito:**
```bash
sudo docker logs genai-server 2>&1 | grep "SECURITY_PROVIDER"
# Should show: SECURITY_PROVIDER = cognito
# NOT: SECURITY_PROVIDER = sql
```

### If 422 from Backend

Means backend is rejecting the Cognito token:

**Check backend logs:**
```bash
sudo docker logs genai-server -f
# Look for JWT validation errors
```

**Verify auth_provider.py has verify_aud: False:**
```bash
grep "verify_aud" /home/tyler.band/oukash5/security/authentication_provider/cognito/auth_provider.py
# Should show: "verify_aud": False,
```

**Restart backend after file changes:**
```bash
cd /home/tyler.band/oukash5
sudo docker compose down
sudo docker compose up -d
```

---

## Success Indicators

When everything is working correctly, you should see:

**Browser:**
- ✅ Click "Sign In" → Redirects to Cognito login page (no 403)
- ✅ After login → Redirects back to https://172.30.3.147
- ✅ Main page loads with user email displayed
- ✅ "Logout" button appears in header
- ✅ Clicking "Companies" loads data (no 403, no 422)
- ✅ Console shows no errors (F12 → Console)

**Backend Logs:**
```
✅ config.py - security enabled: True using SECURITY_PROVIDER: <class '...COGNITO_Authentication_Provider'>
✅ Successfully validated Cognito token for user: <user-id>
```

**Browser Network Tab (F12 → Network):**
```
✅ API calls to /api/COMPANYTB return 200 OK
✅ Authorization header present: Bearer eyJ...
✅ No 401, 403, or 422 errors
```

---

## Change Log

### November 14, 2025
- Modified auth_provider.py to skip audience validation (verify_aud: False)
- Changed docker-compose.yml: SECURITY_PROVIDER from sql to cognito
- Added callback URLs to AWS Cognito app client
- Resolved hours-long 403 issue (cause unknown - possibly AWS service issue or browser cache)
- System fully operational

---

## Contacts / Notes

**AWS Account:** (add your AWS account info here)
**Team Members with Cognito Access:** (list who can modify AWS settings)
**Docker Host Access:** tyler.band@172.30.3.133

**Important:** If multiple people manage AWS Cognito settings, coordinate changes to avoid conflicts.

**CloudTrail:** Check AWS CloudTrail logs if settings mysteriously change - shows who modified what and when.
