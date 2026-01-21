Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Restart API Logic Server for Teams   ║" -ForegroundColor Cyan  
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "The Teams integration has been updated to support Power Automate webhooks." -ForegroundColor Yellow
Write-Host "Please restart your API Logic Server to pick up the changes:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Stop the current server (Ctrl+C in the terminal)" -ForegroundColor White
Write-Host "2. Restart with: python api_logic_server_run.py" -ForegroundColor White
Write-Host ""
Write-Host "After restart, run: .\test_teams_api.ps1" -ForegroundColor Green
Write-Host ""

$restart = Read-Host "Do you want me to try to restart it now? (y/n)"

if ($restart -eq 'y') {
    Write-Host ""
    Write-Host "Stopping any existing API Logic Server processes..." -ForegroundColor Yellow
    
    # Try to stop any running Python processes with api_logic_server
    Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*api_logic_server_run*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    
    Start-Sleep -Seconds 2
    
    Write-Host "Starting API Logic Server in new window..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python api_logic_server_run.py"
    
    Write-Host ""
    Write-Host "Server starting... Wait 5-10 seconds, then run: .\test_teams_api.ps1" -ForegroundColor Cyan
} else {
    Write-Host "Please restart manually when ready." -ForegroundColor Gray
}
