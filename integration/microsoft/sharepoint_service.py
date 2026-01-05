"""
SharePoint Online Integration for API Logic Server
Enterprise-grade document management and sharing solution
"""

import os
import requests
import json
import base64
import logging
from typing import List, Dict, Optional, Union
from urllib.parse import quote, urljoin
from datetime import datetime, timedelta
import msal

logger = logging.getLogger(__name__)

class SharePointService:
    """
    SharePoint Online integration service for API Logic Server
    Provides document library management, file operations, and sharing capabilities
    """
    
    def __init__(self):
        self.tenant_id = os.getenv('SHAREPOINT_TENANT_ID', 'eec94eb4-840d-4d2c-a7f1-05b024e60580')
        self.client_id = os.getenv('SHAREPOINT_CLIENT_ID','cd2ecddd-9615-4a6d-a69a-18e47c4125f5')
        self.client_secret = os.getenv('SHAREPOINT_CLIENT_SECRET')
        self.site_url = os.getenv('SHAREPOINT_SITE_URL', 'https://uojca.sharepoint.com/sites/KashrusDev')
        self.redirect_uri = os.getenv('SHAREPOINT_REDIRECT_URI', 'https://devvm01.ny.ou.org:5656/sharepoint/callback')
        
        # Extract site details from URL
        self.tenant_domain = self._extract_tenant_domain(self.site_url)
        self.site_path = self._extract_site_path(self.site_url)
        
        # MSAL client for authentication
        self.app = None
        self.access_token = None
        self.refresh_token = None
        
        # SharePoint REST API base URLs
        self.graph_base_url = "https://graph.microsoft.com/v1.0"
        self.sharepoint_base_url = f"https://{self.tenant_domain}"
        
        self._initialize_msal_app()
        
    def _extract_tenant_domain(self, site_url: str) -> str:
        """Extract tenant domain from SharePoint site URL"""
        # https://contoso.sharepoint.com/sites/sitename -> contoso.sharepoint.com
        if '://' in site_url:
            parts = site_url.split('://', 1)[1]
            return parts.split('/')[0]
        return site_url.split('/')[0]
    
    def _extract_site_path(self, site_url: str) -> str:
        """Extract site path from SharePoint site URL"""
        # https://contoso.sharepoint.com/sites/sitename -> /sites/sitename
        if '://' in site_url:
            parts = site_url.split('://', 1)[1]
            path_parts = parts.split('/', 1)
            if len(path_parts) > 1:
                return '/' + path_parts[1]
        return '/sites/yoursite'  # default
    
    def _initialize_msal_app(self):
        """Initialize MSAL application for authentication"""
        if not self.client_id or not self.client_secret:
            logger.warning("SharePoint client credentials not configured")
            return
            
        try:
            authority = f"https://login.microsoftonline.com/{self.tenant_id}"
            self.app = msal.ConfidentialClientApplication(
                client_id=self.client_id,
                client_credential=self.client_secret,
                authority=authority
            )
        except Exception as e:
            logger.error(f"Failed to initialize MSAL app: {e}")
    
    def get_auth_url(self, scopes: List[str] = None) -> str:
        """Generate SharePoint OAuth authorization URL"""
        if not self.app:
            raise Exception("MSAL app not initialized. Check client credentials.")
        
        if not scopes:
            scopes = [
                "https://graph.microsoft.com/Sites.ReadWrite.All",
                "https://graph.microsoft.com/Files.ReadWrite.All",
                "offline_access"
            ]
        
        try:
            auth_url = self.app.get_authorization_request_url(
                scopes=scopes,
                redirect_uri=self.redirect_uri,
                state="sharepoint_auth"
            )
            return auth_url
        except Exception as e:
            logger.error(f"Failed to generate auth URL: {e}")
            raise
    
    def exchange_code_for_tokens(self, auth_code: str, scopes: List[str] = None) -> bool:
        """Exchange authorization code for access tokens"""
        if not self.app:
            return False
        
        if not scopes:
            scopes = [
                "https://graph.microsoft.com/Sites.ReadWrite.All",
                "https://graph.microsoft.com/Files.ReadWrite.All", 
                "offline_access"
            ]
        
        try:
            result = self.app.acquire_token_by_authorization_code(
                code=auth_code,
                scopes=scopes,
                redirect_uri=self.redirect_uri
            )
            
            if "access_token" in result:
                self.access_token = result['access_token']
                self.refresh_token = result.get('refresh_token')
                logger.info("Successfully obtained SharePoint access tokens")
                return True
            else:
                logger.error(f"Token exchange failed: {result.get('error_description', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"Error exchanging code for tokens: {e}")
            return False
    
    def refresh_access_token(self) -> bool:
        """Refresh the access token using refresh token"""
        if not self.app or not self.refresh_token:
            return False
        
        try:
            result = self.app.acquire_token_by_refresh_token(
                refresh_token=self.refresh_token,
                scopes=["https://graph.microsoft.com/Sites.ReadWrite.All"]
            )
            
            if "access_token" in result:
                self.access_token = result['access_token']
                if 'refresh_token' in result:
                    self.refresh_token = result['refresh_token']
                return True
            else:
                logger.error(f"Token refresh failed: {result.get('error_description', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return False
    
    def _make_graph_request(self, method: str, endpoint: str, **kwargs) -> Optional[requests.Response]:
        """Make authenticated request to Microsoft Graph API"""
        if not self.access_token:
            logger.error("No access token available")
            return None
        
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {self.access_token}'
        headers['Accept'] = 'application/json'
        kwargs['headers'] = headers
        
        url = f"{self.graph_base_url}{endpoint}"
        
        try:
            response = requests.request(method, url, **kwargs)
            
            # If token expired, try to refresh
            if response.status_code == 401 and self.refresh_token:
                if self.refresh_access_token():
                    headers['Authorization'] = f'Bearer {self.access_token}'
                    kwargs['headers'] = headers
                    response = requests.request(method, url, **kwargs)
            
            return response
            
        except Exception as e:
            logger.error(f"Graph API request failed: {e}")
            return None
    
    def get_site_info(self) -> Optional[Dict]:
        """Get SharePoint site information"""
        # Use Graph API to get site info by path
        site_path_encoded = quote(f"{self.tenant_domain}:{self.site_path}", safe='')
        endpoint = f"/sites/{site_path_encoded}"
        
        response = self._make_graph_request('GET', endpoint)
        
        if response and response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get site info: {response.status_code if response else 'No response'}")
            return None
    
    def get_document_libraries(self) -> List[Dict]:
        """Get all document libraries in the SharePoint site"""
        site_info = self.get_site_info()
        if not site_info:
            return []
        
        site_id = site_info['id']
        endpoint = f"/sites/{site_id}/lists?$filter=baseTemplate eq 101"  # 101 = Document Library
        
        response = self._make_graph_request('GET', endpoint)
        
        if response and response.status_code == 200:
            return response.json().get('value', [])
        else:
            logger.error(f"Failed to get document libraries: {response.status_code if response else 'No response'}")
            return []
    
    def list_files(self, library_name: str = "Documents", folder_path: str = "") -> List[Dict]:
        """List files in a SharePoint document library"""
        site_info = self.get_site_info()
        if not site_info:
            return []
        
        site_id = site_info['id']
        
        if folder_path:
            folder_path = folder_path.strip('/')
            endpoint = f"/sites/{site_id}/lists/{library_name}/drive/root:/{folder_path}:/children"
        else:
            endpoint = f"/sites/{site_id}/lists/{library_name}/drive/root/children"
        
        response = self._make_graph_request('GET', endpoint)
        
        if response and response.status_code == 200:
            return response.json().get('value', [])
        else:
            logger.error(f"Failed to list files: {response.status_code if response else 'No response'}")
            return []
    
    def upload_file(self, library_name: str, file_path: str, content: bytes, 
                   content_type: str = None, overwrite: bool = True) -> Optional[Dict]:
        """Upload file to SharePoint document library"""
        site_info = self.get_site_info()
        if not site_info:
            return None
        
        site_id = site_info['id']
        file_path = file_path.strip('/')
        
        # For files larger than 4MB, use upload session
        if len(content) > 4 * 1024 * 1024:
            return self._upload_large_file(site_id, library_name, file_path, content, overwrite)
        
        # Simple upload for small files
        endpoint = f"/sites/{site_id}/lists/{library_name}/drive/root:/{file_path}:/content"
        
        headers = {}
        if content_type:
            headers['Content-Type'] = content_type
        
        response = self._make_graph_request('PUT', endpoint, data=content, headers=headers)
        
        if response and response.status_code in [200, 201]:
            return response.json()
        else:
            logger.error(f"Failed to upload file: {response.status_code if response else 'No response'}")
            return None
    
    def _upload_large_file(self, site_id: str, library_name: str, file_path: str, 
                          content: bytes, overwrite: bool = True) -> Optional[Dict]:
        """Upload large file using upload session"""
        # Create upload session
        endpoint = f"/sites/{site_id}/lists/{library_name}/drive/root:/{file_path}:/createUploadSession"
        
        session_data = {
            "item": {
                "@microsoft.graph.conflictBehavior": "replace" if overwrite else "rename"
            }
        }
        
        response = self._make_graph_request('POST', endpoint, json=session_data)
        
        if not response or response.status_code != 200:
            logger.error("Failed to create upload session")
            return None
        
        upload_url = response.json()['uploadUrl']
        
        # Upload in chunks
        chunk_size = 320 * 1024  # 320KB chunks
        file_size = len(content)
        
        for start in range(0, file_size, chunk_size):
            end = min(start + chunk_size, file_size)
            chunk = content[start:end]
            
            headers = {
                'Content-Range': f'bytes {start}-{end-1}/{file_size}',
                'Content-Length': str(len(chunk))
            }
            
            chunk_response = requests.put(upload_url, data=chunk, headers=headers)
            
            if chunk_response.status_code not in [202, 201, 200]:
                logger.error(f"Upload chunk failed: {chunk_response.status_code}")
                return None
        
        # Final response should contain the file info
        if chunk_response.status_code in [200, 201]:
            return chunk_response.json()
        
        return None
    
    def download_file(self, file_id: str) -> Optional[bytes]:
        """Download file from SharePoint"""
        endpoint = f"/sites/{self.get_site_info()['id']}/drive/items/{file_id}/content"
        
        response = self._make_graph_request('GET', endpoint)
        
        if response and response.status_code == 200:
            return response.content
        else:
            logger.error(f"Failed to download file: {response.status_code if response else 'No response'}")
            return None
    
    def create_share_link(self, file_id: str, link_type: str = "view", 
                         scope: str = "organization") -> Optional[str]:
        """Create shareable link for SharePoint file"""
        site_id = self.get_site_info()['id']
        endpoint = f"/sites/{site_id}/drive/items/{file_id}/createLink"
        
        data = {
            "type": link_type,  # "view", "edit", "embed"
            "scope": scope      # "anonymous", "organization", "users"
        }
        
        response = self._make_graph_request('POST', endpoint, json=data)
        
        if response and response.status_code == 201:
            return response.json().get('link', {}).get('webUrl')
        else:
            logger.error(f"Failed to create share link: {response.status_code if response else 'No response'}")
            return None
    
    def create_folder(self, library_name: str, folder_name: str, 
                     parent_path: str = "") -> Optional[Dict]:
        """Create folder in SharePoint document library"""
        site_info = self.get_site_info()
        if not site_info:
            return None
        
        site_id = site_info['id']
        
        if parent_path:
            parent_path = parent_path.strip('/')
            endpoint = f"/sites/{site_id}/lists/{library_name}/drive/root:/{parent_path}:/children"
        else:
            endpoint = f"/sites/{site_id}/lists/{library_name}/drive/root/children"
        
        data = {
            "name": folder_name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename"
        }
        
        response = self._make_graph_request('POST', endpoint, json=data)
        
        if response and response.status_code == 201:
            return response.json()
        else:
            logger.error(f"Failed to create folder: {response.status_code if response else 'No response'}")
            return None
    
    def delete_file(self, file_id: str) -> bool:
        """Delete file or folder from SharePoint"""
        site_id = self.get_site_info()['id']
        endpoint = f"/sites/{site_id}/drive/items/{file_id}"
        
        response = self._make_graph_request('DELETE', endpoint)
        
        if response and response.status_code == 204:
            return True
        else:
            logger.error(f"Failed to delete file: {response.status_code if response else 'No response'}")
            return False
    
    def get_file_info(self, file_id: str) -> Optional[Dict]:
        """Get detailed information about a SharePoint file"""
        site_id = self.get_site_info()['id']
        endpoint = f"/sites/{site_id}/drive/items/{file_id}"
        
        response = self._make_graph_request('GET', endpoint)
        
        if response and response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get file info: {response.status_code if response else 'No response'}")
            return None
    
    def search_files(self, query: str, library_name: str = None) -> List[Dict]:
        """Search for files in SharePoint site"""
        site_info = self.get_site_info()
        if not site_info:
            return []
        
        site_id = site_info['id']
        
        if library_name:
            endpoint = f"/sites/{site_id}/lists/{library_name}/drive/search(q='{query}')"
        else:
            endpoint = f"/sites/{site_id}/drive/search(q='{query}')"
        
        response = self._make_graph_request('GET', endpoint)
        
        if response and response.status_code == 200:
            return response.json().get('value', [])
        else:
            logger.error(f"Failed to search files: {response.status_code if response else 'No response'}")
            return []
    
    def get_file_versions(self, file_id: str) -> List[Dict]:
        """Get version history of a SharePoint file"""
        site_id = self.get_site_info()['id']
        endpoint = f"/sites/{site_id}/drive/items/{file_id}/versions"
        
        response = self._make_graph_request('GET', endpoint)
        
        if response and response.status_code == 200:
            return response.json().get('value', [])
        else:
            logger.error(f"Failed to get file versions: {response.status_code if response else 'No response'}")
            return []

# Global instance
sharepoint_service = SharePointService()

def add_sharepoint_endpoints(app):
    """Add SharePoint endpoints to Flask app"""
    
    @app.route('/sharepoint')
    def sharepoint_manager():
        """SharePoint file manager web interface"""
        from flask import render_template
        return render_template('sharepoint_manager.html')
    
    @app.route('/sharepoint/auth')
    def sharepoint_auth():
        """Initiate SharePoint OAuth flow"""
        try:
            auth_url = sharepoint_service.get_auth_url()
            return {"auth_url": auth_url}
        except Exception as e:
            return {"error": str(e)}, 500
    
    @app.route('/sharepoint/callback')
    def sharepoint_callback():
        """Handle SharePoint OAuth callback"""
        from flask import request, session
        
        auth_code = request.args.get('code')
        if not auth_code:
            error = request.args.get('error', 'unknown_error')
            return {"error": error}, 400
        
        if sharepoint_service.exchange_code_for_tokens(auth_code):
            session['sharepoint_authenticated'] = True
            return {"success": True, "message": "SharePoint authentication successful"}
        else:
            return {"error": "Failed to authenticate with SharePoint"}, 400
    
    @app.route('/sharepoint/site')
    def sharepoint_site_info():
        """Get SharePoint site information"""
        site_info = sharepoint_service.get_site_info()
        if site_info:
            return {"site": site_info}
        else:
            return {"error": "Failed to get site information"}, 500
    
    @app.route('/sharepoint/libraries')
    def sharepoint_libraries():
        """Get document libraries in SharePoint site"""
        libraries = sharepoint_service.get_document_libraries()
        return {"libraries": libraries}
    
    @app.route('/sharepoint/files')
    def sharepoint_list_files():
        """List files in SharePoint document library"""
        from flask import request
        
        library = request.args.get('library', 'Documents')
        folder_path = request.args.get('path', '')
        
        files = sharepoint_service.list_files(library, folder_path)
        return {"files": files, "library": library, "path": folder_path}
    
    @app.route('/sharepoint/upload', methods=['POST'])
    def sharepoint_upload():
        """Upload file to SharePoint"""
        from flask import request
        
        if 'file' not in request.files:
            return {"error": "No file provided"}, 400
        
        file = request.files['file']
        library = request.form.get('library', 'Documents')
        folder_path = request.form.get('folder', '')
        
        # Construct file path
        if folder_path:
            file_path = f"{folder_path.strip('/')}/{file.filename}"
        else:
            file_path = file.filename
        
        result = sharepoint_service.upload_file(
            library, 
            file_path, 
            file.read(), 
            file.content_type
        )
        
        if result:
            return {"success": True, "file": result}
        else:
            return {"error": "Upload failed"}, 500
    
    @app.route('/sharepoint/download/<file_id>')
    def sharepoint_download(file_id):
        """Download file from SharePoint"""
        from flask import send_file
        import tempfile
        
        content = sharepoint_service.download_file(file_id)
        if not content:
            return {"error": "Download failed"}, 500
        
        # Get file info for proper filename
        file_info = sharepoint_service.get_file_info(file_id)
        filename = file_info.get('name', 'download') if file_info else 'download'
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(content)
        temp_file.close()
        
        return send_file(temp_file.name, as_attachment=True, download_name=filename)
    
    @app.route('/sharepoint/share/<file_id>')
    def sharepoint_share(file_id):
        """Create share link for SharePoint file"""
        from flask import request
        
        link_type = request.args.get('type', 'view')
        scope = request.args.get('scope', 'organization')
        
        share_link = sharepoint_service.create_share_link(file_id, link_type, scope)
        
        if share_link:
            return {"success": True, "share_link": share_link}
        else:
            return {"error": "Failed to create share link"}, 500
    
    @app.route('/sharepoint/folder', methods=['POST'])
    def sharepoint_create_folder():
        """Create folder in SharePoint"""
        from flask import request
        
        data = request.get_json()
        folder_name = data.get('name')
        library = data.get('library', 'Documents')
        parent_path = data.get('parent_path', '')
        
        if not folder_name:
            return {"error": "Folder name is required"}, 400
        
        result = sharepoint_service.create_folder(library, folder_name, parent_path)
        
        if result:
            return {"success": True, "folder": result}
        else:
            return {"error": "Failed to create folder"}, 500
    
    @app.route('/sharepoint/search')
    def sharepoint_search():
        """Search files in SharePoint"""
        from flask import request
        
        query = request.args.get('q', '')
        library = request.args.get('library')
        
        if not query:
            return {"error": "Search query is required"}, 400
        
        results = sharepoint_service.search_files(query, library)
        return {"results": results, "query": query}
    
    @app.route('/sharepoint/versions/<file_id>')
    def sharepoint_file_versions(file_id):
        """Get version history of SharePoint file"""
        versions = sharepoint_service.get_file_versions(file_id)
        return {"versions": versions}