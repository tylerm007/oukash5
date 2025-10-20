# Cognito 403 Quick Diagnostic Script
Write-Host "🔍 Cognito 403 Error Quick Diagnostic" -ForegroundColor Red
Write-Host "=====================================" -ForegroundColor Cyan

# Set the environment variables first
Write-Host "`n📋 Setting Environment Variables..." -ForegroundColor Yellow
$env:COGNITO_REGION = "us-east-1"
$env:COGNITO_USER_POOL_ID = "us-east-1_d38hiE2QM"
$env:COGNITO_CLIENT_ID = "34sqr8ttgro6ego2117aflg9lr"
$env:COGNITO_CLIENT_SECRET = "rev05ljd8067sbigkhlk153eluh78qgsh8dfptueehdalk42dmg"
$env:COGNITO_DOMAIN = "https://auth.oudirect-st.ou.org"
$env:COGNITO_REDIRECT_URI = "http://192.168.13.31:5656/auth/callback"

Write-Host "✅ Environment variables set" -ForegroundColor Green

Write-Host "`n🚀 Starting Flask server..." -ForegroundColor Yellow
Write-Host "Please wait 10 seconds for server to start..." -ForegroundColor Gray

# Start Flask server in background
$job = Start-Job -ScriptBlock {
    Set-Location "c:\OUProjects\oukash5"
    python api_logic_server_run.py
}

# Wait for server to start
Start-Sleep -Seconds 10

Write-Host "`n🧪 Testing Endpoints..." -ForegroundColor Yellow

# Test 1: Debug endpoint
Write-Host "`n1️⃣ Testing /auth/debug endpoint..." -ForegroundColor Magenta
try {
    $debugResponse = Invoke-RestMethod -Uri "http://192.168.13.31:5656/auth/debug" -Method GET -TimeoutSec 5
    Write-Host "   ✅ Debug endpoint working" -ForegroundColor Green
    Write-Host "   Server Host: $($debugResponse.current_request.host)" -ForegroundColor White
    Write-Host "   Expected Callback: $($debugResponse.current_request.host_url)auth/callback" -ForegroundColor White
    Write-Host "   Configured Callback: $($debugResponse.cognito_configuration.redirect_uri)" -ForegroundColor White
    
    if ($debugResponse.current_request.host_url + "auth/callback" -eq $debugResponse.cognito_configuration.redirect_uri) {
        Write-Host "   ✅ Callback URLs MATCH" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Callback URLs DO NOT MATCH - This is likely the 403 cause!" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ Debug endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Login endpoint (the one giving 403)
Write-Host "`n2️⃣ Testing /auth/login endpoint..." -ForegroundColor Magenta
try {
    $loginResponse = Invoke-WebRequest -Uri "http://192.168.13.31:5656/auth/login" -Method GET -TimeoutSec 5
    Write-Host "   ✅ Login endpoint working - Status: $($loginResponse.StatusCode)" -ForegroundColor Green
    if ($loginResponse.StatusCode -eq 302) {
        Write-Host "   ✅ Redirect to Cognito successful" -ForegroundColor Green
    }
} catch {
    if ($_.Exception.Response.StatusCode -eq 403) {
        Write-Host "   ❌ 403 FORBIDDEN ERROR - Found the problem!" -ForegroundColor Red
        Write-Host "   This confirms the Cognito configuration issue" -ForegroundColor Red
    } else {
        Write-Host "   ❌ Login endpoint error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Test 3: Cognito domain accessibility
Write-Host "`n3️⃣ Testing Cognito Domain..." -ForegroundColor Magenta
try {
    $cognitoTest = Invoke-WebRequest -Uri "$env:COGNITO_DOMAIN/.well-known/openid-configuration" -Method GET -TimeoutSec 5
    Write-Host "   ✅ Cognito domain accessible" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Cognito domain not accessible: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🔧 SOLUTION:" -ForegroundColor Green
Write-Host "The most likely fix for your 403 error:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Go to AWS Cognito Console" -ForegroundColor White
Write-Host "2. Find your User Pool: us-east-1_d38hiE2QM" -ForegroundColor White
Write-Host "3. Go to App clients → Your app → App client settings" -ForegroundColor White
Write-Host "4. In 'Callback URL(s)' add: http://192.168.13.31:5656/auth/callback" -ForegroundColor Cyan
Write-Host "5. Ensure these OAuth settings:" -ForegroundColor White
Write-Host "   ✓ Authorization code grant" -ForegroundColor Green
Write-Host "   ✓ Allowed OAuth Scopes: openid, profile, email" -ForegroundColor Green
Write-Host "6. Save changes" -ForegroundColor White

Write-Host "`n🧪 Quick Test Command:" -ForegroundColor Magenta
Write-Host "After fixing Cognito settings, test with:" -ForegroundColor White
Write-Host "Invoke-WebRequest -Uri 'http://192.168.13.31:5656/auth/login' -Method GET" -ForegroundColor Cyan

# Clean up
Write-Host "`n🧹 Cleaning up..." -ForegroundColor Yellow
Stop-Job -Job $job -ErrorAction SilentlyContinue
Remove-Job -Job $job -ErrorAction SilentlyContinue

Write-Host "Done!" -ForegroundColor Green