# PowerShell script to diagnose Cognito 403 Forbidden error
# This will help identify the exact cause of the issue

Write-Host "🔍 Cognito 403 Forbidden Diagnostic Script" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan

# Check if server is running
Write-Host "`n1️⃣ Checking if Flask server is running..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5656" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "   ✅ Server is running on HTTP port 5656" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Server not responding on HTTP port 5656" -ForegroundColor Red
    Write-Host "   💡 Try starting the server first: python api_logic_server_run.py" -ForegroundColor Yellow
    
    # Check HTTPS
    try {
        $response = Invoke-WebRequest -Uri "https://localhost:5656" -Method GET -TimeoutSec 5 -SkipCertificateCheck -ErrorAction Stop
        Write-Host "   ✅ Server is running on HTTPS port 5656" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Server not responding on HTTPS port 5656 either" -ForegroundColor Red
        exit 1
    }
}

# Check debug endpoint
Write-Host "`n2️⃣ Checking Cognito configuration..." -ForegroundColor Yellow

try {
    $debugResponse = Invoke-RestMethod -Uri "http://localhost:5656/auth/debug" -Method GET -ErrorAction Stop
    
    Write-Host "   ✅ Debug endpoint accessible" -ForegroundColor Green
    Write-Host "`n📊 Configuration Analysis:" -ForegroundColor Magenta
    
    $config = $debugResponse.cognito_configuration
    
    Write-Host "   Region: $($config.region)" -ForegroundColor White
    Write-Host "   User Pool ID: $($config.user_pool_id)" -ForegroundColor White
    Write-Host "   Client ID: $($config.client_id)" -ForegroundColor White
    Write-Host "   Domain: $($config.domain)" -ForegroundColor White
    Write-Host "   Redirect URI: $($config.redirect_uri)" -ForegroundColor White
    
    # Check for common issues
    Write-Host "`n🚨 Issue Analysis:" -ForegroundColor Red
    
    $currentUrl = $debugResponse.current_request.host_url + "auth/callback"
    $configuredUri = $config.redirect_uri
    
    Write-Host "   Expected callback: $currentUrl" -ForegroundColor Yellow
    Write-Host "   Configured URI:   $configuredUri" -ForegroundColor Yellow
    
    if ($currentUrl -eq $configuredUri) {
        Write-Host "   ✅ Redirect URI matches" -ForegroundColor Green
    } else {
        Write-Host "   ❌ REDIRECT URI MISMATCH - This is likely the cause!" -ForegroundColor Red
        Write-Host "   🔧 Fix: Update COGNITO_REDIRECT_URI environment variable to: $currentUrl" -ForegroundColor Yellow
    }
    
    # Check if values are defaults
    if ($config.client_id -like "*4daf1daa8hcs79ts7rugo362lt*") {
        Write-Host "   ❌ Using default/example Client ID" -ForegroundColor Red
    }
    
    if ($config.domain -like "*us-east-1d38hie2qm*") {
        Write-Host "   ❌ Using default/example Domain" -ForegroundColor Red
    }
    
} catch {
    Write-Host "   ❌ Cannot access debug endpoint: $($_.Exception.Message)" -ForegroundColor Red
}

# Try login endpoint
Write-Host "`n3️⃣ Testing login endpoint..." -ForegroundColor Yellow

try {
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:5656/auth/login-postman" -Method GET -ErrorAction Stop
    
    Write-Host "   ✅ Login endpoint accessible" -ForegroundColor Green
    Write-Host "   🔗 Auth URL generated successfully" -ForegroundColor Green
    
    $authUrl = $loginResponse.auth_url
    Write-Host "   Generated URL: $authUrl" -ForegroundColor Cyan
    
    # Test the auth URL
    Write-Host "`n4️⃣ Testing Cognito domain accessibility..." -ForegroundColor Yellow
    
    $cognitoDomain = ($authUrl -split '/oauth2')[0]
    
    try {
        $cognitoResponse = Invoke-WebRequest -Uri "$cognitoDomain/.well-known/openid-configuration" -Method GET -TimeoutSec 10 -ErrorAction Stop
        Write-Host "   ✅ Cognito domain is accessible" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Cannot access Cognito domain: $cognitoDomain" -ForegroundColor Red
        Write-Host "   💡 Check if COGNITO_DOMAIN is correct" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "   ❌ Cannot access login endpoint: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🔧 Recommended Actions:" -ForegroundColor Magenta
Write-Host "1. Check the redirect URI mismatch above" -ForegroundColor White
Write-Host "2. Verify your Cognito App Client settings in AWS Console" -ForegroundColor White
Write-Host "3. Ensure callback URL matches exactly: http://localhost:5656/auth/callback" -ForegroundColor White
Write-Host "4. Check if you're using example/default values instead of real ones" -ForegroundColor White

Write-Host "`n💡 Quick Fix Commands:" -ForegroundColor Magenta
Write-Host "`$env:COGNITO_REDIRECT_URI = 'http://localhost:5656/auth/callback'" -ForegroundColor Yellow
Write-Host "`$env:COGNITO_CLIENT_ID = 'your-real-client-id'" -ForegroundColor Yellow
Write-Host "`$env:COGNITO_DOMAIN = 'https://your-domain.auth.region.amazoncognito.com'" -ForegroundColor Yellow

Write-Host "`nDone! ✨" -ForegroundColor Green