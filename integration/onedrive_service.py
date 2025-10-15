"""
OneDrive Client Integration for API Logic Server
Simple implementation to integrate OneDrive file sharing with your existing Flask app
"""

import requests
import json
import os
from typing import List, Dict, Optional
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class OneDriveService:
    """
    OneDrive integration service for API Logic Server
    Provides file upload, download, and sharing capabilities
    """
    
    def __init__(self):
        self.client_id = os.getenv('ONEDRIVE_CLIENT_ID')
        self.client_secret = os.getenv('ONEDRIVE_CLIENT_SECRET')
        self.tenant_id = os.getenv('ONEDRIVE_TENANT_ID', 'common')
        self.redirect_uri = os.getenv('ONEDRIVE_REDIRECT_URI', 'http://localhost:5656/onedrive/callback')
        self.access_token = None
        self.refresh_token = None
        self.base_url = "https://graph.microsoft.com/v1.0"
        
    def get_auth_url(self) -> str:
        """Generate OneDrive OAuth authorization URL"""
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': 'Files.ReadWrite Files.ReadWrite.All Sites.ReadWrite.All offline_access',
            'response_mode': 'query'
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        auth_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/authorize?{query_string}"
        
        return auth_url
    
    def exchange_code_for_tokens(self, auth_code: str) -> bool:
        """Exchange authorization code for access tokens"""
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        try:
            response = requests.post(token_url, data=data)
            token_data = response.json()
            
            if 'access_token' in token_data:
                self.access_token = token_data['access_token']
                self.refresh_token = token_data.get('refresh_token')
                logger.info("Successfully obtained OneDrive access tokens")
                return True
            else:
                logger.error(f"Token exchange failed: {token_data}")
                return False
                
        except Exception as e:
            logger.error(f"Error exchanging code for tokens: {e}")
            return False
    
    def refresh_access_token(self) -> bool:
        """Refresh the access token using refresh token"""
        if not self.refresh_token:
            return False
            
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }
        
        try:
            response = requests.post(token_url, data=data)
            token_data = response.json()
            
            if 'access_token' in token_data:
                self.access_token = token_data['access_token']
                if 'refresh_token' in token_data:
                    self.refresh_token = token_data['refresh_token']
                return True
            else:
                logger.error(f"Token refresh failed: {token_data}")
                return False
                
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return False
    
    def _make_api_request(self, method: str, endpoint: str, **kwargs) -> Optional[requests.Response]:
        """Make authenticated API request to Microsoft Graph"""
        if not self.access_token:
            logger.error("No access token available")
            return None
        
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {self.access_token}'
        kwargs['headers'] = headers
        
        url = f"{self.base_url}{endpoint}"
        
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
            logger.error(f"API request failed: {e}")
            return None
    
    def list_files(self, folder_path: str = "/") -> List[Dict]:
        """List files in OneDrive folder"""
        if folder_path == "/":
            endpoint = "/me/drive/root/children"
        else:
            folder_path = folder_path.strip('/')
            endpoint = f"/me/drive/root:/{folder_path}:/children"
        
        response = self._make_api_request('GET', endpoint)
        
        if response and response.status_code == 200:
            return response.json().get('value', [])
        else:
            logger.error(f"Failed to list files: {response.status_code if response else 'No response'}")
            return []
    
    def upload_file(self, file_path: str, content: bytes, content_type: str = None) -> Optional[Dict]:
        """Upload file to OneDrive"""
        file_path = file_path.strip('/')
        endpoint = f"/me/drive/root:/{file_path}:/content"
        
        headers = {}
        if content_type:
            headers['Content-Type'] = content_type
        
        response = self._make_api_request('PUT', endpoint, data=content, headers=headers)
        
        if response and response.status_code in [200, 201]:
            return response.json()
        else:
            logger.error(f"Failed to upload file: {response.status_code if response else 'No response'}")
            return None
    
    def download_file(self, file_id: str) -> Optional[bytes]:
        """Download file from OneDrive"""
        endpoint = f"/me/drive/items/{file_id}/content"
        
        response = self._make_api_request('GET', endpoint)
        
        if response and response.status_code == 200:
            return response.content
        else:
            logger.error(f"Failed to download file: {response.status_code if response else 'No response'}")
            return None
    
    def create_share_link(self, file_id: str, link_type: str = "view", scope: str = "anonymous") -> Optional[str]:
        """Create shareable link for file or folder"""
        endpoint = f"/me/drive/items/{file_id}/createLink"
        
        data = {
            "type": link_type,  # "view", "edit", "embed"
            "scope": scope      # "anonymous", "organization"
        }
        
        response = self._make_api_request('POST', endpoint, json=data)
        
        if response and response.status_code == 201:
            return response.json().get('link', {}).get('webUrl')
        else:
            logger.error(f"Failed to create share link: {response.status_code if response else 'No response'}")
            return None
    
    def create_folder(self, folder_name: str, parent_path: str = "/") -> Optional[Dict]:
        """Create a new folder in OneDrive"""
        if parent_path == "/":
            endpoint = "/me/drive/root/children"
        else:
            parent_path = parent_path.strip('/')
            endpoint = f"/me/drive/root:/{parent_path}:/children"
        
        data = {
            "name": folder_name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename"
        }
        
        response = self._make_api_request('POST', endpoint, json=data)
        
        if response and response.status_code == 201:
            return response.json()
        else:
            logger.error(f"Failed to create folder: {response.status_code if response else 'No response'}")
            return None
    
    def delete_file(self, file_id: str) -> bool:
        """Delete file or folder from OneDrive"""
        endpoint = f"/me/drive/items/{file_id}"
        
        response = self._make_api_request('DELETE', endpoint)
        
        if response and response.status_code == 204:
            return True
        else:
            logger.error(f"Failed to delete file: {response.status_code if response else 'No response'}")
            return False
    
    def get_file_info(self, file_id: str) -> Optional[Dict]:
        """Get detailed information about a file or folder"""
        endpoint = f"/me/drive/items/{file_id}"
        
        response = self._make_api_request('GET', endpoint)
        
        if response and response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get file info: {response.status_code if response else 'No response'}")
            return None

# Global instance
onedrive_service = OneDriveService()

def add_onedrive_endpoints(app):
    """Add OneDrive endpoints to Flask app"""
    
    @app.route('/onedrive')
    def onedrive_manager():
        """OneDrive file manager web interface"""
        from flask import render_template
        return render_template('onedrive_manager.html')
    
    @app.route('/onedrive/auth')
    def onedrive_auth():
        """Initiate OneDrive OAuth flow"""
        auth_url = onedrive_service.get_auth_url()
        return {"auth_url": auth_url}
    
    @app.route('/onedrive/callback')
    def onedrive_callback():
        """Handle OneDrive OAuth callback"""
        from flask import request, session
        
        auth_code = request.args.get('code')
        if not auth_code:
            error = request.args.get('error', 'unknown_error')
            return {"error": error}, 400
        
        if onedrive_service.exchange_code_for_tokens(auth_code):
            session['onedrive_authenticated'] = True
            return {"success": True, "message": "OneDrive authentication successful"}
        else:
            return {"error": "Failed to authenticate with OneDrive"}, 400
    
    @app.route('/onedrive/files')
    def onedrive_list_files():
        """List OneDrive files"""
        from flask import request
        
        folder_path = request.args.get('path', '/')
        files = onedrive_service.list_files(folder_path)
        
        return {"files": files}
    
    @app.route('/onedrive/upload', methods=['POST'])
    def onedrive_upload():
        """Upload file to OneDrive"""
        from flask import request
        
        if 'file' not in request.files:
            return {"error": "No file provided"}, 400
        
        file = request.files['file']
        folder_path = request.form.get('folder', '/')
        
        # Construct file path
        if folder_path == '/':
            file_path = file.filename
        else:
            file_path = f"{folder_path.strip('/')}/{file.filename}"
        
        result = onedrive_service.upload_file(
            file_path, 
            file.read(), 
            file.content_type
        )
        
        if result:
            return {"success": True, "file": result}
        else:
            return {"error": "Upload failed"}, 500
    
    @app.route('/onedrive/download/<file_id>')
    def onedrive_download(file_id):
        """Download file from OneDrive"""
        from flask import send_file
        import tempfile
        
        content = onedrive_service.download_file(file_id)
        if not content:
            return {"error": "Download failed"}, 500
        
        # Get file info for proper filename
        file_info = onedrive_service.get_file_info(file_id)
        filename = file_info.get('name', 'download') if file_info else 'download'
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(content)
        temp_file.close()
        
        return send_file(temp_file.name, as_attachment=True, download_name=filename)
    
    @app.route('/onedrive/share/<file_id>')
    def onedrive_share(file_id):
        """Create share link for OneDrive file"""
        from flask import request
        
        link_type = request.args.get('type', 'view')
        scope = request.args.get('scope', 'anonymous')
        
        share_link = onedrive_service.create_share_link(file_id, link_type, scope)
        
        if share_link:
            return {"success": True, "share_link": share_link}
        else:
            return {"error": "Failed to create share link"}, 500
    
    @app.route('/onedrive/folder', methods=['POST'])
    def onedrive_create_folder():
        """Create folder in OneDrive"""
        from flask import request
        
        data = request.get_json()
        folder_name = data.get('name')
        parent_path = data.get('parent_path', '/')
        
        if not folder_name:
            return {"error": "Folder name is required"}, 400
        
        result = onedrive_service.create_folder(folder_name, parent_path)
        
        if result:
            return {"success": True, "folder": result}
        else:
            return {"error": "Failed to create folder"}, 500