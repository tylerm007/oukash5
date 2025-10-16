# 📚 SharePoint Integration - Complete Setup Guide

## 🎯 Overview

SharePoint integration provides **enterprise-grade document management** with advanced features like:

- **Document Libraries** with metadata and content types
- **Version Control** and check-in/check-out capabilities  
- **Enterprise Permissions** and governance
- **Advanced Search** across all documents
- **Workflow Integration** with Microsoft 365
- **Compliance** and retention policies

## 🚀 Quick Start

### 1. Install Required Dependencies

```powershell
# Install Microsoft Authentication Library
pip install msal requests
```

### 2. Azure App Registration

**Create Azure App:**
1. Go to [portal.azure.com](https://portal.azure.com)
2. **Azure Active Directory** → **App registrations** → **New registration**
3. **Name**: YourApp-SharePoint-Integration
4. **Redirect URI**: `http://localhost:5656/sharepoint/callback`
5. **Account types**: Accounts in this organizational directory only

**Get Required Information:**
- **Application (client) ID**: `abc12345-def6-7890-ghij-klmnopqrstuv`
- **Directory (tenant) ID**: `def67890-abc1-2345-fghi-jklmnopqrstuv`

**Create Client Secret:**
1. **Certificates & secrets** → **New client secret**
2. Copy the secret value (shown only once!)

**Set API Permissions:**
1. **API permissions** → **Add a permission**
2. **Microsoft Graph** → **Delegated permissions**
3. Add these permissions:
   - ✅ `Sites.ReadWrite.All` - Read/write all SharePoint sites
   - ✅ `Files.ReadWrite.All` - Read/write all files
   - ✅ `offline_access` - Maintain access to data
4. **Grant admin consent** for your organization

### 3. SharePoint Site Configuration

**Identify Your Site:**
- Find your SharePoint site URL: `https://contoso.sharepoint.com/sites/documents`
- Extract tenant domain: `contoso.sharepoint.com`
- Note site path: `/sites/documents`

**Document Libraries:**
- **Documents** (default library)
- **Shared Documents**
- Custom libraries you've created

### 4. Environment Configuration

**Set Environment Variables:**
```powershell
# Replace with your actual Azure values
$env:SHAREPOINT_TENANT_ID = "def67890-abc1-2345-fghi-jklmnopqrstuv"
$env:SHAREPOINT_CLIENT_ID = "abc12345-def6-7890-ghij-klmnopqrstuv"
$env:SHAREPOINT_CLIENT_SECRET = "your-client-secret-from-azure"
$env:SHAREPOINT_SITE_URL = "https://contoso.sharepoint.com/sites/documents"
$env:SHAREPOINT_REDIRECT_URI = "http://localhost:5656/sharepoint/callback"
```

**Or update default.env file:**
```env
SHAREPOINT_TENANT_ID=def67890-abc1-2345-fghi-jklmnopqrstuv
SHAREPOINT_CLIENT_ID=abc12345-def6-7890-ghij-klmnopqrstuv
SHAREPOINT_CLIENT_SECRET=your-client-secret-from-azure
SHAREPOINT_SITE_URL=https://contoso.sharepoint.com/sites/documents
SHAREPOINT_REDIRECT_URI=http://localhost:5656/sharepoint/callback
```

### 5. Start Your Server

```powershell
# Start API Logic Server (SharePoint integration is already added)
python api_logic_server_run.py
```

You should see:
```
✅ SharePoint integration endpoints added
   • GET  /sharepoint              - Web interface
   • GET  /sharepoint/auth         - Start OAuth flow
   • GET  /sharepoint/callback     - OAuth callback  
   • GET  /sharepoint/libraries    - List document libraries
   • GET  /sharepoint/files        - List files
   • POST /sharepoint/upload       - Upload files
   • GET  /sharepoint/download/<id> - Download files
   • GET  /sharepoint/share/<id>   - Create share links
   • POST /sharepoint/folder       - Create folders
   • GET  /sharepoint/search       - Search documents
   • GET  /sharepoint/versions/<id> - File versions
```

### 6. Access SharePoint Manager

**Open in your browser:**
```
http://localhost:5656/sharepoint
```

**First-time setup:**
1. Click **"Connect to SharePoint"**
2. Complete Microsoft OAuth flow
3. Grant permissions to your app
4. Return to the document manager

## 🖥️ Web Interface Features

### Document Management
- **Multi-library support** - Browse different document libraries
- **Advanced file browser** with folder navigation
- **Drag & drop uploads** with progress indicators
- **Version history** viewing and management
- **Enterprise search** across all documents
- **Share link creation** with organization-level permissions

### Enterprise Features
- **Document library selector** - Switch between different libraries
- **Metadata display** - See file properties, created by, modified date
- **Version control** - View and manage document versions
- **Collaboration tools** - Share with team members
- **Search functionality** - Find documents across the site

## 🔗 API Endpoints

### Authentication & Site Info
```http
# Get authentication URL
GET /sharepoint/auth

# Get site information
GET /sharepoint/site

# List document libraries
GET /sharepoint/libraries
```

### Document Operations
```http
# List files in library
GET /sharepoint/files?library=Documents&path=/Contracts

# Upload document
POST /sharepoint/upload
Content-Type: multipart/form-data
{
  "file": <file_data>,
  "library": "Documents",
  "folder": "/Contracts"
}

# Download document
GET /sharepoint/download/{file_id}

# Create share link
GET /sharepoint/share/{file_id}?type=view&scope=organization

# Search documents
GET /sharepoint/search?q=contract&library=Documents

# Get version history
GET /sharepoint/versions/{file_id}

# Create folder
POST /sharepoint/folder
Content-Type: application/json
{
  "name": "New Folder",
  "library": "Documents",
  "parent_path": "/Contracts"
}
```

## 📝 Usage Examples

### PowerShell Examples
```powershell
# Get authentication URL
$auth = Invoke-RestMethod -Uri "http://localhost:5656/sharepoint/auth"
Write-Host "Visit: $($auth.auth_url)"

# List document libraries (after authentication)
$libraries = Invoke-RestMethod -Uri "http://localhost:5656/sharepoint/libraries"
$libraries.libraries | ForEach-Object { Write-Host $_.displayName }

# Search for contracts
$results = Invoke-RestMethod -Uri "http://localhost:5656/sharepoint/search?q=contract"
Write-Host "Found $($results.results.Count) documents"

# Get site information
$site = Invoke-RestMethod -Uri "http://localhost:5656/sharepoint/site"
Write-Host "Site: $($site.site.displayName)"
```

### JavaScript Examples
```javascript
// Upload document
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('library', 'Documents');
formData.append('folder', '/Contracts');

fetch('/sharepoint/upload', {
    method: 'POST',
    body: formData
}).then(response => response.json())
  .then(data => console.log('Upload result:', data));

// Search documents
fetch('/sharepoint/search?q=budget&library=Documents')
    .then(response => response.json())
    .then(data => console.log('Search results:', data.results));

// Get document libraries
fetch('/sharepoint/libraries')
    .then(response => response.json())
    .then(data => console.log('Libraries:', data.libraries));
```

## 🏢 Enterprise Integration

### Business Logic Integration
```python
# Example: Automatically save reports to SharePoint
from integration.sharepoint_service import sharepoint_service

def save_report_to_sharepoint(report_data, filename, library="Reports"):
    """Save generated report to SharePoint document library"""
    try:
        result = sharepoint_service.upload_file(
            library,
            f"/Monthly Reports/{filename}",
            report_data,
            "application/pdf"
        )
        
        if result:
            # Create organization share link
            share_link = sharepoint_service.create_share_link(
                result['id'], 
                link_type='view',
                scope='organization'
            )
            
            # Log to audit trail
            logger.info(f"Report uploaded: {filename}, Share: {share_link}")
            return share_link
        
    except Exception as e:
        logger.error(f"Failed to save report: {e}")
        return None

# Example: Document workflow integration
def process_contract_workflow(contract_data):
    """Process contract through SharePoint workflow"""
    # Upload contract
    contract_file = generate_contract_pdf(contract_data)
    result = sharepoint_service.upload_file(
        "Contracts",
        f"/Pending/{contract_data['contract_number']}.pdf",
        contract_file,
        "application/pdf"
    )
    
    if result:
        # Create share link for review
        review_link = sharepoint_service.create_share_link(
            result['id'], 
            link_type='edit',
            scope='organization'
        )
        
        # Send for approval (integrate with your workflow)
        send_for_approval(contract_data, review_link)
```

### Metadata and Content Types
```python
# Example: Enhanced file upload with metadata
def upload_with_metadata(file_data, filename, document_type, department):
    """Upload file with SharePoint metadata"""
    
    # Upload the file first
    result = sharepoint_service.upload_file(
        "Documents",
        f"/{department}/{filename}",
        file_data,
        "application/pdf"
    )
    
    if result:
        # Add metadata (requires Graph API extensions)
        file_id = result['id']
        metadata = {
            "DocumentType": document_type,
            "Department": department,
            "UploadedBy": get_current_user(),
            "ReviewDate": get_next_review_date()
        }
        
        # Note: Metadata updates require additional Graph API calls
        # This is a conceptual example
```

## 🔐 Security & Compliance

### Production Security
```powershell
# Production environment variables
$env:SHAREPOINT_CLIENT_SECRET = Get-AzKeyVaultSecret -VaultName "YourKeyVault" -Name "SharePointSecret"
$env:SHAREPOINT_SITE_URL = "https://yourtenant.sharepoint.com/sites/production"
```

### Access Control
- **Organization-only sharing** by default
- **Conditional access policies** support
- **Multi-factor authentication** integration
- **Audit logging** for all operations

### Compliance Features
- **Data Loss Prevention (DLP)** integration
- **Retention policies** automatic application
- **eDiscovery** support
- **Compliance center** integration

## 🔧 Advanced Configuration

### Multi-Site Support
```python
# Configure multiple SharePoint sites
sites_config = {
    "documents": "https://contoso.sharepoint.com/sites/documents",
    "projects": "https://contoso.sharepoint.com/sites/projects",
    "hr": "https://contoso.sharepoint.com/sites/hr"
}

def get_site_service(site_name):
    """Get SharePoint service for specific site"""
    site_url = sites_config.get(site_name)
    if site_url:
        service = SharePointService()
        service.site_url = site_url
        return service
    return None
```

### Custom Document Libraries
```python
# Work with custom content types
def upload_contract(contract_data, file_content):
    """Upload to Contracts library with proper content type"""
    result = sharepoint_service.upload_file(
        "Contracts",
        f"/Active/{contract_data['number']}.pdf",
        file_content,
        "application/pdf"
    )
    
    # Set contract-specific metadata
    if result:
        # Additional metadata handling here
        pass
```

## 🧪 Testing & Troubleshooting

### Health Checks
```powershell
# Test SharePoint connectivity
Invoke-RestMethod -Uri "http://localhost:5656/sharepoint/site" | 
    ConvertTo-Json -Depth 3

# Test document library access
Invoke-RestMethod -Uri "http://localhost:5656/sharepoint/libraries" |
    ConvertTo-Json -Depth 3
```

### Common Issues

**1. Authentication Failures**
```
Error: "AADSTS65001: The user or administrator has not consented"
```
**Solution**: Grant admin consent in Azure portal for all required permissions

**2. Site Access Denied**
```
Error: "Access denied to SharePoint site"
```
**Solution**: Ensure the app has proper permissions and the user has access to the site

**3. Library Not Found**
```
Error: "Document library not found"
```
**Solution**: Check library name and ensure it exists in the SharePoint site

## ✅ SharePoint vs OneDrive Benefits

| Feature | SharePoint | OneDrive |
|---------|------------|----------|
| **Document Libraries** | ✅ Multiple libraries with metadata | ❌ Single file storage |
| **Version Control** | ✅ Full version history & check-in/out | ✅ Basic versions |
| **Enterprise Permissions** | ✅ Advanced ACLs & governance | ❌ Limited sharing |
| **Content Types** | ✅ Rich metadata & workflows | ❌ Basic file properties |
| **Compliance** | ✅ DLP, retention, eDiscovery | ❌ Limited compliance |
| **Team Collaboration** | ✅ Built for teams | ❌ Personal storage focus |
| **Search** | ✅ Enterprise search across sites | ❌ Limited search |
| **Integration** | ✅ Full Microsoft 365 integration | ❌ Basic integration |

## 🎉 Summary

You now have **enterprise-grade SharePoint integration** that provides:

- ✅ **Professional document management** with multiple libraries
- ✅ **Advanced permissions** and governance features
- ✅ **Version control** and audit trails
- ✅ **Enterprise search** capabilities
- ✅ **Microsoft 365 integration**
- ✅ **Compliance and security** features
- ✅ **Team collaboration** tools

**Access your SharePoint manager at:** `http://localhost:5656/sharepoint`

Perfect for enterprise environments where document governance, compliance, and team collaboration are essential! 🏢📚