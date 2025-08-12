# POSTMAN Token Setup Guide

## Quick Start

1. **Get Auth URL**:
   ```
   GET http://localhost:5656/auth/login-postman
   ```

2. **Login via Browser**:
   - Copy the `auth_url` from response
   - Complete OKTA login in browser
   - Copy the `access_token` from the JSON response

3. **Set in POSTMAN**:
   - Collection → Authorization → Bearer Token
   - Paste the `access_token`

## Automated Setup (Recommended)

### Method 1: Collection Variables
1. Import `OKTA_API_Logic_Server.postman_collection.json`
2. Run "1. Get Auth URL" request
3. Follow auth flow - token auto-saved to `{{access_token}}`
4. Collection uses `{{access_token}}` automatically

### Method 2: Environment Setup
1. Create Environment: "OKTA Local"
2. Add variables:
   ```
   access_token = [leave empty initially]
   base_url = http://localhost:5656
   ```
3. Collection Authorization: Bearer Token = `{{access_token}}`

### Method 3: Pre-request Script (Fully Automated)
Add to Collection Pre-request Script:

```javascript
const token = pm.collectionVariables.get("access_token");
const expiry = pm.collectionVariables.get("token_expiry");
const now = new Date().getTime();

if (!token || (expiry && now > expiry)) {
    pm.sendRequest({
        url: pm.variables.get("base_url") + "/auth/token",
        method: 'GET'
    }, function(err, res) {
        if (res.code === 200) {
            const data = res.json();
            pm.collectionVariables.set("access_token", data.access_token);
            pm.collectionVariables.set("token_expiry", now + (50 * 60 * 1000));
        }
    });
}
```

## Manual Token Retrieval

### From Active Session:
```
GET http://localhost:5656/auth/token
```
Returns your current session token if logged in.

### Fresh Authentication:
1. `GET http://localhost:5656/auth/login-postman` - Get auth URL
2. Open auth URL in browser
3. Complete OKTA login  
4. Get token from JSON response
5. Set as Bearer token in POSTMAN

## Testing Your Setup

### Test API Call:
```
GET http://localhost:5656/api/COMPANYTB
Authorization: Bearer {{access_token}}
```

### Debug Token:
```
GET http://localhost:5656/auth/user
```
Shows current authenticated user info.

## Common Issues

### "Not authenticated" error:
- Token expired (OKTA tokens last 1 hour)
- Get new token via `/auth/login-postman` flow

### "Invalid token" error:
- Copy full token without extra spaces
- Ensure Bearer prefix in Authorization header

### Collection not using token:
- Check Collection → Authorization is set to Bearer Token
- Verify token variable name matches (`{{access_token}}`)

## Environment Variables

Set these in your environment:
```
OKTA_API_TOKEN=your_okta_api_token_here
```

This enables user lookup by email functionality.

## Token Expiry

- OKTA tokens expire in 1 hour
- Collection auto-refreshes if session active  
- Manual re-auth needed if session expired
