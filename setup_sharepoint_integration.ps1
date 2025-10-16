# SharePoint Integration Setup Script
# Run this to integrate SharePoint document management with your API Logic Server

Write-Host "📚 SharePoint Integration Setup for API Logic Server" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan

Write-Host "`n📋 Setup Steps:" -ForegroundColor Yellow

Write-Host "`n1️⃣ Azure App Registration Required" -ForegroundColor Magenta
Write-Host "   • Go to: https://portal.azure.com" -ForegroundColor White
Write-Host "   • Azure Active Directory → App registrations → New registration" -ForegroundColor White
Write-Host "   • Name: YourApp-SharePoint-Integration" -ForegroundColor White
Write-Host "   • Redirect URI: http://localhost:5656/sharepoint/callback" -ForegroundColor White
Write-Host "   • Note down: Application (client) ID and Directory (tenant) ID" -ForegroundColor White
Write-Host "   • Create client secret under 'Certificates & secrets'" -ForegroundColor White

Write-Host "`n2️⃣ API Permissions Setup" -ForegroundColor Magenta
Write-Host "   • Go to 'API permissions' in your Azure app" -ForegroundColor White
Write-Host "   • Add permission → Microsoft Graph → Delegated permissions" -ForegroundColor White
Write-Host "   • Select:" -ForegroundColor White
Write-Host "     ✓ Sites.ReadWrite.All" -ForegroundColor Green
Write-Host "     ✓ Files.ReadWrite.All" -ForegroundColor Green
Write-Host "     ✓ offline_access" -ForegroundColor Green
Write-Host "   • Click 'Grant admin consent'" -ForegroundColor White

Write-Host "`n3️⃣ SharePoint Site Information" -ForegroundColor Magenta
Write-Host "   • Identify your SharePoint site URL:" -ForegroundColor White
Write-Host "     Example: https://contoso.sharepoint.com/sites/documents" -ForegroundColor Cyan
Write-Host "   • Find your tenant domain (first part of the URL)" -ForegroundColor White
Write-Host "   • Note the site path (/sites/documents)" -ForegroundColor White

Write-Host "`n4️⃣ Set Environment Variables" -ForegroundColor Magenta
Write-Host "   Replace these with your actual values:" -ForegroundColor White

# Set example environment variables (user needs to replace)
$env:SHAREPOINT_TENANT_ID = "your-azure-tenant-id-here"
$env:SHAREPOINT_CLIENT_ID = "your-azure-client-id-here"
$env:SHAREPOINT_CLIENT_SECRET = "your-azure-client-secret-here"
$env:SHAREPOINT_SITE_URL = "https://yourtenant.sharepoint.com/sites/yoursite"
$env:SHAREPOINT_REDIRECT_URI = "http://localhost:5656/sharepoint/callback"

Write-Host "   `$env:SHAREPOINT_TENANT_ID = '$env:SHAREPOINT_TENANT_ID'" -ForegroundColor Yellow
Write-Host "   `$env:SHAREPOINT_CLIENT_ID = '$env:SHAREPOINT_CLIENT_ID'" -ForegroundColor Yellow  
Write-Host "   `$env:SHAREPOINT_CLIENT_SECRET = '$env:SHAREPOINT_CLIENT_SECRET'" -ForegroundColor Yellow
Write-Host "   `$env:SHAREPOINT_SITE_URL = '$env:SHAREPOINT_SITE_URL'" -ForegroundColor Yellow
Write-Host "   `$env:SHAREPOINT_REDIRECT_URI = '$env:SHAREPOINT_REDIRECT_URI'" -ForegroundColor Yellow

Write-Host "`n5️⃣ Available Endpoints" -ForegroundColor Magenta
Write-Host "   After integration, you'll have:" -ForegroundColor White
Write-Host "   • GET  /sharepoint              - Web interface" -ForegroundColor Cyan
Write-Host "   • GET  /sharepoint/auth         - Start OAuth flow" -ForegroundColor Cyan
Write-Host "   • GET  /sharepoint/callback     - OAuth callback" -ForegroundColor Cyan  
Write-Host "   • GET  /sharepoint/libraries    - List document libraries" -ForegroundColor Cyan
Write-Host "   • GET  /sharepoint/files        - List files" -ForegroundColor Cyan
Write-Host "   • POST /sharepoint/upload       - Upload files" -ForegroundColor Cyan
Write-Host "   • GET  /sharepoint/download/<id> - Download files" -ForegroundColor Cyan
Write-Host "   • GET  /sharepoint/share/<id>   - Create share links" -ForegroundColor Cyan
Write-Host "   • POST /sharepoint/folder       - Create folders" -ForegroundColor Cyan
Write-Host "   • GET  /sharepoint/search       - Search documents" -ForegroundColor Cyan
Write-Host "   • GET  /sharepoint/versions/<id> - File versions" -ForegroundColor Cyan

Write-Host "`n6️⃣ Usage Example" -ForegroundColor Magenta
Write-Host "   # 1. Authenticate" -ForegroundColor White
Write-Host "   GET http://localhost:5656/sharepoint/auth" -ForegroundColor Cyan
Write-Host "   # Follow the auth_url, complete OAuth" -ForegroundColor White
Write-Host ""
Write-Host "   # 2. List document libraries" -ForegroundColor White  
Write-Host "   GET http://localhost:5656/sharepoint/libraries" -ForegroundColor Cyan
Write-Host ""
Write-Host "   # 3. List files in Documents library" -ForegroundColor White  
Write-Host "   GET http://localhost:5656/sharepoint/files?library=Documents" -ForegroundColor Cyan
Write-Host ""
Write-Host "   # 4. Upload file" -ForegroundColor White
Write-Host "   POST http://localhost:5656/sharepoint/upload" -ForegroundColor Cyan
Write-Host "   Content-Type: multipart/form-data" -ForegroundColor Gray
Write-Host "   file: <file_data>" -ForegroundColor Gray
Write-Host "   library: Documents" -ForegroundColor Gray
Write-Host "   folder: /Contracts" -ForegroundColor Gray
Write-Host ""
Write-Host "   # 5. Search documents" -ForegroundColor White
Write-Host "   GET http://localhost:5656/sharepoint/search?q=contract&library=Documents" -ForegroundColor Cyan

Write-Host "`n🚀 Quick Test Commands" -ForegroundColor Magenta
Write-Host "   After setting up Azure app and environment variables:" -ForegroundColor White
Write-Host ""
Write-Host "   # Test authentication" -ForegroundColor White
Write-Host "   Invoke-RestMethod -Uri 'http://localhost:5656/sharepoint/auth' -Method GET" -ForegroundColor Cyan
Write-Host ""
Write-Host "   # Test site info (after auth)" -ForegroundColor White  
Write-Host "   Invoke-RestMethod -Uri 'http://localhost:5656/sharepoint/site' -Method GET" -ForegroundColor Cyan

Write-Host "`n⚠️ Security & Enterprise Features" -ForegroundColor Red
Write-Host "   • Use HTTPS in production" -ForegroundColor White
Write-Host "   • Store client secrets securely (Azure Key Vault)" -ForegroundColor White  
Write-Host "   • Implement proper session management" -ForegroundColor White
Write-Host "   • Version control and audit trails available" -ForegroundColor White
Write-Host "   • Enterprise permissions and compliance" -ForegroundColor White
Write-Host "   • Integration with Microsoft 365 apps" -ForegroundColor White

Write-Host "`n✅ SharePoint vs OneDrive Benefits" -ForegroundColor Green
Write-Host "   • Enterprise document libraries" -ForegroundColor White
Write-Host "   • Advanced permissions and governance" -ForegroundColor White
Write-Host "   • Version history and check-in/check-out" -ForegroundColor White
Write-Host "   • Metadata and content types" -ForegroundColor White
Write-Host "   • Workflow automation integration" -ForegroundColor White
Write-Host "   • Compliance and retention policies" -ForegroundColor White
Write-Host "   • Team collaboration features" -ForegroundColor White

Write-Host "`n💡 Required Dependencies" -ForegroundColor Magenta
Write-Host "   Install required Python packages:" -ForegroundColor White
Write-Host "   pip install msal requests" -ForegroundColor Cyan

if ($env:SHAREPOINT_CLIENT_ID -eq "your-azure-client-id-here") {
    Write-Host "`n🔴 REMEMBER: Update the environment variables with your real Azure app values!" -ForegroundColor Red
    Write-Host "   And set your actual SharePoint site URL!" -ForegroundColor Red
} else {
    Write-Host "`n✅ Environment variables appear to be configured" -ForegroundColor Green
}

Write-Host "`n🌐 Access SharePoint Manager at:" -ForegroundColor Magenta
Write-Host "   http://localhost:5656/sharepoint" -ForegroundColor Cyan

Write-Host "`nDone! 🎉" -ForegroundColor Green