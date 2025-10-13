# PowerShell script to generate self-signed SSL certificate for Flask HTTPS
# Run this script once to create certificates for development

param(
    [string]$Domain = "localhost",
    [int]$Days = 365
)

Write-Host "🔐 Generating self-signed SSL certificate for Flask HTTPS..." -ForegroundColor Green

# Create SSL directory if it doesn't exist
$sslDir = "security\ssl"
if (!(Test-Path $sslDir)) {
    New-Item -ItemType Directory -Path $sslDir -Force
    Write-Host "📁 Created SSL directory: $sslDir" -ForegroundColor Cyan
}

# Certificate paths
$certPath = "$sslDir\server.crt"
$keyPath = "$sslDir\server.key"
$pfxPath = "$sslDir\server.pfx"

try {
    # Create certificate using New-SelfSignedCertificate (Windows PowerShell 5.1+)
    $cert = New-SelfSignedCertificate `
        -Subject "CN=$Domain" `
        -DnsName $Domain, "127.0.0.1", "0.0.0.0" `
        -KeyLength 2048 `
        -KeyAlgorithm RSA `
        -KeyExportPolicy Exportable `
        -KeyUsage DigitalSignature, KeyEncipherment `
        -NotAfter (Get-Date).AddDays($Days) `
        -CertStoreLocation Cert:\CurrentUser\My `
        -Provider "Microsoft Enhanced RSA and AES Cryptographic Provider"
    
    Write-Host "✅ Certificate created in Windows Certificate Store" -ForegroundColor Green
    
    # Export to PFX (includes private key)
    $password = ConvertTo-SecureString -String "flask-dev-cert" -Force -AsPlainText
    Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $password
    
    # Export certificate to PEM format
    $certContent = "-----BEGIN CERTIFICATE-----`n"
    $certContent += [System.Convert]::ToBase64String($cert.RawData, [System.Base64FormattingOptions]::InsertLineBreaks)
    $certContent += "`n-----END CERTIFICATE-----"
    $certContent | Out-File -FilePath $certPath -Encoding ascii
    
    # Export private key (requires more complex handling)
    Write-Host "📝 Certificate exported to: $certPath" -ForegroundColor Cyan
    Write-Host "📦 PFX file created at: $pfxPath (password: flask-dev-cert)" -ForegroundColor Cyan
    
    Write-Host "`n🎉 SSL certificate generation completed!" -ForegroundColor Green
    Write-Host "Valid for domains: $Domain, 127.0.0.1, 0.0.0.0" -ForegroundColor Yellow
    Write-Host "Certificate expires: $((Get-Date).AddDays($Days).ToString('yyyy-MM-dd'))" -ForegroundColor Yellow
    
    Write-Host "`n🚀 To use HTTPS with Flask:" -ForegroundColor Magenta
    Write-Host "1. Set environment variable: `$env:FLASK_SSL_CERT = '$certPath'" -ForegroundColor White
    Write-Host "2. Set environment variable: `$env:FLASK_SSL_KEY = '$keyPath'" -ForegroundColor White
    Write-Host "3. Or use PFX file: `$env:FLASK_SSL_PFX = '$pfxPath'" -ForegroundColor White
    Write-Host "4. Start your Flask app - it will automatically use HTTPS" -ForegroundColor White
    
    Write-Host "`n⚠️  Browser Security Notice:" -ForegroundColor Red
    Write-Host "Your browser will show a security warning for self-signed certificates." -ForegroundColor Yellow
    Write-Host "Click 'Advanced' -> 'Proceed to localhost (unsafe)' to continue." -ForegroundColor Yellow
    
    # Clean up certificate from store (optional)
    # Remove-Item -Path "Cert:\CurrentUser\My\$($cert.Thumbprint)" -Force
    
} catch {
    Write-Host "❌ Error generating certificate: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Try running PowerShell as Administrator" -ForegroundColor Yellow
}