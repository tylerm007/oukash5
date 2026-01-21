# Set Teams Webhook URL Environment Variable
# Run this: . .\set_teams_env.ps1

$env:TEAMS_WEBHOOK_URL = "https://defaulteec94eb4840d4d2ca7f105b024e605.80.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/2bce774ace0947e3a3e6d7db26749c78/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=2vjsOgKvgKOY3aFegAJ18ZQQ06We9zx_hX-161sRMXA"

Write-Host "✅ TEAMS_WEBHOOK_URL environment variable set!" -ForegroundColor Green
Write-Host ""
Write-Host "Webhook URL: $($env:TEAMS_WEBHOOK_URL.Substring(0, 80))..." -ForegroundColor Gray
Write-Host ""
Write-Host "Test it with: .\test_teams_api.ps1" -ForegroundColor Cyan
