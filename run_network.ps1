# PowerShell script to start Flask server for network access
# run_network.ps1

Write-Host "Starting Flask API Logic Server for Network Access..." -ForegroundColor Green
Write-Host "Server will be accessible at: http://192.168.13.31:5656" -ForegroundColor Yellow
Write-Host ""

# Set environment variables for network access
$env:APILOGICPROJECT_FLASK_HOST = "0.0.0.0"
$env:APILOGICPROJECT_SWAGGER_HOST = "192.168.13.31"  
$env:APILOGICPROJECT_PORT = "5656"

# Display network information
Write-Host "Network Configuration:" -ForegroundColor Cyan
Write-Host "  Flask Host: $env:APILOGICPROJECT_FLASK_HOST (binds to all interfaces)" -ForegroundColor White
Write-Host "  Swagger Host: $env:APILOGICPROJECT_SWAGGER_HOST (your IP address)" -ForegroundColor White
Write-Host "  Port: $env:APILOGICPROJECT_PORT" -ForegroundColor White
Write-Host ""

# Check if firewall rule exists
$firewallRule = Get-NetFirewallRule -DisplayName "Flask API Server" -ErrorAction SilentlyContinue
if (-not $firewallRule) {
    Write-Host "Adding Windows Firewall rule for port 5656..." -ForegroundColor Yellow
    New-NetFirewallRule -DisplayName "Flask API Server" -Direction Inbound -Protocol TCP -LocalPort 5656 -Action Allow
    Write-Host "Firewall rule added successfully!" -ForegroundColor Green
} else {
    Write-Host "Firewall rule already exists." -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting server..." -ForegroundColor Green
Write-Host "External users can access:"
Write-Host "  Admin App: http://192.168.13.31:5656" -ForegroundColor Yellow
Write-Host "  API Docs:  http://192.168.13.31:5656/api" -ForegroundColor Yellow
Write-Host ""

# Start the Flask application
python api_logic_server_run.py --flask_host 0.0.0.0 --swagger_host 192.168.13.31 --port 5656