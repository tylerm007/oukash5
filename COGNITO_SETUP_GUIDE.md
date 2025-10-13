# Amazon Cognito Setup Instructions

## 🎯 How to Get Your Real Cognito Values

### 1. Go to AWS Cognito Console
- Open [AWS Console](https://console.aws.amazon.com/)
- Navigate to **Amazon Cognito**
- Select **User pools**

### 2. Create or Select User Pool
If you don't have one:
- Click **Create user pool**
- Choose **Cognito user pool** sign-in options
- Configure as needed
- Note down the **User Pool ID** (format: `us-east-1_XXXXXXXXX`)

### 3. Create or Configure App Client
- Go to your User Pool
- Click **App integration** tab
- Under **App clients and analytics**, click **Create app client** or select existing one

#### App Client Settings:
```
App type: Public client OR Confidential client (with secret)
App client name: your-app-name
Authentication flows: 
  ✅ ALLOW_ADMIN_USER_PASSWORD_AUTH
  ✅ ALLOW_USER_PASSWORD_AUTH  
  ✅ ALLOW_REFRESH_TOKEN_AUTH
```

#### OAuth 2.0 Settings:
```
Allowed callback URLs:
  http://localhost:5656/auth/callback
  https://192.168.13.31:5656/auth/callback

Allowed sign-out URLs:
  http://localhost:5656/
  
OAuth 2.0 grant types:
  ✅ Authorization code grant
  
OAuth 2.0 scopes:
  ✅ openid
  ✅ profile
  ✅ email
```

### 4. Get Your Values

After creating the app client, you'll see:

1. **User Pool ID**: `us-east-1_XXXXXXXXX` (from User Pool details page)
2. **Client ID**: `1234567890abcdefghij` (from App client details)
3. **Client Secret**: Click "Show client secret" (only if Confidential client)

### 5. Set Up Domain (Optional - for Hosted UI)
- Go to **App integration** → **Domain**
- Choose **Cognito domain** or **Custom domain**
- If Cognito domain: `https://your-domain.auth.us-east-1.amazoncognito.com`

### 6. Update Your Environment Variables

Replace the values in `set_cognito_env.ps1`:

```powershell
$env:COGNITO_REGION = "us-east-1"                                    # Your region
$env:COGNITO_USER_POOL_ID = "us-east-1_XXXXXXXXX"                    # From step 2
$env:COGNITO_CLIENT_ID = "1234567890abcdefghij"                      # From step 3
$env:COGNITO_CLIENT_SECRET = "your-secret-if-confidential-client"    # From step 3
$env:COGNITO_DOMAIN = "https://your-domain.auth.us-east-1.amazoncognito.com"  # From step 5
$env:COGNITO_REDIRECT_URI = "http://localhost:5656/auth/callback"
```

### 7. Test Setup

1. Run: `.\set_cognito_env.ps1`
2. Start Flask: `python api_logic_server_run.py`
3. Test: Navigate to `http://localhost:5656/auth/login-postman`

## 🔍 Troubleshooting 403 Errors

**Common Causes:**
- ❌ Using example/default values (most common!)
- ❌ Redirect URI mismatch between Cognito config and environment variable
- ❌ Invalid Client ID or Client Secret
- ❌ OAuth flows not enabled in Cognito
- ❌ App client not configured for your domain

**Debug Steps:**
1. Check `/auth/debug` endpoint for configuration
2. Verify redirect URI matches exactly
3. Check Cognito CloudWatch logs for detailed errors
4. Ensure OAuth scopes are properly configured