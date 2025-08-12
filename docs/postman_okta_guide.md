# POSTMAN + OKTA Authentication Guide

This guide shows you how to authenticate with OKTA and use the access token in POSTMAN for API calls.

## Quick Setup (Recommended)

### Method 1: Using the POSTMAN Collection

1. **Import the Collection**
   - In POSTMAN, click "Import"
   - Select `postman/OKTA_API_Logic_Server.postman_collection.json`
   - The collection includes automated token handling

2. **Start Authentication Flow**
   - Run the request: **"1. Get Auth URL"**
   - Copy the `auth_url` from the response
   - Open the URL in your web browser
   - Complete OKTA login

3. **Get Your Token**
   - After login, browser shows JSON with `access_token`
   - Run the request: **"2. Set Token from Session"**
   - Token is automatically saved to collection variables

4. **Test API Calls**
   - Run **"Test API - Company List"** 
   - All subsequent requests will use the token automatically

## Manual Setup

### Method 2: Browser + Manual Token Copy

1. **Start the API Logic Server**
   ```bash
   python api_logic_server_run.py
   ```

2. **Get Authentication URL**
   - GET `http://localhost:5656/auth/login-postman`
   - Copy the `auth_url` from response
   - Open URL in browser and login to OKTA

3. **Extract Token from Browser Response**
   After login, you'll see JSON like:
   ```json
   {
     "success": true,
     "access_token": "eyJhbGci...",
     "token_type": "Bearer",
     "user_info": {...}
   }
   ```

4. **Configure POSTMAN**
   - Open POSTMAN collection settings
   - Go to "Authorization" tab
   - Select "Bearer Token"
   - Paste the `access_token` value

### Method 3: Session-Based Token Retrieval

1. **Login via Browser**
   - Open `http://localhost:5656/auth/login`
   - Complete OKTA authentication
   - You'll be redirected to the app

2. **Get Session Token**
   - GET `http://localhost:5656/auth/token`
   - Copy the `access_token` from response
   - Use in POSTMAN Authorization

## POSTMAN Configuration

### Collection-Level Authorization (Recommended)
1. Right-click collection → "Edit"
2. Go to "Authorization" tab
3. Type: "Bearer Token"
4. Token: `{{access_token}}` (uses collection variable)

### Request-Level Authorization
1. Open individual request
2. "Authorization" tab
3. Type: "Bearer Token" 
4. Token: Paste your access token

## Environment Variables

Set these in POSTMAN environment or collection variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `base_url` | `http://localhost:5656` | API base URL |
| `access_token` | `eyJhbGci...` | OKTA access token |
| `user_id` | `user@example.com` | Current user ID |

## API Testing Examples

### Test Authentication
```
GET {{base_url}}/auth/user
Authorization: Bearer {{access_token}}
```

### Test Data Access
```
GET {{base_url}}/api/COMPANYTB
Authorization: Bearer {{access_token}}
```

### Test Specific Record
```
GET {{base_url}}/api/COMPANYTB/1
Authorization: Bearer {{access_token}}
```

## Troubleshooting

### 401 Unauthorized
- Token missing or expired
- Run authentication flow again
- Check Authorization header format: `Bearer your_token_here`

### 422 Signature Verification Failed
- Token format invalid
- Get fresh token from OKTA
- Ensure token starts with `eyJ`

### Token Expired
- OKTA tokens typically last 1 hour
- Re-run authentication flow
- Check token expiration in JWT payload

## Advanced: Automated Token Refresh

For automated testing, you can use POSTMAN's pre-request scripts:

```javascript
// Pre-request Script
const token = pm.collectionVariables.get('access_token');
const expiry = pm.collectionVariables.get('token_expiry');
const now = new Date().getTime();

if (!token || (expiry && now > expiry)) {
    // Token expired, get new one
    pm.sendRequest({
        url: pm.variables.get('base_url') + '/auth/token',
        method: 'GET'
    }, function (err, res) {
        if (!err && res.code === 200) {
            const response = res.json();
            pm.collectionVariables.set('access_token', response.access_token);
            
            // Set expiry 1 hour from now
            const newExpiry = new Date();
            newExpiry.setHours(newExpiry.getHours() + 1);
            pm.collectionVariables.set('token_expiry', newExpiry.getTime());
        }
    });
}
```

## Security Notes

1. **Don't share tokens** - They provide full access to your account
2. **Tokens expire** - Usually after 1 hour, get fresh ones
3. **Use HTTPS in production** - Never send tokens over HTTP
4. **Log out when done** - Visit `/auth/logout` to end session

## API Endpoints Summary

| Endpoint | Purpose | Method |
|----------|---------|--------|
| `/auth/login-postman` | Get auth URL for POSTMAN | GET |
| `/auth/postman-callback` | POSTMAN callback (returns JSON) | GET |
| `/auth/token` | Get token from session | GET |
| `/auth/user` | Check auth status | GET |
| `/auth/logout` | Logout | GET |
| `/api/*` | Protected API endpoints | GET/POST/etc |

Now you can authenticate with OKTA and use the access token for all your API calls in POSTMAN! 🚀
