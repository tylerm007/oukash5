# Teams API Setup Helper
# Run this script to set up your Teams webhook integration

Write-Host @"
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        Microsoft Teams API Integration Setup              ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host ""

# Skip SSL certificate validation (for self-signed certs)
if (-not ([System.Management.Automation.PSTypeName]'ServerCertificateValidationCallback').Type) {
    $certCallback = @"
        using System;
        using System.Net;
        using System.Net.Security;
        using System.Security.Cryptography.X509Certificates;
        public class ServerCertificateValidationCallback
        {
            public static void Ignore()
            {
                if(ServicePointManager.ServerCertificateValidationCallback == null)
                {
                    ServicePointManager.ServerCertificateValidationCallback += 
                        delegate
                        (
                            Object obj, 
                            X509Certificate certificate, 
                            X509Chain chain, 
                            SslPolicyErrors errors
                        )
                        {
                            return true;
                        };
                }
            }
        }
"@
    Add-Type $certCallback
}
[ServerCertificateValidationCallback]::Ignore()
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Step 1: Check if webhook URL is already set
Write-Host "Step 1: Check Environment Variable" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

if ($env:TEAMS_WEBHOOK_URL) {
    Write-Host "✅ TEAMS_WEBHOOK_URL is already set" -ForegroundColor Green
    Write-Host "   Current value: $($env:TEAMS_WEBHOOK_URL.Substring(0, [Math]::Min(50, $env:TEAMS_WEBHOOK_URL.Length)))..." -ForegroundColor Gray
    
    $change = Read-Host "`nDo you want to change it? (y/n)"
    if ($change -ne 'y') {
        Write-Host "`nKeeping existing webhook URL" -ForegroundColor Green
    } else {
        $env:TEAMS_WEBHOOK_URL = $null
    }
}

if (-not $env:TEAMS_WEBHOOK_URL) {
    Write-Host "❌ TEAMS_WEBHOOK_URL is not set" -ForegroundColor Red
    Write-Host ""
    Write-Host "To get your webhook URL:" -ForegroundColor Yellow
    Write-Host "  1. Open Microsoft Teams" -ForegroundColor White
    Write-Host "  2. Go to your 'NewAPI Team' channel" -ForegroundColor White
    Write-Host "  3. Click the ... (three dots) next to the channel name" -ForegroundColor White
    Write-Host "  4. Select 'Connectors' or 'Workflows'" -ForegroundColor White
    Write-Host "  5. Search for 'Incoming Webhook'" -ForegroundColor White
    Write-Host "  6. Click 'Add' or 'Configure'" -ForegroundColor White
    Write-Host "  7. Give it a name and click 'Create'" -ForegroundColor White
    Write-Host "  8. Copy the webhook URL" -ForegroundColor White
    Write-Host ""
    
    $webhookUrl = Read-Host "Paste your Teams webhook URL here"
    
    if ($webhookUrl) {
        $env:TEAMS_WEBHOOK_URL = $webhookUrl
        Write-Host "✅ Webhook URL set for this session" -ForegroundColor Green
        
        # Offer to save to .env file
        Write-Host ""
        $saveToFile = Read-Host "Do you want to save this to .env file? (y/n)"
        if ($saveToFile -eq 'y') {
            $envFile = "config/default.env"
            if (Test-Path $envFile) {
                # Check if already exists in file
                $content = Get-Content $envFile -Raw
                if ($content -match 'TEAMS_WEBHOOK_URL') {
                    Write-Host "⚠️  TEAMS_WEBHOOK_URL already exists in $envFile" -ForegroundColor Yellow
                    $overwrite = Read-Host "Overwrite it? (y/n)"
                    if ($overwrite -eq 'y') {
                        $content = $content -replace 'TEAMS_WEBHOOK_URL=.*', "TEAMS_WEBHOOK_URL=$webhookUrl"
                        Set-Content -Path $envFile -Value $content
                        Write-Host "✅ Updated $envFile" -ForegroundColor Green
                    }
                } else {
                    Add-Content -Path $envFile -Value "`nTEAMS_WEBHOOK_URL=$webhookUrl"
                    Write-Host "✅ Added to $envFile" -ForegroundColor Green
                }
            } else {
                # Create new .env file
                "TEAMS_WEBHOOK_URL=$webhookUrl" | Out-File -FilePath $envFile -Encoding UTF8
                Write-Host "✅ Created $envFile" -ForegroundColor Green
            }
        }
    } else {
        Write-Host "⚠️  No webhook URL provided. You can set it later." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

# Step 2: Check if server is running
Write-Host "Step 2: Check API Server" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

try {
    $testResponse = Invoke-RestMethod -Uri "http://localhost:5656/hello_world?user=test" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ API server is running on http://localhost:5656" -ForegroundColor Green
} catch {
    Write-Host "❌ API server is not running" -ForegroundColor Red
    Write-Host ""
    Write-Host "To start the server:" -ForegroundColor Yellow
    Write-Host "  python api_logic_server_run.py" -ForegroundColor White
    Write-Host ""
    
    $startNow = Read-Host "Do you want to start it now? (y/n)"
    if ($startNow -eq 'y') {
        Write-Host "Starting server in new window..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python api_logic_server_run.py"
        Write-Host "Waiting for server to start..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        
        # Test again
        try {
            $testResponse = Invoke-RestMethod -Uri "http://localhost:5656/hello_world?user=test" -TimeoutSec 2
            Write-Host "✅ Server started successfully" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  Server may still be starting. Please wait a moment and try again." -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

# Step 3: Test the integration
Write-Host "Step 3: Test Teams Integration" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

if ($env:TEAMS_WEBHOOK_URL) {
    $runTest = Read-Host "Send a test message to Teams? (y/n)"
    
    if ($runTest -eq 'y') {
        Write-Host "`nSending test message..." -ForegroundColor Green
        
        $testBody = @{
            title = "🎉 Setup Complete!"
            message = "Your Teams API integration is working!`n`n**Time**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            message_type = "card"
            color = "00FF00"
        } | ConvertTo-Json
        
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:5656/teams/send_message" -Method POST -Body $testBody -ContentType "application/json"
            Write-Host "✅ Test message sent successfully!" -ForegroundColor Green
            Write-Host "   Check your 'NewAPI Team' channel in Teams" -ForegroundColor Gray
            Write-Host ""
            Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor Gray
        } catch {
            Write-Host "❌ Failed to send test message" -ForegroundColor Red
            Write-Host "   Error: $_" -ForegroundColor Red
        }
    }
} else {
    Write-Host "⚠️  Skipping test - webhook URL not configured" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

# Summary
Write-Host "Setup Summary" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

if ($env:TEAMS_WEBHOOK_URL) {
    Write-Host "✅ Webhook URL: Configured" -ForegroundColor Green
} else {
    Write-Host "❌ Webhook URL: Not configured" -ForegroundColor Red
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  • Run full test suite: .\test_teams_api.ps1" -ForegroundColor White
Write-Host "  • Read documentation: docs\TEAMS_API_SETUP.md" -ForegroundColor White
Write-Host "  • Quick reference: docs\TEAMS_API_QUICKREF.md" -ForegroundColor White
Write-Host "  • Summary: TEAMS_API_README.md" -ForegroundColor White
Write-Host ""

Write-Host "API Endpoint:" -ForegroundColor Yellow
Write-Host "  POST http://localhost:5656/teams/send_message" -ForegroundColor White
Write-Host ""

Write-Host "Quick Test:" -ForegroundColor Yellow
Write-Host @'
  $body = @{
      message = "Hello Teams!"
      message_type = "card"
      title = "Test"
  } | ConvertTo-Json
  Invoke-RestMethod -Uri "http://localhost:5656/teams/send_message" -Method POST -Body $body -ContentType "application/json"
'@ -ForegroundColor Gray

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

$runFullTest = Read-Host "Run full test suite now? (y/n)"
if ($runFullTest -eq 'y') {
    Write-Host ""
    & .\test_teams_api.ps1
}

Write-Host ""
Write-Host "Setup complete! 🚀" -ForegroundColor Green
Write-Host ""
