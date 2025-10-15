# 🗂️ OneDrive Shared Folder Integration - Complete Setup Guide

## 📋 Overview

You now have a complete OneDrive integration with your API Logic Server that provides:

- **Web-based file manager** at `http://localhost:5656/onedrive`
- **RESTful API endpoints** for programmatic access
- **OAuth2 authentication** with Microsoft Graph API
- **File upload/download** capabilities
- **Share link generation** for easy file sharing
- **Folder management** with navigation

## 🚀 Quick Start

### 1. Azure App Registration (Required)

**Go to Azure Portal:**
1. Visit [portal.azure.com](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**

**App Settings:**
```
Name: YourApp-OneDrive-Integration
Redirect URI: http://localhost:5656/onedrive/callback
Account types: Accounts in any organizational directory and personal Microsoft accounts
```

**Get Required Information:**
- Application (client) ID: `abc12345-def6-7890-ghij-klmnopqrstuv`
- Directory (tenant) ID: `def67890-abc1-2345-fghi-jklmnopqrstuv`

**Create Client Secret:**
1. Go to **Certificates & secrets** → **New client secret**
2. Copy the secret value (you can only see it once!)

**Set API Permissions:**
1. Go to **API permissions** → **Add a permission**
2. Select **Microsoft Graph** → **Delegated permissions**
3. Add these permissions:
   - ✅ `Files.ReadWrite`
   - ✅ `Files.ReadWrite.All`
   - ✅ `Sites.ReadWrite.All`
   - ✅ `offline_access`
4. Click **Grant admin consent**

### 2. Environment Setup

**Run the setup script:**
```powershell
# Navigate to your project
cd c:\OUProjects\oukash5

# Run the setup script to see instructions
.\setup_onedrive_integration.ps1
```

**Set your real environment variables:**
```powershell
# Replace with YOUR actual values from Azure
$env:ONEDRIVE_CLIENT_ID = "abc12345-def6-7890-ghij-klmnopqrstuv"
$env:ONEDRIVE_CLIENT_SECRET = "your-client-secret-from-azure"  
$env:ONEDRIVE_TENANT_ID = "def67890-abc1-2345-fghi-jklmnopqrstuv"
$env:ONEDRIVE_REDIRECT_URI = "http://localhost:5656/onedrive/callback"
```

### 3. Start Your Server

```powershell
# Start API Logic Server (OneDrive integration is already added)
python api_logic_server_run.py
```

You should see:
```
✅ OneDrive integration endpoints added
   • GET  /onedrive/auth           - Start OAuth flow
   • GET  /onedrive/callback       - OAuth callback
   • GET  /onedrive/files          - List files
   • POST /onedrive/upload         - Upload files
   • GET  /onedrive/download/<id>  - Download files
   • GET  /onedrive/share/<id>     - Create share links
   • POST /onedrive/folder         - Create folders
```

### 4. Access the OneDrive Manager

**Open in your browser:**
```
http://localhost:5656/onedrive
```

**First-time setup:**
1. Click **"Connect to OneDrive"**
2. Complete Microsoft OAuth flow
3. Grant permissions to your app
4. Return to the file manager

## 🖥️ Web Interface Features

### File Manager Interface
- **Drag & drop file uploads**
- **File browser with navigation**
- **Download files directly**
- **Create share links**
- **Folder creation and navigation**
- **Breadcrumb navigation**

### Authentication Status
- Visual indicator of connection status
- One-click connect/disconnect
- Automatic token refresh

### File Operations
- **Upload**: Drag files or click to select
- **Download**: One-click download to your computer
- **Share**: Generate shareable links with view/edit permissions
- **Navigate**: Browse folders like a file explorer

## 🔗 API Endpoints

### Authentication
```http
GET /onedrive/auth
```
Returns: `{"auth_url": "https://login.microsoftonline.com/..."}`

### File Management
```http
# List files in a folder
GET /onedrive/files?path=/Documents

# Upload a file
POST /onedrive/upload
Content-Type: multipart/form-data
{
  "file": <file_data>,
  "folder": "/Documents"
}

# Download a file
GET /onedrive/download/{file_id}

# Create share link
GET /onedrive/share/{file_id}?type=view&scope=anonymous

# Create folder
POST /onedrive/folder
Content-Type: application/json
{
  "name": "New Folder",
  "parent_path": "/Documents"
}
```

## 📝 Usage Examples

### PowerShell Examples
```powershell
# Get authentication URL
$auth = Invoke-RestMethod -Uri "http://localhost:5656/onedrive/auth"
Write-Host "Visit: $($auth.auth_url)"

# List files (after authentication)
$files = Invoke-RestMethod -Uri "http://localhost:5656/onedrive/files"
$files.files | ForEach-Object { Write-Host $_.name }

# Create a share link
$share = Invoke-RestMethod -Uri "http://localhost:5656/onedrive/share/ABC123?type=view"
Write-Host "Share link: $($share.share_link)"
```

### JavaScript Examples
```javascript
// Upload file via fetch
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('folder', '/Documents');

fetch('/onedrive/upload', {
    method: 'POST',
    body: formData
}).then(response => response.json())
  .then(data => console.log('Upload result:', data));

// List files
fetch('/onedrive/files?path=/Documents')
    .then(response => response.json())
    .then(data => console.log('Files:', data.files));
```

## 🔐 Security & Best Practices

### Production Considerations
- **Use HTTPS** in production environments
- **Secure client secrets** using environment variables or Azure Key Vault
- **Implement rate limiting** to prevent API abuse
- **Validate file types** and sizes before upload
- **Set appropriate permissions** (view vs edit)

### Environment Variables
```bash
# For production, use these environment variables
ONEDRIVE_CLIENT_ID=your-prod-client-id
ONEDRIVE_CLIENT_SECRET=your-prod-client-secret
ONEDRIVE_TENANT_ID=your-tenant-id
ONEDRIVE_REDIRECT_URI=https://yourdomain.com/onedrive/callback
```

### File Validation
```python
# Example: Restrict file types and sizes
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.xlsx', '.png', '.jpg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(file):
    if file.content_length > MAX_FILE_SIZE:
        raise ValueError("File too large")
    
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("File type not allowed")
```

## 🧪 Testing

### Manual Testing
1. **Authentication**: Visit `/onedrive/auth` and complete OAuth flow
2. **File Upload**: Use the web interface to upload a test file
3. **File Download**: Download the uploaded file
4. **Share Link**: Create and test a share link
5. **Folder Operations**: Create and navigate folders

### API Testing with Postman
```json
{
  "name": "OneDrive Integration Tests",
  "requests": [
    {
      "name": "Get Auth URL",
      "method": "GET",
      "url": "http://localhost:5656/onedrive/auth"
    },
    {
      "name": "List Files",
      "method": "GET", 
      "url": "http://localhost:5656/onedrive/files"
    },
    {
      "name": "Upload File",
      "method": "POST",
      "url": "http://localhost:5656/onedrive/upload",
      "body": {
        "type": "form-data",
        "formdata": [
          {"key": "file", "type": "file"},
          {"key": "folder", "value": "/"}
        ]
      }
    }
  ]
}
```

## 🆘 Troubleshooting

### Common Issues

**1. Authentication Failures**
```
Error: "Invalid client" or 403 Forbidden
```
**Solution**: Verify client ID, secret, and redirect URI match Azure app registration exactly

**2. Permission Denied**
```
Error: "Insufficient privileges to complete the operation"
```
**Solution**: Grant admin consent for API permissions in Azure portal

**3. Token Expired**
```
Error: 401 Unauthorized
```
**Solution**: The service automatically refreshes tokens, but you may need to re-authenticate

**4. File Upload Issues**
```
Error: "Upload failed"
```
**Solution**: Check file size limits, network connection, and OneDrive storage quota

### Debug Mode
Enable debug logging in your API Logic Server:
```python
import logging
logging.getLogger('integration.onedrive_service').setLevel(logging.DEBUG)
```

### Health Check Endpoint
Test if OneDrive service is working:
```http
GET /onedrive/files
```
Should return file list if authenticated, or authentication error if not.

## 🎯 Next Steps

### Integration with Your Business Logic
```python
# Example: Automatically upload reports to OneDrive
from integration.onedrive_service import onedrive_service

def save_report_to_onedrive(report_data, filename):
    """Save generated report to OneDrive"""
    try:
        result = onedrive_service.upload_file(
            f"/Reports/{filename}",
            report_data,
            "application/pdf"
        )
        
        if result:
            # Create share link for easy access
            share_link = onedrive_service.create_share_link(
                result['id'], 
                link_type='view'
            )
            return share_link
        
    except Exception as e:
        logger.error(f"Failed to save report: {e}")
        return None
```

### Custom UI Integration
Add OneDrive functionality to your existing admin interface:
```javascript
// Add to your existing admin UI
function addOneDriveButton() {
    const button = document.createElement('button');
    button.textContent = '📁 OneDrive Files';
    button.onclick = () => window.open('/onedrive', '_blank');
    document.querySelector('.toolbar').appendChild(button);
}
```

## ✅ Summary

You now have:
- ✅ Complete OneDrive integration with API Logic Server
- ✅ Web-based file manager interface
- ✅ RESTful API endpoints for programmatic access
- ✅ OAuth2 authentication with automatic token refresh
- ✅ File upload, download, and sharing capabilities
- ✅ Folder management and navigation
- ✅ Production-ready security considerations

**Access your OneDrive manager at:** `http://localhost:5656/onedrive`

Happy file sharing! 🎉