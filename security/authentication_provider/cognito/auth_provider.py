from security.authentication_provider.abstract_authentication_provider import Abstract_Authentication_Provider
import sqlalchemy as sqlalchemy
import database.database_discovery.authentication_models as authentication_models
from flask import Flask
import safrs
from safrs.errors import JsonapiError
from dotmap import DotMap
from sqlalchemy import inspect
from http import HTTPStatus
import logging
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required as jwt_required_ori
import flask_jwt_extended as flask_jwt_extended
from flask import jsonify, g, request, redirect, url_for
from flask import session
import requests
import json
import sys
import time
import jwt
from jwt.algorithms import RSAAlgorithm
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import hmac
import hashlib
import urllib.parse

# **********************
# Amazon Cognito auth provider
# **********************

db = None
db_session = None  # Renamed to avoid conflict with Flask session

logger = logging.getLogger('api_logic_server_app')

class ALSError(JsonapiError):
    def __init__(self, message, status_code=HTTPStatus.BAD_REQUEST):
        super().__init__()
        self.message = message
        self.status_code = status_code

class DotMapX(DotMap):
    """ DotMap, with extended support for auth providers """
    def check_password(self, password=None):
        # For Cognito, password validation is handled by token validation
        return True

class Authentication_Provider(Abstract_Authentication_Provider):

    @staticmethod
    def configure_auth(flask_app: Flask):
        """ Called by authentication.py on server start, to 
        - initialize jwt
        - establish Flask end points for login.
        """
        # Configure JWT for Cognito tokens
        flask_app.config['JWT_SECRET_KEY'] = "ApiLogicServerSecret"
        flask_app.config['JWT_ALGORITHM'] = 'HS256'
        flask_app.config['JWT_IDENTITY_CLAIM'] = 'sub'
        flask_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1440)  # 24 hours
        flask_app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
        
        logger.info("Configured Amazon Cognito JWT authentication:")
        logger.info("- JWT signature verification handled manually")
        logger.info("- Cognito RS256 tokens validated via JWKS")
        logger.info("- Internal tokens use system defaults")
        
        # Install JWT monkey patch for Cognito tokens
        Authentication_Provider._install_jwt_monkey_patch()
        
        # Add Cognito endpoints
        Authentication_Provider._add_cognito_endpoints(flask_app)
        return

    @staticmethod
    def _install_jwt_monkey_patch():
        """Install a monkey patch to intercept JWT verification for Cognito tokens"""
        import flask_jwt_extended.utils
        import flask_jwt_extended.view_decorators
        from flask import request, g
        
        # Save the original functions
        original_decode_token = flask_jwt_extended.utils.decode_token
        original_verify_jwt_in_request = flask_jwt_extended.view_decorators.verify_jwt_in_request
        
        def patched_decode_token(encoded_token, csrf_token=None, allow_expired=False):
            """Patched JWT decode function that handles Cognito tokens"""
            try:
                return original_decode_token(encoded_token, csrf_token, allow_expired)
            except Exception as e:
                logger.info(f"Flask-JWT-Extended decode failed: {str(e)[:100]}")
                
                # Check if this looks like a Cognito token (RS256 algorithm)
                try:
                    import jwt as pyjwt
                    header = pyjwt.get_unverified_header(encoded_token)
                    if header.get('alg') == 'RS256':
                        logger.info("Detected RS256 token, trying Cognito validation")
                        
                        # Try Cognito validation
                        claims = Authentication_Provider.validate_cognito_token(encoded_token)
                        if claims:
                            logger.info("Successfully validated Cognito token")
                            return {
                                'sub': claims.get('sub'),
                                'iat': claims.get('iat', 0),
                                'exp': claims.get('exp', 0),
                                'jti': claims.get('jti', 'cognito-token'),
                                'type': 'access',
                                'fresh': False,
                                **claims
                            }
                        else:
                            logger.info("Cognito validation failed")
                except Exception as cognito_error:
                    logger.info(f"Cognito validation error: {cognito_error}")
                
                raise e
        
        def patched_verify_jwt_in_request(optional=False, fresh=False, refresh=False, locations=None, verify_type=True):
            """Patched JWT verification that's more lenient with Cognito tokens"""
            try:
                return original_verify_jwt_in_request(optional, fresh, refresh, locations, verify_type)
            except Exception as e:
                logger.info(f"JWT verification failed: {str(e)[:100]}")
                
                if optional:
                    logger.info("Optional JWT verification, allowing request to continue")
                    return None
                
                # Try to extract token manually and validate with Cognito
                auth_header = request.headers.get('Authorization', '')
                if auth_header.startswith('Bearer '):
                    token = auth_header.replace('Bearer ', '')
                    
                    claims = Authentication_Provider.validate_cognito_token(token)
                    if claims:
                        logger.info("Cognito token validated during verify_jwt_in_request")
                        g.jwt_user_claims = claims
                        g.jwt_user_identity = claims.get('sub')
                        return None
                
                raise e
        
        # Replace the functions
        flask_jwt_extended.utils.decode_token = patched_decode_token
        flask_jwt_extended.view_decorators.verify_jwt_in_request = patched_verify_jwt_in_request
        
        logger.info("Installed comprehensive JWT monkey patch for Cognito token support")

    @staticmethod
    def _add_cognito_endpoints(flask_app: Flask):
        """Add Cognito endpoints to Flask app"""
        from config.config import Args
        
        @flask_app.route('/auth/login', methods=['GET', 'POST'])
        def cognito_login():
            """Redirect to Cognito Hosted UI for authentication"""
            try:
                # Check if Cognito is properly configured
                if not getattr(Args.instance, 'cognito_client_id', None):
                    return jsonify({
                        'error': 'Cognito not configured',
                        'message': 'COGNITO_CLIENT_ID not set',
                        'debug_url': f"{request.host_url}auth/debug"
                    }), 500
                
                if not getattr(Args.instance, 'cognito_domain', None):
                    return jsonify({
                        'error': 'Cognito not configured', 
                        'message': 'COGNITO_DOMAIN not set',
                        'debug_url': f"{request.host_url}auth/debug"
                    }), 500
                
                import secrets
                state = secrets.token_urlsafe(32)
                session['oauth_state'] = state
                
                # Build Cognito authorization URL
                auth_params = {
                    'client_id': Args.instance.cognito_client_id,
                    'response_type': 'code',
                    'scope': 'openid profile email phone', #aws.cognito.signin.user.admin',
                    'redirect_uri': Args.instance.cognito_redirect_uri.strip('/'),
                    'state': state
                }
                
                # Cognito Hosted UI URL format
                auth_url = f"{Args.instance.cognito_domain}/oauth2/authorize?" + urllib.parse.urlencode(auth_params)
                
                logger.info(f"Cognito login attempt:")
                logger.info(f"  Auth URL: {auth_url}")
                logger.info(f"  Redirect URI: {auth_params['redirect_uri']}")
                logger.info(f"  Client ID: {auth_params['client_id'][:8]}...")
                logger.info(f"  State: {state}")
                
                return redirect(auth_url)
                
            except Exception as e:
                logger.error(f"Error in Cognito login: {e}")
                return jsonify({
                    'error': 'Login configuration error',
                    'message': str(e),
                    'debug_url': f"{request.host_url}auth/debug"
                }), 500
        
        @flask_app.route('/auth/login-postman', methods=['GET'])
        def cognito_login_postman():
            """Cognito login for POSTMAN testing - returns JSON instead of redirecting"""
            import secrets
            state = secrets.token_urlsafe(32)
            session['oauth_state'] = state
            
            auth_params = {
                'client_id': Args.instance.cognito_client_id,
                'response_type': 'code',
                'scope': 'openid profile email phone', #aws.cognito.signin.user.admin',
                'redirect_uri': Args.instance.cognito_redirect_uri.strip('/'),
                'state': state
            }
            
            auth_url = f"{Args.instance.cognito_domain}/oauth2/authorize?" + urllib.parse.urlencode(auth_params)
            
            return jsonify({
                'message': 'Amazon Cognito Authentication Required',
                'instructions': [
                    '1. Copy the auth_url below',
                    '2. Open it in a web browser',
                    '3. Complete Cognito login',
                    '4. You will get a JSON response with your access_token',
                    '5. Copy the access_token to POSTMAN Authorization > Bearer Token'
                ],
                'auth_url': auth_url,
                'callback_url': f"{request.host_url}auth/callback",
                'note': 'After authentication, you can also GET /auth/token to retrieve your session token'
            })
        
        @flask_app.route('/auth/callback')
        def cognito_callback():
            """Handle Cognito SSO callback"""
            logger.info(f"Cognito callback received: {dict(request.args)}")
            
            # Verify state parameter
            received_state = request.args.get('state')
            session_state = session.get('oauth_state')
            
            if received_state != session_state:
                logger.error("Invalid state parameter in Cognito callback")
                return jsonify({'error': 'Invalid state parameter'}), 400
            
            # Get authorization code
            auth_code = request.args.get('code')
            if not auth_code:
                error = request.args.get('error', 'unknown_error')
                error_description = request.args.get('error_description', 'No authorization code received')
                return jsonify({
                    'error': error, 
                    'error_description': error_description,
                    'received_params': dict(request.args)
                }), 400
            
            try:
                # Exchange authorization code for tokens
                tokens = Authentication_Provider._exchange_code_for_tokens(auth_code)
                if not tokens:
                    return jsonify({'error': 'Failed to exchange code for tokens'}), 400
                
                # Validate and decode the ID token
                id_token = tokens.get('id_token')
                if not id_token:
                    return jsonify({'error': 'No ID token received'}), 400
                
                claims = Authentication_Provider.validate_cognito_token(id_token)
                if not claims:
                    return jsonify({'error': 'Invalid ID token'}), 400
                
                # Find or create user in database
                user = Authentication_Provider.get_or_create_user_from_claims(claims)
                if not user:
                    return jsonify({'error': 'User creation failed'}), 400
                
                # Store user info in session
                session['user_id'] = user.name
                session['user_email'] = user.email
                session['user_roles'] = [role.role_name for role in user.UserRoleList]
                session['authenticated'] = True
                session['access_token'] = tokens.get('access_token')
                session['id_token'] = id_token
                
                # Clean up OAuth session data
                session.pop('oauth_state', None)
                
                logger.info(f"User {user.name} successfully authenticated via Cognito SSO")
                
                return jsonify({
                    'success': True,
                    'message': 'Authentication successful',
                    'access_token': tokens.get('access_token'),
                    'token_type': 'Bearer',
                    'user_info': {
                        'user_id': user.name,
                        'email': user.email,
                        'roles': [role.role_name for role in user.UserRoleList]
                    },
                    'postman_setup': {
                        'instruction': 'Copy the access_token value below',
                        'authorization_type': 'Bearer Token',
                        'token_location': 'Headers > Authorization > Bearer {access_token}'
                    }
                })
                
            except Exception as e:
                logger.error(f"Error processing Cognito callback: {e}")
                return jsonify({'error': 'Authentication failed', 'details': str(e)}), 500
        
        @flask_app.route('/auth/logout')
        def cognito_logout():
            """Logout from Cognito SSO"""
            session.clear()
            
            logout_params = {
                'client_id': Args.instance.cognito_client_id,
                'logout_uri': f"{request.host_url}"
            }
            
            logout_url = f"{Args.instance.cognito_domain}/logout?" + urllib.parse.urlencode(logout_params)
            
            logger.info("User logged out, redirecting to Cognito logout")
            return redirect(logout_url)
        
        @flask_app.route('/auth/token', methods=['GET'])
        def get_session_token():
            """Get access token from current session for API testing"""
            if 'user_id' not in session or 'access_token' not in session:
                return jsonify({
                    'error': 'Not authenticated',
                    'message': 'Please login first at /auth/login'
                }), 401
            
            return jsonify({
                'access_token': session.get('access_token'),
                'token_type': 'Bearer',
                'user_id': session.get('user_id'),
                'user_email': session.get('user_email'),
                'user_roles': session.get('user_roles', []),
                'expires_in': 3600,
                'usage': {
                    'postman_setup': 'Copy the access_token value to Authorization > Bearer Token',
                    'curl_example': f'curl -H "Authorization: Bearer {session.get("access_token", "TOKEN_HERE")}" http://localhost:5656/api/COMPANYTB'
                }
            })

        @flask_app.route('/auth/debug')
        def cognito_debug():
            """Debug endpoint to check Cognito configuration and troubleshoot 403 errors"""
            try:
                return jsonify({
                    'cognito_configuration': {
                        'region': getattr(Args.instance, 'cognito_region', 'NOT_SET'),
                        'user_pool_id': getattr(Args.instance, 'cognito_user_pool_id', 'NOT_SET'),
                        'client_id': getattr(Args.instance, 'cognito_client_id', 'NOT_SET')[:8] + '...' if getattr(Args.instance, 'cognito_client_id', None) else 'NOT_SET',
                        'domain': getattr(Args.instance, 'cognito_domain', 'NOT_SET'),
                        'redirect_uri': getattr(Args.instance, 'cognito_redirect_uri', 'NOT_SET'),
                    },
                    'current_request': {
                        'host': request.host,
                        'host_url': request.host_url,
                        'url': request.url,
                        'scheme': request.scheme
                    },
                    'session_info': {
                        'session_keys': list(session.keys()) if session else [],
                        'oauth_state': session.get('oauth_state', 'NOT_SET') if session else 'NO_SESSION',
                        'authenticated': session.get('authenticated', False) if session else False
                    },
                    'troubleshooting': {
                        'expected_callback_url': f"{request.host_url}auth/callback",
                        'current_redirect_uri_config': getattr(Args.instance, 'cognito_redirect_uri', 'NOT_SET'),
                        'match': f"{request.host_url}auth/callback" == getattr(Args.instance, 'cognito_redirect_uri', 'NOT_SET'),
                        'common_issues': [
                            '1. Redirect URI mismatch - must match exactly in Cognito app client',
                            '2. Domain not configured in Cognito',
                            '3. Client ID/Secret incorrect',
                            '4. User Pool ID incorrect',
                            '5. App client not properly configured'
                        ]
                    }
                })
            except Exception as e:
                return jsonify({
                    'error': 'Configuration check failed',
                    'details': str(e),
                    'message': 'Check your Cognito environment variables'
                }), 500

    @staticmethod
    def _exchange_code_for_tokens(auth_code: str) -> Optional[Dict[str, str]]:
        """Exchange authorization code for access and ID tokens"""
        from config.config import Args
        
        try:
            token_url = f"{Args.instance.cognito_domain}/oauth2/token"
            
            # Create client secret hash for Cognito
            client_secret_hash = Authentication_Provider._calculate_secret_hash(
                Args.instance.cognito_client_id,
                Args.instance.cognito_client_secret,
                Args.instance.cognito_client_id  # username for client credentials
            )
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'grant_type': 'authorization_code',
                'client_id': Args.instance.cognito_client_id,
                'client_secret': Args.instance.cognito_client_secret,
                'code': auth_code,
                'redirect_uri': Args.instance.cognito_redirect_uri
            }
            
            response = requests.post(token_url, headers=headers, data=data, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Token exchange failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error exchanging code for tokens: {e}")
            return None

    @staticmethod
    def _calculate_secret_hash(client_id: str, client_secret: str, username: str) -> str:
        """Calculate SECRET_HASH for Cognito client authentication"""
        message = username + client_id
        dig = hmac.new(
            client_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()

    @staticmethod
    def validate_cognito_token(token: str) -> Optional[Dict[str, Any]]:
        """Validate a Cognito JWT token"""
        from config.config import Args
        
        try:
            # Get Cognito JWKS
            region = Args.instance.cognito_region
            user_pool_id = Args.instance.cognito_user_pool_id
            
            jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
            
            logger.info(f"Fetching Cognito JWKS from: {jwks_url}")
            
            jwks_response = requests.get(jwks_url, timeout=10)
            if jwks_response.status_code != 200:
                logger.error(f"Could not retrieve Cognito JWKS: {jwks_response.status_code}")
                return None
            
            jwks_data = jwks_response.json()
            
            # Get the signing key
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")
            
            signing_key = None
            for key in jwks_data.get("keys", []):
                if key.get("kid") == kid:
                    signing_key = key
                    break
            
            if not signing_key:
                logger.error(f"Signing key not found in Cognito JWKS for kid: {kid}")
                return None
            
            # Convert JWK to PEM format for PyJWT
            public_key = RSAAlgorithm.from_jwk(signing_key)
            
            # Validate token
            claims = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=Args.instance.cognito_client_id,
                options={
                    "verify_exp": True,
                    "verify_iat": True,
                    "verify_aud": True,
                    "verify_iss": True
                },
                issuer=f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}",
                leeway=timedelta(minutes=2)
            )
            
            logger.info(f"Successfully validated Cognito token for user: {claims.get('sub', 'unknown')}")
            return claims
            
        except jwt.ExpiredSignatureError:
            logger.error("Cognito token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid Cognito token: {e}")
            return None
        except Exception as e:
            logger.error(f"Error validating Cognito token: {e}")
            return None

    @staticmethod
    def get_or_create_user_from_claims(claims: dict) -> object:
        """Create user from Cognito claims"""
        rtn_user = DotMapX()
        
        # Cognito standard claims
        rtn_user.name = claims.get("email") or claims.get("sub")
        rtn_user.email = claims.get("email")
        rtn_user.given_name = claims.get("given_name")
        rtn_user.family_name = claims.get("family_name")
        rtn_user.id = claims.get("sub")
        rtn_user.password_hash = None
        
        # Handle Cognito groups/roles
        rtn_user.UserRoleList = []
        
        # Cognito uses 'cognito:groups' claim for roles
        role_names = []
        if "cognito:groups" in claims:
            role_names = claims["cognito:groups"]
        elif "groups" in claims:
            role_names = claims["groups"]
        
        for each_role_name in role_names:
            each_user_role = DotMapX()
            each_user_role.role_name = each_role_name
            rtn_user.UserRoleList.append(each_user_role)
            
        return rtn_user

    @staticmethod
    def get_user(id: str, password: str = "") -> object:
        """Get user for Cognito authentication"""
        jwt_data = {}
        
        if isinstance(password, dict):
            jwt_data = password
        elif isinstance(password, str) and password.startswith('eyJ'):
            jwt_data = Authentication_Provider.validate_cognito_token(password)
            if not jwt_data:
                rtn_user = DotMapX()
                rtn_user.id = id
                rtn_user.name = id
                rtn_user.email = None
                rtn_user.UserRoleList = []
                return rtn_user
        elif not password:
            rtn_user = DotMapX()
            rtn_user.id = id
            rtn_user.name = id
            rtn_user.email = None
            rtn_user.UserRoleList = []
            return rtn_user
        
        # Get user/roles from Cognito JWT data
        rtn_user = Authentication_Provider.get_or_create_user_from_claims(jwt_data)
        
        if not rtn_user.name:
            rtn_user.name = id
        if not hasattr(rtn_user, 'id') or not rtn_user.id:
            rtn_user.id = id
            
        return rtn_user

    @staticmethod
    def check_password(user: object, password: str) -> bool:
        """Check password for Cognito authentication"""
        if not password:
            from flask import has_request_context
            if has_request_context() and 'user_id' in session:
                return True
            return False
        
        if isinstance(password, str) and password.startswith('eyJ'):
            # Try Cognito validation
            claims = Authentication_Provider.validate_cognito_token(password)
            if claims:
                token_user_id = claims.get('sub') or claims.get('email')
                user_id = getattr(user, 'id', None) or getattr(user, 'name', None)
                return token_user_id == user_id
            
            # Try internal token validation
            try:
                from flask_jwt_extended import decode_token
                internal_claims = decode_token(password)
                if internal_claims:
                    token_user_id = internal_claims.get('sub')
                    user_id = getattr(user, 'id', None) or getattr(user, 'name', None)
                    return token_user_id == user_id
            except Exception:
                pass
            
            return False
            
        return True

    @staticmethod
    def get_sso_login_url() -> str:
        """Get the Cognito SSO login URL"""
        from flask import request
        return f"{request.host_url}auth/login"
    
    @staticmethod
    def is_authenticated(request) -> bool:
        """Check if the current request is authenticated"""
        return 'user_id' in session and 'access_token' in session
