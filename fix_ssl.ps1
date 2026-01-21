# Quick SSL Fix for PowerShell Invoke-RestMethod
# Run this before making HTTPS requests to servers with self-signed certificates
# Usage: . .\fix_ssl.ps1

Write-Host "Configuring SSL certificate bypass..." -ForegroundColor Yellow

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

Write-Host "✅ SSL certificate validation bypassed" -ForegroundColor Green
Write-Host "✅ TLS 1.2 enabled" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run: .\test_teams_api.ps1" -ForegroundColor Cyan
