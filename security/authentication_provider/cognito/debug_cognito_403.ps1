# Cognito 403 Debugging Script
# This will help identify the exact cause of the 403 error

Write-Host "🔍 Cognito 403 Error Diagnostic" -ForegroundColor Red
Write-Host "==============================" -ForegroundColor Cyan

Write-Host "`n1️⃣ Checking Current Environment Variables..." -ForegroundColor Yellow

# Display current Cognito configuration
Write-Host "`n📋 Current Configuration:" -ForegroundColor Magenta
Write-Host "   COGNITO_REGION: $env:COGNITO_REGION" -ForegroundColor White
Write-Host "   COGNITO_USER_POOL_ID: $env:COGNITO_USER_POOL_ID" -ForegroundColor White
Write-Host "   COGNITO_CLIENT_ID: $env:COGNITO_CLIENT_ID" -ForegroundColor White
Write-Host "   COGNITO_DOMAIN: $env:COGNITO_DOMAIN" -ForegroundColor White
Write-Host "   COGNITO_REDIRECT_URI: $env:COGNITO_REDIRECT_URI" -ForegroundColor White

Write-Host "`n2️⃣ Checking Flask Server Status..." -ForegroundColor Yellow

# Test HTTP connection
try {
    $httpResponse = Invoke-WebRequest -Uri "https://192.168.13.31:5656/auth/debug" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "   ✅ HTTP server responding on port 5656" -ForegroundColor Green
    
    $debugData = $httpResponse.Content | ConvertFrom-Json
    
    Write-Host "`n📊 Server Configuration Analysis:" -ForegroundColor Magenta
    Write-Host "   Server Host: $($debugData.current_request.host)" -ForegroundColor White
    Write-Host "   Server URL: $($debugData.current_request.host_url)" -ForegroundColor White
    Write-Host "   Server Scheme: $($debugData.current_request.scheme)" -ForegroundColor White
    
    Write-Host "`n🔧 Cognito Configuration on Server:" -ForegroundColor Magenta
    Write-Host "   Region: $($debugData.cognito_configuration.region)" -ForegroundColor White
    Write-Host "   User Pool ID: $($debugData.cognito_configuration.user_pool_id)" -ForegroundColor White
    Write-Host "   Client ID: $($debugData.cognito_configuration.client_id)" -ForegroundColor White
    Write-Host "   Domain: $($debugData.cognito_configuration.domain)" -ForegroundColor White
    Write-Host "   Redirect URI: $($debugData.cognito_configuration.redirect_uri)" -ForegroundColor White
    
    # Check for common mismatches
    $expectedCallback = $debugData.current_request.host_url + "auth/callback"
    $configuredCallback = $debugData.cognito_configuration.redirect_uri
    
    Write-Host "`n🚨 Configuration Analysis:" -ForegroundColor Red
    Write-Host "   Expected Callback: $expectedCallback" -ForegroundColor Yellow
    Write-Host "   Configured Callback: $configuredCallback" -ForegroundColor Yellow
    
    if ($expectedCallback -eq $configuredCallback) {
        Write-Host "   ✅ Redirect URIs match!" -ForegroundColor Green
    } else {
        Write-Host "   ❌ REDIRECT URI MISMATCH - This could cause 403!" -ForegroundColor Red
        Write-Host "   🔧 Fix: Set COGNITO_REDIRECT_URI = '$expectedCallback'" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "   ❌ Cannot connect to HTTP server: $($_.Exception.Message)" -ForegroundColor Red
}

# Test HTTPS connection if SSL is enabled
Write-Host "`n3️⃣ Checking HTTPS Configuration..." -ForegroundColor Yellow

try {
    $httpsResponse = Invoke-WebRequest -Uri "https://192.168.13.31:5656/auth/debug" -Method GET -TimeoutSec 5 -SkipCertificateCheck -ErrorAction Stop
    Write-Host "   ✅ HTTPS server also responding" -ForegroundColor Green
    
    Write-Host "   ⚠️  Both HTTP and HTTPS are running - this can cause redirect issues!" -ForegroundColor Yellow
    
} catch {
    Write-Host "   ❌ HTTPS not responding: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n4️⃣ Testing Cognito Domain Accessibility..." -ForegroundColor Yellow

if ($env:COGNITO_DOMAIN) {
    try {
        $wellKnownUrl = "$env:COGNITO_DOMAIN/.well-known/openid-configuration"
        Write-Host "   Testing: $wellKnownUrl" -ForegroundColor Gray
        
        $cognitoResponse = Invoke-WebRequest -Uri $wellKnownUrl -Method GET -TimeoutSec 10 -ErrorAction Stop
        Write-Host "   ✅ Cognito domain is accessible" -ForegroundColor Green
        
        $oidcConfig = $cognitoResponse.Content | ConvertFrom-Json
        Write-Host "   Issuer: $($oidcConfig.issuer)" -ForegroundColor White
        Write-Host "   Authorization Endpoint: $($oidcConfig.authorization_endpoint)" -ForegroundColor White
        
    } catch {
        Write-Host "   ❌ Cannot access Cognito domain: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "   💡 Check if COGNITO_DOMAIN is correct" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ COGNITO_DOMAIN not set" -ForegroundColor Red
}

Write-Host "`n5️⃣ Testing Direct Login Endpoint..." -ForegroundColor Yellow

try {
    # Test the login endpoint that's giving 403
    $loginResponse = Invoke-WebRequest -Uri "https://192.168.13.31:5656/auth/login" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "   ✅ Login endpoint accessible - should redirect to Cognito" -ForegroundColor Green
    
} catch {
    $errorDetails = $_.Exception.Response
    if ($errorDetails.StatusCode -eq 403) {
        Write-Host "   ❌ 403 FORBIDDEN ERROR - This is the problem!" -ForegroundColor Red
        Write-Host "   📄 Error details: $($_.Exception.Message)" -ForegroundColor Red
        
        # Try to get more details
        try {
            $errorContent = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($errorContent)
            $errorText = $reader.ReadToEnd()
            Write-Host "   📄 Error response: $errorText" -ForegroundColor Red
        } catch {
            Write-Host "   📄 Could not read error details" -ForegroundColor Red
        }
        
    } else {
        Write-Host "   ❌ Other error: $($errorDetails.StatusCode) - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n6️⃣ Common 403 Causes & Solutions:" -ForegroundColor Magenta

Write-Host "`n🔍 Most Likely Causes:" -ForegroundColor Red
Write-Host "   1. Redirect URI mismatch between config and Cognito app client" -ForegroundColor White
Write-Host "   2. HTTP/HTTPS mismatch (server running on HTTP, config has HTTPS)" -ForegroundColor White
Write-Host "   3. Cognito App Client not configured for OAuth flows" -ForegroundColor White
Write-Host "   4. Client Secret incorrect or missing" -ForegroundColor White
Write-Host "   5. Cognito Domain incorrect or inaccessible" -ForegroundColor White

Write-Host "`n🔧 Quick Fixes to Try:" -ForegroundColor Green

# Determine the correct scheme
$correctScheme = "http"
if ($env:FLASK_USE_SSL -eq "True") {
    $correctScheme = "https"
}

Write-Host "   # Fix 1: Match your running server scheme" -ForegroundColor Yellow
Write-Host "   `$env:COGNITO_REDIRECT_URI = '${correctScheme}://192.168.13.31:5656/auth/callback'" -ForegroundColor Cyan

Write-Host "`n   # Fix 2: Ensure Cognito domain format is correct" -ForegroundColor Yellow
Write-Host "   # Standard format: https://your-domain.auth.region.amazoncognito.com" -ForegroundColor Gray
Write-Host "   # Your current: $env:COGNITO_DOMAIN" -ForegroundColor Gray

Write-Host "`n   # Fix 3: Verify in AWS Cognito Console:" -ForegroundColor Yellow
Write-Host "   • App Client → App client settings → Callback URL must match exactly" -ForegroundColor White
Write-Host "   • Enabled Identity Providers: Cognito User Pool" -ForegroundColor White
Write-Host "   • OAuth 2.0 → Allowed OAuth Flows: Authorization code grant" -ForegroundColor White
Write-Host "   • OAuth 2.0 → Allowed OAuth Scopes: openid, profile, email" -ForegroundColor White

Write-Host "`n   # Fix 4: Test with simplified config" -ForegroundColor Yellow
Write-Host "   `$env:COGNITO_REDIRECT_URI = 'https://192.168.13.31:5656/auth/callback'" -ForegroundColor Cyan
Write-Host "   `$env:FLASK_USE_SSL = 'False'" -ForegroundColor Cyan

Write-Host "`n🧪 Next Steps:" -ForegroundColor Magenta
Write-Host "   1. Apply one fix above and restart Flask server" -ForegroundColor White
Write-Host "   2. Test: Invoke-WebRequest -Uri 'https://192.168.13.31:5656/auth/login'" -ForegroundColor Cyan
Write-Host "   3. If still 403, check AWS Cognito Console app client settings" -ForegroundColor White
Write-Host "   4. Run this script again to verify fixes" -ForegroundColor White

Write-Host "`nDone!" -ForegroundColor Green