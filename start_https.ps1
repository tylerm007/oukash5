# PowerShell script to start Flask with HTTPS support
# Usage examples:
#   .\start_https.ps1                    # Start with HTTPS if certificates exist
#   .\start_https.ps1 -GenerateCert      # Generate certificates and start HTTPS
#   .\start_https.ps1 -HTTP              # Force HTTP mode

param(
    [switch]$GenerateCert = $false,
    [switch]$HTTP = $false,
    [string]$Host = "localhost",
    [int]$Port = 5656
)

Write-Host "🚀 API Logic Server HTTPS Startup Script" -ForegroundColor Green

# Check if certificates should be generated
if ($GenerateCert -or (-not (Test-Path "security\ssl\server.crt") -and -not $HTTP)) {
    Write-Host "📝 Generating SSL certificates..." -ForegroundColor Cyan
    
    if (Test-Path "security\ssl\generate_cert.ps1") {
        & "security\ssl\generate_cert.ps1" -Domain $Host
    } else {
        Write-Host "❌ Certificate generation script not found at security\ssl\generate_cert.ps1" -ForegroundColor Red
        Write-Host "💡 Run this first: python security\ssl\generate_cert.py" -ForegroundColor Yellow
        exit 1
    }
}

# Set environment variables based on mode
if ($HTTP) {
    Write-Host "🌐 Starting in HTTP mode..." -ForegroundColor Yellow
    $env:FLASK_USE_SSL = "false"
    $env:APILOGICPROJECT_HTTP_SCHEME = "http"
} else {
    Write-Host "🔒 Starting in HTTPS mode..." -ForegroundColor Green
    $env:FLASK_USE_SSL = "true" 
    $env:APILOGICPROJECT_HTTP_SCHEME = "https"
    $env:FLASK_SSL_CERT = "security\ssl\server.crt"
    $env:FLASK_SSL_KEY = "security\ssl\server.key"
    $env:FLASK_SSL_PFX = "security\ssl\server.pfx"
    $env:FLASK_SSL_PFX_PASSWORD = "flask-dev-cert"
}

# Set host and port
$env:APILOGICPROJECT_FLASK_HOST = $Host
$env:APILOGICPROJECT_PORT = $Port.ToString()
$env:APILOGICPROJECT_SWAGGER_HOST = $Host

# Display startup information
Write-Host "`n📊 Configuration:" -ForegroundColor Magenta
Write-Host "  Host: $Host" -ForegroundColor White
Write-Host "  Port: $Port" -ForegroundColor White
Write-Host "  SSL: $(if ($HTTP) { 'Disabled' } else { 'Enabled' })" -ForegroundColor White
Write-Host "  URL: $($env:APILOGICPROJECT_HTTP_SCHEME)://$Host:$Port" -ForegroundColor Yellow

if (-not $HTTP) {
    Write-Host "`n🔐 SSL Certificate Information:" -ForegroundColor Magenta
    if (Test-Path "security\ssl\server.crt") {
        Write-Host "  Certificate: security\ssl\server.crt ✅" -ForegroundColor Green
    } else {
        Write-Host "  Certificate: security\ssl\server.crt ❌" -ForegroundColor Red
    }
    
    if (Test-Path "security\ssl\server.key") {
        Write-Host "  Private Key: security\ssl\server.key ✅" -ForegroundColor Green
    } else {
        Write-Host "  Private Key: security\ssl\server.key ❌" -ForegroundColor Red
    }
    
    Write-Host "`n⚠️  Browser Security Notice:" -ForegroundColor Yellow
    Write-Host "  Your browser will show a security warning for self-signed certificates." -ForegroundColor White
    Write-Host "  Click 'Advanced' -> 'Proceed to $Host (unsafe)' to continue." -ForegroundColor White
}

Write-Host "`n🎯 Access URLs:" -ForegroundColor Magenta
Write-Host "  Admin App: $($env:APILOGICPROJECT_HTTP_SCHEME)://$Host:$Port" -ForegroundColor Cyan
Write-Host "  API Docs:  $($env:APILOGICPROJECT_HTTP_SCHEME)://$Host:$Port/api" -ForegroundColor Cyan
Write-Host "  Auth Login: $($env:APILOGICPROJECT_HTTP_SCHEME)://$Host:$Port/auth/login" -ForegroundColor Cyan

Write-Host "`n🚀 Starting Flask application..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray

# Start the Flask application
try {
    python api_logic_server_run.py
} catch {
    Write-Host "❌ Error starting Flask application: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Make sure you're in the project root directory" -ForegroundColor Yellow
    Write-Host "💡 Make sure Python environment is activated" -ForegroundColor Yellow
}