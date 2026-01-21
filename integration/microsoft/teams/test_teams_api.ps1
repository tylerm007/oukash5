# Test script for Teams API integration
# Usage: .\test_teams_api.ps1

Write-Host "=== Teams API Test Script ===" -ForegroundColor Cyan
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

# Also set TLS 1.2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

Write-Host "✅ SSL certificate validation bypassed for self-signed certs" -ForegroundColor Gray
Write-Host ""

# Configuration
$apiUrl = "https://devvm01.nyc.ou.org:5656/teams/send_message"
#https://defaulteec94eb4840d4d2ca7f105b024e605.80.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/2bce774ace0947e3a3e6d7db26749c78/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=2vjsOgKvgKOY3aFegAJ18ZQQ06We9zx_hX-161sRMXA
# Check if TEAMS_WEBHOOK_URL is set
if (-not $env:TEAMS_WEBHOOK_URL) {
    Write-Host "WARNING: TEAMS_WEBHOOK_URL environment variable is not set!" -ForegroundColor Yellow
    Write-Host "You can either:" -ForegroundColor Yellow
    Write-Host "  1. Set it: `$env:TEAMS_WEBHOOK_URL = 'your-webhook-url'" -ForegroundColor Yellow
    Write-Host "  2. Include webhook_url in the request body (see examples below)" -ForegroundColor Yellow
    Write-Host ""
    
    $setNow = Read-Host "Would you like to set it now? (y/n)"
    if ($setNow -eq 'y') {
        $webhookUrl = Read-Host "Enter your Teams webhook URL"
        $env:TEAMS_WEBHOOK_URL = $webhookUrl
        Write-Host "Environment variable set for this session." -ForegroundColor Green
        Write-Host ""
    }
}

# Test 1: Simple Message
Write-Host "Test 1: Sending simple text message..." -ForegroundColor Green
$body1 = @{
    message = "Hello from API Logic Server! Test at $(Get-Date -Format 'HH:mm:ss')"
} | ConvertTo-Json -Depth 10

try {
    $response1 = Invoke-RestMethod -Uri $apiUrl -Method POST -Body ([System.Text.Encoding]::UTF8.GetBytes($body1)) -ContentType "application/json; charset=utf-8"
    Write-Host "Success: $($response1.message)" -ForegroundColor Green
    Write-Host "Response: $($response1 | ConvertTo-Json)" -ForegroundColor Gray
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host "Error Details: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Start-Sleep -Seconds 2

# Test 2: Card Message with Green (Success) Color
Write-Host "Test 2: Sending card message (Success - Green)..." -ForegroundColor Green
$body2 = @{
    title = "System Status"
    message = "**All systems operational** - OK`n`nLast checked: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    message_type = "card"
    color = "00FF00"
} | ConvertTo-Json -Depth 10

try {
    $response2 = Invoke-RestMethod -Uri $apiUrl -Method POST -Body ([System.Text.Encoding]::UTF8.GetBytes($body2)) -ContentType "application/json; charset=utf-8"
    Write-Host "Success: $($response2.message)" -ForegroundColor Green
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host "Error Details: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Start-Sleep -Seconds 2

# Test 3: Card Message with Yellow (Warning) Color
Write-Host "Test 3: Sending card message (Warning - Yellow)..." -ForegroundColor Yellow
$body3 = @{
    title = "Warning Alert"
    message = "**Disk space low**`n`nCurrent usage: 85%`nAction required: Clean up old files"
    message_type = "card"
    color = "FFCC00"
} | ConvertTo-Json -Depth 10

try {
    $response3 = Invoke-RestMethod -Uri $apiUrl -Method POST -Body ([System.Text.Encoding]::UTF8.GetBytes($body3)) -ContentType "application/json; charset=utf-8"
    Write-Host "Success: $($response3.message)" -ForegroundColor Green
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host "Error Details: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Start-Sleep -Seconds 2

# Test 4: Card Message with Red (Error) Color
Write-Host "Test 4: Sending card message (Error - Red)..." -ForegroundColor Red
$body4 = @{
    title = "Error Alert"
    message = "**Database connection failed**`n`nError: Connection timeout`nRetrying in 30 seconds..."
    message_type = "card"
    color = "FF0000"
} | ConvertTo-Json -Depth 10

try {
    $response4 = Invoke-RestMethod -Uri $apiUrl -Method POST -Body ([System.Text.Encoding]::UTF8.GetBytes($body4)) -ContentType "application/json; charset=utf-8"
    Write-Host "Success: $($response4.message)" -ForegroundColor Green
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host "Error Details: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Start-Sleep -Seconds 2

# Test 5: Formatted Card with Multiple Sections
Write-Host "Test 5: Sending formatted report card..." -ForegroundColor Cyan
$reportMessage = @"
## Daily Report

**Orders Processed**: 150
**Revenue**: `$25,430.50
**New Customers**: 12

---

### Top Products
1. Widget A - 45 units
2. Gadget B - 32 units
3. Tool C - 28 units

---
_Report generated at $(Get-Date -Format 'HH:mm:ss')_
"@

$body5 = @{
    title = "Daily Business Report"
    message = $reportMessage
    message_type = "card"
    color = "0076D7"
} | ConvertTo-Json -Depth 10

try {
    $response5 = Invoke-RestMethod -Uri $apiUrl -Method POST -Body ([System.Text.Encoding]::UTF8.GetBytes($body5)) -ContentType "application/json; charset=utf-8"
    Write-Host "Success: $($response5.message)" -ForegroundColor Green
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host "Error Details: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== All Tests Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Check your Teams channel 'NewAPI Team' for the messages!" -ForegroundColor Yellow
Write-Host ""

# Option to test with custom webhook
Write-Host "Would you like to test with a different webhook URL? (y/n)" -ForegroundColor Cyan
$testCustom = Read-Host
if ($testCustom -eq 'y') {
    $customWebhook = Read-Host "Enter custom webhook URL"
    
    Write-Host "Sending test message to custom webhook..." -ForegroundColor Green
    $customBody = @{
        message = "Test message to custom webhook"
        webhook_url = $customWebhook
    } | ConvertTo-Json
    
    try {
        $customResponse = Invoke-RestMethod -Uri $apiUrl -Method POST -Body $customBody -ContentType "application/json"
        Write-Host "✅ Success: $($customResponse.message)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Error: $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "For more examples, see: docs/TEAMS_API_SETUP.md" -ForegroundColor Gray
