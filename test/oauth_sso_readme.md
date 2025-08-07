# OAuth SSO Authorization Code Guide

## 🔑 What is an Authorization Code?

An **Authorization Code** is a temporary, one-time-use token in the OAuth 2.0 Authorization Code flow. It represents the user's consent to allow your application to access their information and serves as the bridge between user authentication with OKTA and your application receiving access tokens.

## 🔄 OAuth 2.0 Authorization Code Flow

Here's how the complete OAuth flow works in your OKTA setup:

### Step 1: Authorization Request
When a user clicks "Login", your app redirects to OKTA:

```
https://ou.okta.com/oauth2/v1/authorize?
  client_id=0oa1crjfiwoxRYadi0x8&
  response_type=code&
  redirect_uri=http://localhost:5656/auth/callback&
  scope=openid profile email&
  state=random_string&
  nonce=random_string
```

### Step 2: User Authentication
- User logs into OKTA with username/password
- OKTA verifies credentials
- User sees consent screen (if configured)

### Step 3: Authorization Code Issued
OKTA redirects back to your app with the authorization code:

```
http://localhost:5656/auth/callback?
  code=0AbCdEf1GhIj2KlMn3OpQr4StUv5WxYz6&
  state=random_string
```

### Step 4: Token Exchange
Your app exchanges the code for tokens:

```http
POST https://ou.okta.com/oauth2/v1/token
Authorization: Basic base64(client_id:client_secret)
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=0AbCdEf1GhIj2KlMn3OpQr4StUv5WxYz6&
redirect_uri=http://localhost:5656/auth/callback
```

### Step 5: Tokens Received
OKTA responds with access and ID tokens:

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiI...",
  "id_token": "eyJhbGciOiJSUzI1NiI...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "openid profile email"
}
```

## 📝 Authorization Code Characteristics

| Property | Value |
|----------|-------|
| **Lifetime** | Very short (typically 60 seconds or less) |
| **Usage** | Single-use only (cannot be reused) |
| **Format** | Random string (usually 30-50 characters) |
| **Purpose** | Exchange for access/ID tokens |
| **Security** | Must match exact redirect URI |

## 🔍 Example Authorization Code

A real OKTA Authorization Code might look like:
```
0AbCdEf1GhIj2KlMn3OpQr4StUv5WxYz6A7B8C9D0E1F2G3H4I5J6K7L8M9N0O1P
```

## ⚠️ Common Issues with Authorization Codes

### 1. "Authorization code is invalid or has expired"

**Most Common Causes:**
- Authorization code used multiple times (codes are single-use)
- Authorization code expired (>60 seconds)
- Redirect URI mismatch between authorization and token requests

**Solutions:**
- Process the authorization code immediately after receiving it
- Don't refresh the callback page after successful authentication
- Ensure redirect URI matches exactly in all requests

### 2. "The 'redirect_uri' parameter must be a Login redirect URI in the client app settings"

**Cause:** Your OKTA application configuration doesn't include the redirect URI you're using.

**Solution:** Update OKTA Application Settings:
1. Log into OKTA Admin Console: https://ou.okta.com/admin
2. Navigate to **Applications** → **Applications**
3. Find your application with Client ID: `0oa1crjfiwoxRYadi0x8`
4. Go to the **General** tab
5. In the **Login** section, add your redirect URI to **Sign-in redirect URIs**
6. Ensure exact match: `http://localhost:5656/auth/callback`

### 3. "Cannot supply multiple client credentials"

**Cause:** Sending client credentials in both Authorization header AND request body.

**Solution:** Use only Basic Auth header (fixed in current implementation):
```python
headers = {
    'Authorization': f'Basic {base64_credentials}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# DON'T include client_id and client_secret in body
data = {
    'grant_type': 'authorization_code',
    'code': auth_code,
    'redirect_uri': redirect_uri
}
```

## 🛠️ Debug Tools

### 1. OAuth Callback Inspector
Run the callback inspector to see exactly what parameters are received:

```bash
python test/callback_inspector.py
```

- Listens on: http://localhost:5555/auth/callback
- View debug info at: http://localhost:5555/auth/debug

### 2. OAuth Flow Debug Script
Test the complete OAuth flow step by step:

```bash
python test/debug_oauth_flow.py
```

This script will:
- Test OpenID configuration
- Generate authorization URLs
- Test token exchange with various scenarios
- Provide specific error analysis

## 🔧 Configuration Checklist

### OKTA Application Settings
Verify your OKTA app configuration includes:

- **Application Type:** Web Application
- **Grant Types:** Authorization Code ✅
- **Sign-in redirect URIs:** 
  - `http://localhost:5656/auth/callback`
  - `http://localhost:5555/auth/callback` (for testing)
- **Sign-out redirect URIs:** 
  - `http://localhost:5656`
  - `http://localhost:5555`

### Environment Variables
Ensure these are set in your `config/default.env`:

```env
OKTA_DOMAIN=https://ou.okta.com
OKTA_CLIENT_ID=0oa1crjfiwoxRYadi0x8
OKTA_CLIENT_SECRET=eVdobSwZgx8ANVRwPTxX6lce24t4e5ZBuAQSn_QPopvi69Xa36SWoyPjH4WcjAI7
OKTA_REDIRECT_URI=http://localhost:5656/auth/callback
```

## 🚀 Testing Your OAuth Flow

### Quick Test Steps:

1. **Start the callback inspector:**
   ```bash
   python test/callback_inspector.py
   ```

2. **Temporarily update OKTA app redirect URI to:** 
   ```
   http://localhost:5555/auth/callback
   ```

3. **Generate test authorization URL:**
   ```bash
   python test/debug_oauth_flow.py
   ```

4. **Copy the authorization URL from output and paste in browser**

5. **Login with your OKTA credentials**

6. **Check the callback inspector console for the authorization code**

7. **Copy the authorization code and test token exchange**

### Expected Flow:
1. Browser redirects to OKTA login
2. After successful login, redirects to callback inspector
3. Callback inspector shows authorization code in console
4. Use the code to test token exchange

## 📚 Implementation Files

### Key Files:
- `security/authentication_provider/okta/auth_provider.py` - Main OKTA authentication provider
- `security/authentication_provider/okta/okta_token.py` - Token management utilities
- `test/callback_inspector.py` - Debug callback parameters
- `test/debug_oauth_flow.py` - Test OAuth flow step by step
- `config/default.env` - Configuration settings

### Important Methods:
- `_add_okta_endpoints()` - Adds OAuth endpoints to Flask app
- `_exchange_code_for_tokens()` - Exchanges authorization code for tokens
- `validate_okta_token()` - Validates received ID tokens

## 🔍 Troubleshooting Checklist

When you encounter authorization code issues, check:

- [ ] **Redirect URI exact match** in all three places:
  - Authorization request
  - Token exchange request  
  - OKTA app configuration

- [ ] **Authorization code used only once** - codes are single-use

- [ ] **Code processed immediately** - codes expire in ~60 seconds

- [ ] **No page refreshes** on callback endpoint after successful auth

- [ ] **Client credentials properly formatted** - Basic Auth header only

- [ ] **OKTA app configured for Authorization Code flow**

- [ ] **Correct scopes requested:** `openid profile email`

## 📞 Getting Help

If you're still encountering issues:

1. **Run the debug script:** `python test/debug_oauth_flow.py`
2. **Check callback inspector logs:** `python test/callback_inspector.py`
3. **Verify OKTA app configuration** matches your redirect URIs exactly
4. **Check OKTA admin logs** for detailed error messages

## 🎯 Success Indicators

You know your OAuth flow is working when:

- ✅ Authorization URL redirects to OKTA login
- ✅ After login, redirects to your callback with `code` parameter
- ✅ Token exchange returns `access_token` and `id_token`
- ✅ ID token validates successfully
- ✅ User session is created with proper claims

---

*This guide covers the complete OAuth 2.0 Authorization Code flow for OKTA SSO integration. Keep this file updated as you make configuration changes.*
