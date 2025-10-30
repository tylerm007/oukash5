# PowerShell script to set Amazon Cognito environment variables
# Replace these with your ACTUAL Cognito values from AWS Console

Write-Host "🔧 Setting Amazon Cognito Environment Variables" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan

# ⚠️ REPLACE THESE WITH YOUR REAL VALUES FROM AWS COGNITO CONSOLE ⚠️
$env:COGNITO_REGION = "us-east-1"                                    # Your AWS region
$env:COGNITO_USER_POOL_ID = "us-east-1_d38hiE2QM"                    # Replace with real User Pool ID
$env:COGNITO_CLIENT_ID = "34sqr8ttgro6ego2117aflg9lr" # "34sqr8ttgro6ego2117aflg9lr"                  # Replace with real Client ID
$env:COGNITO_CLIENT_SECRET = "rev05ljd8067sbigkhlk153eluh78qgsh8dfptueehdalk42dmg"          # Replace with real Client Secret
$env:COGNITO_DOMAIN = "https://auth.oudirect-st.ou.org"
#"https://us-east-1d38hie2qm.auth.us-east-1.amazoncognito.com"  # Replace with real domain

# Set redirect URI to HTTP (matching your current setup)
$env:COGNITO_REDIRECT_URI = "http://localhost:5656/auth/callback"

Write-Host "✅ Environment variables set:" -ForegroundColor Green
Write-Host "   COGNITO_REGION: $($env:COGNITO_REGION)" -ForegroundColor White
Write-Host "   COGNITO_USER_POOL_ID: $($env:COGNITO_USER_POOL_ID)" -ForegroundColor White
Write-Host "   COGNITO_CLIENT_ID: $($env:COGNITO_CLIENT_ID)" -ForegroundColor White
Write-Host "   COGNITO_CLIENT_SECRET: [HIDDEN]" -ForegroundColor White
Write-Host "   COGNITO_DOMAIN: $($env:COGNITO_DOMAIN)" -ForegroundColor White
Write-Host "   COGNITO_REDIRECT_URI: $($env:COGNITO_REDIRECT_URI)" -ForegroundColor White

Write-Host "`n⚠️  IMPORTANT: These are currently set to EXAMPLE values!" -ForegroundColor Red
Write-Host "   You MUST update this script with your real AWS Cognito values" -ForegroundColor Yellow
Write-Host "   from the AWS Console before running your Flask app." -ForegroundColor Yellow

Write-Host "`n🚀 After setting real values, start your Flask app with:" -ForegroundColor Magenta
Write-Host "   python api_logic_server_run.py" -ForegroundColor Cyan