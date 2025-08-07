from flask import Flask, request, jsonify
from security.authentication_provider.okta.okta_token import OktaToken 
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

from flask import request, jsonify
import logging

app_logger = logging.getLogger("api_logic_server_app")
# Configuration - these should be set as environment variables in production
OKTA_DOMAIN = os.getenv('OKTA_DOMAIN', 'https://ou.okta.com')
OKTA_CLIENT_ID = os.getenv('OKTA_CLIENT_ID', '0oa1crjfiwoxRYadi0x8')
OKTA_CLIENT_SECRET = os.getenv('OKTA_CLIENT_SECRET', 'eVdobSwZgx8ANVRwPTxX6lce24t4e5ZBuAQSn_QPopvi69Xa36SWoyPjH4WcjAI7')
OKTA_REDIRECT_URL = os.getenv('OKTA_REDIRECT_URL', 'http://localhost:5656/auth/callback')# 'http://localhost:5000/callback')

# Initialize OktaToken instance
okta_token = OktaToken(
    domain=OKTA_DOMAIN,
    client_id=OKTA_CLIENT_ID,
    redirect_url=OKTA_REDIRECT_URL,
    client_secret=OKTA_CLIENT_SECRET
)


def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators ):
    pass



    @app.route('/okta', methods=['GET'])
    def index():
        """Basic health check endpoint"""
        return jsonify({
            "message": "Okta Token Service is running",
            "endpoints": {
                "get_id_token": "/api/get-id-token (POST)",
                "create_web_access_token": "/api/create-web-access-token (POST)",
                "validate_token": "/api/validate-token (POST)",
                "validate_pkce_token": "/api/validate-pkce-token (POST)"
            }
        })


    @app.route('/api/get-id-token', methods=['POST'])
    def get_id_token():
        """
        Get ID token using username and password
        
        Expected JSON payload:
        {
            "username": "user@example.com",
            "password": "password123"
        }
        """
        try:
            data = request.get_json()
            
            if not data or 'username' not in data or 'password' not in data:
                return jsonify({"error": "Username and password are required"}), 400
            
            username = data['username']
            password = data['password']
            logging.info(f"Username: {username}, Password: {password}")  # Debugging line, remove in production
            
            # Get ID token using OktaToken instance
            id_token = okta_token.get_id_token(username, password)
            logging.info(f"ID Token: {id_token}")  # Debugging line, remove in production
            if id_token:
                return jsonify({
                    "success": True,
                    "id_token": id_token
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to obtain ID token"
                }), 401
                
        except Exception as e:
            logging.error(f"Error in get_id_token: {e}")
            return jsonify({"error": "Internal server error"}), 500


    @app.route('/api/create-web-access-token', methods=['POST'])
    def create_web_access_token():
        """
        Create a web access token using client credentials
        """
        try:
            access_token = okta_token.create_web_access_token()
            
            if access_token:
                return jsonify({
                    "success": True,
                    "token_type": access_token.token_type,
                    "expires_in": access_token.expires_in,
                    "access_token": access_token.access_token,
                    "scope": access_token.scope
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to create web access token"
                }), 401
                
        except Exception as e:
            logging.error(f"Error in create_web_access_token: {e}")
            return jsonify({"error": str(e)}), 500


    @app.route('/api/validate-token', methods=['POST'])
    def validate_token():
        """
        Validate an Okta token
        
        Expected JSON payload:
        {
            "token": "eyJhbGciOiJSUzI1NiI..."
        }
        """
        try:
            data = request.get_json()
            
            if not data or 'token' not in data:
                return jsonify({"error": "Token is required"}), 400
            
            token = data['token']
            claims = okta_token.validate_okta_token(token)
            
            if claims:
                return jsonify({
                    "success": True,
                    "valid": True,
                    "claims": claims
                })
            else:
                return jsonify({
                    "success": True,
                    "valid": False,
                    "error": "Token validation failed"
                }), 401
                
        except Exception as e:
            logging.error(f"Error in validate_token: {e}")
            return jsonify({"error": "Internal server error"}), 500


    @app.route('/api/validate-pkce-token', methods=['POST'])
    def validate_pkce_token():
        """
        Validate an Okta PKCE token
        
        Expected JSON payload:
        {
            "token": "eyJhbGciOiJSUzI1NiI..."
        }
        """
        try:
            data = request.get_json()
            
            if not data or 'token' not in data:
                return jsonify({"error": "Token is required"}), 400
            
            token = data['token']
            claims = okta_token.validate_okta_pkce_token(token)
            
            if claims:
                return jsonify({
                    "success": True,
                    "valid": True,
                    "claims": claims
                })
            else:
                return jsonify({
                    "success": True,
                    "valid": False,
                    "error": "PKCE token validation failed"
                }), 401
                
        except Exception as e:
            logging.error(f"Error in validate_pkce_token: {e}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route('/callback')
    def auth_callback():
        """
        Handle the callback from Okta after authentication
        """
        code = request.args.get('code')
        state = request.args.get('state')
        if not code or not state:
            return jsonify({"error": "Missing code or state"}), 400

        # Exchange the authorization code for tokens
        tokens = okta_token.exchange_code_for_tokens(code, state)
        if tokens:
            return jsonify({
                "success": True,
                "access_token": tokens.access_token,
                "refresh_token": tokens.refresh_token,
                "expires_in": tokens.expires_in
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to exchange code for tokens"
            }), 401 

