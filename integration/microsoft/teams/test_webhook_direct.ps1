# Direct test to Power Automate webhook
# This tests the webhook directly without going through the API

Write-Host "Testing Power Automate Webhook Directly" -ForegroundColor Cyan
Write-Host ""

# SSL bypass
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

$webhookUrl = $env:TEAMS_WEBHOOK_URL

if (-not $webhookUrl) {
    Write-Host "ERROR: TEAMS_WEBHOOK_URL environment variable not set" -ForegroundColor Red
    exit 1
}

Write-Host "Webhook URL: $($webhookUrl.Substring(0, 80))..." -ForegroundColor Gray
Write-Host ""

# Test 1: Simple payload
Write-Host "Test 1: Simple text payload..." -ForegroundColor Green
$simpleBody = @{
    text = "Hello from PowerShell! Test at $(Get-Date -Format 'HH:mm:ss')"
    title = "Test Message"
} | ConvertTo-Json

try {
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($simpleBody)
    $response = Invoke-RestMethod -Uri $webhookUrl -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8"
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "Response: $response" -ForegroundColor Gray
}
catch {
    Write-Host "FAILED!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Start-Sleep -Seconds 2

# Test 2: Card-style payload
Write-Host "Test 2: Card-style payload..." -ForegroundColor Green
$cardBody = @{
    title = "System Status"
    text = "All systems operational - OK"
    color = "00FF00"
} | ConvertTo-Json

try {
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($cardBody)
    $response = Invoke-RestMethod -Uri $webhookUrl -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8"
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "Response: $response" -ForegroundColor Gray
}
catch {
    Write-Host "FAILED!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Done! Check your Teams channel." -ForegroundColor Cyan
