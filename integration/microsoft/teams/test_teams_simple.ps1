# Simple Teams API Test (No Emojis, UTF-8 Safe)
# Usage: .\test_teams_simple.ps1

Write-Host "Simple Teams API Test" -ForegroundColor Cyan
Write-Host ""

# SSL bypass for self-signed certs
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

# Configuration
$apiUrl = "https://devvm01.nyc.ou.org:5656/teams/send_message"

Write-Host "Sending test message..." -ForegroundColor Green

$body = @{
    title = "Test Message"
    message = "Hello from API Logic Server! This is a test message at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    message_type = "card"
    color = "0076D7"
} | ConvertTo-Json -Depth 10

try {
    # Convert to UTF-8 bytes to avoid encoding issues
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    
    $response = Invoke-RestMethod -Uri $apiUrl -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8"
    
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "Status: $($response.status)" -ForegroundColor Gray
    Write-Host "Message: $($response.message)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Check your Teams channel for the message!" -ForegroundColor Yellow
}
catch {
    Write-Host "FAILED!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    # Try to parse error response
    if ($_.ErrorDetails) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Cyan
