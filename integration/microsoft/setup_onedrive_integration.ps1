# OneDrive Integration Setup Script
# Run this to integrate OneDrive file sharing with your API Logic Server

Write-Host "🗂️ OneDrive Integration Setup for API Logic Server" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Cyan

Write-Host "`n📋 Setup Steps:" -ForegroundColor Yellow

Write-Host "`n1️⃣ Azure App Registration Required" -ForegroundColor Magenta
Write-Host "   • Go to: https://portal.azure.com" -ForegroundColor White
Write-Host "   • Azure Active Directory → App registrations → New registration" -ForegroundColor White
Write-Host "   • Name: YourApp-OneDrive-Integration" -ForegroundColor White
Write-Host "   • Redirect URI: http://192.168.13.31:5656/onedrive/callback" -ForegroundColor White
Write-Host "   • Note down: Application (client) ID and Directory (tenant) ID" -ForegroundColor White
Write-Host "   • Create client secret under 'Certificates & secrets'" -ForegroundColor White

Write-Host "`n2️⃣ API Permissions Setup" -ForegroundColor Magenta
Write-Host "   • Go to 'API permissions' in your Azure app" -ForegroundColor White
Write-Host "   • Add permission → Microsoft Graph → Delegated permissions" -ForegroundColor White
Write-Host "   • Select:" -ForegroundColor White
Write-Host "     ✓ Files.ReadWrite" -ForegroundColor Green
Write-Host "     ✓ Files.ReadWrite.All" -ForegroundColor Green
Write-Host "     ✓ Sites.ReadWrite.All" -ForegroundColor Green
Write-Host "     ✓ offline_access" -ForegroundColor Green
Write-Host "   • Click 'Grant admin consent'" -ForegroundColor White

Write-Host "`n3️⃣ Set Environment Variables" -ForegroundColor Magenta
Write-Host "   Replace these with your actual values:" -ForegroundColor White

# Set example environment variables (user needs to replace)
$env:ONEDRIVE_CLIENT_ID = "your-azure-client-id-here"
$env:ONEDRIVE_CLIENT_SECRET = "your-azure-client-secret-here"  
$env:ONEDRIVE_TENANT_ID = "your-azure-tenant-id-here"
$env:ONEDRIVE_REDIRECT_URI = "http://192.168.13.31:5656/onedrive/callback"

Write-Host "   `$env:ONEDRIVE_CLIENT_ID = '$env:ONEDRIVE_CLIENT_ID'" -ForegroundColor Yellow
Write-Host "   `$env:ONEDRIVE_CLIENT_SECRET = '$env:ONEDRIVE_CLIENT_SECRET'" -ForegroundColor Yellow  
Write-Host "   `$env:ONEDRIVE_TENANT_ID = '$env:ONEDRIVE_TENANT_ID'" -ForegroundColor Yellow
Write-Host "   `$env:ONEDRIVE_REDIRECT_URI = '$env:ONEDRIVE_REDIRECT_URI'" -ForegroundColor Yellow

Write-Host "`n4️⃣ Integration with API Logic Server" -ForegroundColor Magenta
Write-Host "   • OneDrive service created at: integration/onedrive_service.py" -ForegroundColor Green
Write-Host "   • Add to your api_logic_server_run.py:" -ForegroundColor White
Write-Host "     from integration.onedrive_service import add_onedrive_endpoints" -ForegroundColor Cyan
Write-Host "     add_onedrive_endpoints(app)" -ForegroundColor Cyan

Write-Host "`n5️⃣ Available Endpoints" -ForegroundColor Magenta
Write-Host "   After integration, you'll have:" -ForegroundColor White
Write-Host "   • GET  /onedrive/auth           - Start OAuth flow" -ForegroundColor Cyan
Write-Host "   • GET  /onedrive/callback       - OAuth callback" -ForegroundColor Cyan  
Write-Host "   • GET  /onedrive/files          - List files" -ForegroundColor Cyan
Write-Host "   • POST /onedrive/upload         - Upload files" -ForegroundColor Cyan
Write-Host "   • GET  /onedrive/download/<id>  - Download files" -ForegroundColor Cyan
Write-Host "   • GET  /onedrive/share/<id>     - Create share links" -ForegroundColor Cyan
Write-Host "   • POST /onedrive/folder         - Create folders" -ForegroundColor Cyan

Write-Host "`n6️⃣ Usage Example" -ForegroundColor Magenta
Write-Host "   # 1. Authenticate" -ForegroundColor White
Write-Host "   GET http://192.168.13.31:5656/onedrive/auth" -ForegroundColor Cyan
Write-Host "   # Follow the auth_url, complete OAuth" -ForegroundColor White
Write-Host ""
Write-Host "   # 2. List files" -ForegroundColor White  
Write-Host "   GET http://192.168.13.31:5656/onedrive/files" -ForegroundColor Cyan
Write-Host ""
Write-Host "   # 3. Upload file" -ForegroundColor White
Write-Host "   POST http://192.168.13.31:5656/onedrive/upload" -ForegroundColor Cyan
Write-Host "   Content-Type: multipart/form-data" -ForegroundColor Gray
Write-Host "   file: <file_data>" -ForegroundColor Gray
Write-Host "   folder: /Documents" -ForegroundColor Gray
Write-Host ""
Write-Host "   # 4. Create share link" -ForegroundColor White
Write-Host "   GET http://192.168.13.31:5656/onedrive/share/{file_id}?type=view" -ForegroundColor Cyan

Write-Host "`n🚀 Quick Test Commands" -ForegroundColor Magenta
Write-Host "   After setting up Azure app and environment variables:" -ForegroundColor White
Write-Host ""
Write-Host "   # Test authentication" -ForegroundColor White
Write-Host "   Invoke-RestMethod -Uri 'http://192.168.13.31:5656/onedrive/auth' -Method GET" -ForegroundColor Cyan
Write-Host ""
Write-Host "   # Test file listing (after auth)" -ForegroundColor White  
Write-Host "   Invoke-RestMethod -Uri 'http://192.168.13.31:5656/onedrive/files' -Method GET" -ForegroundColor Cyan

Write-Host "`n⚠️ Security Notes" -ForegroundColor Red
Write-Host "   • Use HTTPS in production" -ForegroundColor White
Write-Host "   • Store client secrets securely" -ForegroundColor White  
Write-Host "   • Implement proper session management" -ForegroundColor White
Write-Host "   • Validate file types and sizes" -ForegroundColor White
Write-Host "   • Set appropriate permission scopes" -ForegroundColor White

Write-Host "`n✅ Integration Benefits" -ForegroundColor Green
Write-Host "   • Seamless file sharing with OneDrive" -ForegroundColor White
Write-Host "   • RESTful API endpoints" -ForegroundColor White
Write-Host "   • Automatic authentication handling" -ForegroundColor White
Write-Host "   • Share link generation" -ForegroundColor White
Write-Host "   • Full CRUD operations on files/folders" -ForegroundColor White

if ($env:ONEDRIVE_CLIENT_ID -eq "your-azure-client-id-here") {
    Write-Host "`n🔴 REMEMBER: Update the environment variables with your real Azure app values!" -ForegroundColor Red
} else {
    Write-Host "`n✅ Environment variables appear to be configured" -ForegroundColor Green
}

Write-Host "`nDone! 🎉" -ForegroundColor Green