# PowerShell script to decode JWT token and show expiration
param(
    [Parameter(Mandatory=$true)]
    [string]$Token
)

function Decode-JWTToken {
    param($token)
    
    # Split the token into parts
    $parts = $token.Split('.')
    if ($parts.Length -ne 3) {
        throw "Invalid JWT token format"
    }
    
    # Decode the payload (second part)
    $payload = $parts[1]
    
    # Add padding if needed for base64 decoding
    while ($payload.Length % 4 -ne 0) {
        $payload += "="
    }
    
    # Replace URL-safe base64 characters
    $payload = $payload.Replace('-', '+').Replace('_', '/')
    
    # Decode from base64
    $bytes = [Convert]::FromBase64String($payload)
    $json = [System.Text.Encoding]::UTF8.GetString($bytes)
    
    return $json | ConvertFrom-Json
}

try {
    $decoded = Decode-JWTToken -token $Token
    
    Write-Host "JWT Token Information:" -ForegroundColor Green
    Write-Host "Subject (sub): $($decoded.sub)" -ForegroundColor Cyan
    Write-Host "Issued At (iat): $($decoded.iat)" -ForegroundColor Cyan
    Write-Host "Expires (exp): $($decoded.exp)" -ForegroundColor Cyan
    Write-Host "Not Before (nbf): $($decoded.nbf)" -ForegroundColor Cyan
    Write-Host "Token Type: $($decoded.type)" -ForegroundColor Cyan
    Write-Host ""
    
    # Convert Unix timestamps to readable dates
    $issuedAt = [DateTimeOffset]::FromUnixTimeSeconds($decoded.iat).DateTime
    $expiresAt = [DateTimeOffset]::FromUnixTimeSeconds($decoded.exp).DateTime
    $notBefore = [DateTimeOffset]::FromUnixTimeSeconds($decoded.nbf).DateTime
    
    Write-Host "Readable Timestamps:" -ForegroundColor Yellow
    Write-Host "Issued At: $issuedAt" -ForegroundColor White
    Write-Host "Expires At: $expiresAt" -ForegroundColor White
    Write-Host "Not Before: $notBefore" -ForegroundColor White
    Write-Host ""
    
    # Check if token is expired
    $now = Get-Date
    if ($now -gt $expiresAt) {
        Write-Host "⚠️  TOKEN IS EXPIRED!" -ForegroundColor Red
    } else {
        $timeLeft = $expiresAt - $now
        Write-Host "✅ Token is valid for: $($timeLeft.Hours)h $($timeLeft.Minutes)m $($timeLeft.Seconds)s" -ForegroundColor Green
    }
    
} catch {
    Write-Host "Error decoding token: $($_.Exception.Message)" -ForegroundColor Red
}