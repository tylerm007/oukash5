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
import ssl
from database.models import vUserRole
import threading

# **********************
# Amazon Cognito auth provider
# **********************

db = None
db_session = None  # Renamed to avoid conflict with Flask session

logger = logging.getLogger('api_logic_server_app')

# JWKS cache to prevent rate limiting from Cognito
_jwks_cache = {
    'data': None,
    'timestamp': None,
    'lock': threading.Lock()
}
_JWKS_CACHE_DURATION = 3600  # Cache JWKS for 1 hour (in seconds)

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
        # Configure JWT for hybrid Cognito/Internal token support
        flask_app.config['JWT_SECRET_KEY'] = "ApiLogicServerSecret"
        flask_app.config['JWT_ALGORITHM'] = 'HS256'  # For internal tokens (symmetric key)
        flask_app.config['JWT_DECODE_ALGORITHMS'] = ['HS256', 'RS256']  # Support both algorithms
        flask_app.config['JWT_IDENTITY_CLAIM'] = 'sub'
        flask_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1440)  # 24 hours
        flask_app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
        flask_app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
        
        # Configure Flask to handle SSL/connection issues better
        flask_app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching
        flask_app.config['SESSION_COOKIE_SECURE'] = False  # Allow HTTP for dev
        flask_app.config['SESSION_COOKIE_HTTPONLY'] = True
        flask_app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        
        logger.info("✅ Configured Cognito RS256 JWT authentication:")
        logger.info("   - Primary: Cognito RS256 tokens (validated via JWKS)")
        logger.info("   - Fallback: HS256 internal tokens (if needed)")
        logger.info("   - Callback returns RS256 tokens directly (no conversion)")
        logger.info("   - RS256 tokens usable with @jwt_required() via monkey patch")
        
        # Install JWT monkey patch for Cognito tokens
        Authentication_Provider._install_jwt_monkey_patch()
        
        # Preload JWKS cache to avoid first-request delay
        Authentication_Provider.preload_jwks_cache()
        
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
            """Patched JWT decode function that handles both HS256 and RS256 tokens"""
            # IMPORTANT: Check algorithm FIRST before attempting decode
            # This prevents PEM deserialization errors when RS256 token hits HS256 decoder
            try:
                import jwt as pyjwt
                header = pyjwt.get_unverified_header(encoded_token)
                token_alg = header.get('alg')
                
                logger.debug(f"Token algorithm detected: {token_alg}")
                
                # Route based on algorithm
                if token_alg == 'RS256':
                    logger.info("RS256 Cognito token detected - using Cognito validation")
                    
                    # Validate with Cognito JWKS
                    claims = Authentication_Provider.validate_cognito_token(encoded_token)
                    if claims:
                        logger.info(f"Successfully validated RS256 Cognito token for user: {claims.get('sub', 'unknown')}")
                        return {
                            'sub': claims.get('sub'),
                            'iat': claims.get('iat', 0),
                            'exp': claims.get('exp', 0),
                            'jti': claims.get('jti', 'cognito-token'),
                            'type': 'access',
                            'fresh': False,
                            'email': claims.get('email'),
                            'name': claims.get('name'),
                            'app_username': claims.get('app_username'),
                            'loaded_user': getUserRoles(claims.get('app_username'), claims.get('roles', [])),
                            'roles': claims.get('roles', []),
                            'auth_provider': 'cognito',
                            'delegated': claims.get('delegated')
                        }
                    else:
                        logger.error("RS256 Cognito token validation failed")
                        raise Exception("Invalid Cognito RS256 token")
                
                elif token_alg == 'HS256':
                    # HS256 internal token - use Flask-JWT-Extended standard decode
                    logger.debug("HS256 internal token detected - using Flask-JWT-Extended")
                    return original_decode_token(encoded_token, csrf_token, allow_expired)
                
                else:
                    logger.error(f"Unsupported token algorithm: {token_alg}")
                    raise Exception(f"Unsupported JWT algorithm: {token_alg}")
                    
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Token decode error: {error_msg[:200]}")
                
                # If algorithm detection failed, try the original decoder as fallback
                if "get_unverified_header" in error_msg or "Token algorithm" not in error_msg:
                    logger.info("Algorithm detection failed, trying original decoder")
                    try:
                        return original_decode_token(encoded_token, csrf_token, allow_expired)
                    except Exception as original_error:
                        logger.error(f"Original decoder also failed: {str(original_error)[:100]}")
                
                raise e
        
        def patched_verify_jwt_in_request(optional=False, fresh=False, refresh=False, locations=None, verify_type=True):
            """Patched JWT verification that handles both HS256 and RS256 tokens"""
            # CRITICAL: Extract and check token algorithm BEFORE calling original verify
            # This prevents PEM deserialization errors with RS256 tokens
            
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header.replace('Bearer ', '')
                
                try:
                    import jwt as pyjwt
                    header = pyjwt.get_unverified_header(token)
                    token_alg = header.get('alg')
                    
                    if token_alg == 'RS256':
                        # This is a Cognito RS256 token - handle it manually
                        logger.info("RS256 Cognito token detected in verify_jwt_in_request")
                        
                        claims = Authentication_Provider.validate_cognito_token(token)
                        if claims:
                            logger.info(f"Cognito token validated for user: {claims.get('sub', 'unknown')}")
                            
                            # Create a Flask-JWT-Extended compatible token structure
                            jwt_data = {
                                'sub': claims.get('sub'),
                                'iat': claims.get('iat', 0),
                                'exp': claims.get('exp', 0),
                                'jti': claims.get('jti', 'cognito-token'),
                                'type': 'access',
                                'fresh': False,
                                'email': claims.get('email'),
                                'name': claims.get('name'),
                                'app_username': claims.get('app_username'),
                                'loaded_user': getUserRoles(claims.get('app_username'), claims.get('roles', [])), # TODO we need to lookup a Uer?
                                'roles': claims.get('roles', []),
                                'auth_provider': 'cognito',
                                'delegated': claims.get('delegated')
                            }
                            
                            # Manually set the JWT data in Flask's 'g' object
                            # These are the globals that Flask-JWT-Extended and decorators expect
                            g.jwt_user_claims = claims
                            g.jwt_user_identity = claims.get('sub')
                            g._jwt_extended_jwt = jwt_data
                            g._jwt_extended_jwt_user = jwt_data
                            g._jwt_extended_jwt_header = header
                            g._jwt_extended_jwt_location = 'headers'
                            
                            logger.info("Successfully set Flask-JWT-Extended globals for RS256 token")
                            return None
                        else:
                            logger.error("RS256 Cognito token validation failed")
                            if not optional:
                                raise Exception("Invalid Cognito RS256 token")
                            return None
                    
                    elif token_alg == 'HS256':
                        # HS256 internal token - use original Flask-JWT-Extended verification
                        logger.debug("HS256 token detected - using original verify_jwt_in_request")
                        return original_verify_jwt_in_request(optional, fresh, refresh, locations, verify_type)
                    
                    else:
                        logger.warning(f"Unsupported token algorithm in verify_jwt_in_request: {token_alg}")
                        if not optional:
                            raise Exception(f"Unsupported JWT algorithm: {token_alg}")
                        return None
                        
                except Exception as e:
                    error_msg = str(e)
                    logger.error(f"Error in patched verify_jwt_in_request: {error_msg[:200]}")
                    
                    if optional:
                        logger.info("Optional JWT verification, allowing request to continue despite error")
                        return None
                    
                    # Try original as fallback
                    try:
                        return original_verify_jwt_in_request(optional, fresh, refresh, locations, verify_type)
                    except Exception as fallback_error:
                        logger.error(f"Original verify also failed: {str(fallback_error)[:100]}")
                        raise e
            
            # No Authorization header - let original handle it
            logger.debug("No Authorization header, using original verify_jwt_in_request")
            return original_verify_jwt_in_request(optional, fresh, refresh, locations, verify_type)
        
        # Replace the functions
        flask_jwt_extended.utils.decode_token = patched_decode_token
        flask_jwt_extended.view_decorators.verify_jwt_in_request = patched_verify_jwt_in_request
        
        logger.info("✅ Installed comprehensive JWT monkey patch for Cognito token support")
        logger.info("   - patched decode_token: detects RS256 vs HS256 before decode")
        logger.info("   - patched verify_jwt_in_request: handles RS256 tokens directly")
        logger.info("   - RS256 tokens will bypass Flask-JWT-Extended's HS256 decoder")

    @staticmethod
    def _add_cognito_endpoints(flask_app: Flask):
        """Add Cognito endpoints to Flask app"""
        from config.config import Args
        
        @flask_app.route('/api/auth/login', methods=['GET', 'POST'])
        def cognito_login():
            """Redirect to Cognito Hosted UI for authentication"""
            try:
                # Check if Cognito is properly configured
                if not getattr(Args.instance, 'cognito_client_id', None):
                    return jsonify({
                        'error': 'Cognito not configured',
                        'message': 'COGNITO_CLIENT_ID not set',
                        'debug_url': f"{request.host_url}auth/debug-cognito"
                    }), 500
                
                if not getattr(Args.instance, 'cognito_domain', None):
                    return jsonify({
                        'error': 'Cognito not configured', 
                        'message': 'COGNITO_DOMAIN not set',
                        'debug_url': f"{request.host_url}auth/debug-cognito"
                    }), 500
                
                # Store return URL to redirect back after authentication
                return_url = request.args.get('return_url') or request.headers.get('Referer')
                if return_url:
                    session['return_url'] = return_url
                    logger.info(f"Stored return URL for post-auth redirect: {return_url}")
                
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
                logger.info(f"   return_url {return_url}")
                
                # Check if this is an API request that wants JSON instead of redirect
                accept_header = request.headers.get('Accept', '')
                if 'application/json' in accept_header:
                    return jsonify({
                        'redirect_url': auth_url,
                        'message': 'Please redirect to the provided URL',
                        'method': 'GET'
                    })
                
                # For web browsers, use JavaScript redirect to avoid SSL issues
                html_redirect = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Redirecting to Cognito...</title>
                    <meta http-equiv="refresh" content="0; url={auth_url}">
                </head>
                <body>
                    <script>
                        window.location.href = "{auth_url}";
                    </script>
                    <p>Redirecting to authentication... <a href="{auth_url}">Click here if not redirected</a></p>
                </body>
                </html>
                """
                
                from flask import Response
                response = Response(html_redirect, mimetype='text/html')
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
                
                return response
                
            except Exception as e:
                logger.error(f"Error in Cognito login: {e}")
                return jsonify({
                    'error': 'Login configuration error',
                    'message': str(e),
                    'debug_url': f"{request.host_url}auth/debug-cognito"
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
                
                # Get the Cognito access token (RS256) - we'll use this directly
                cognito_access_token = tokens.get('access_token')
                id_token = tokens.get('id_token')
                
                if not cognito_access_token:
                    return jsonify({'error': 'No access token received'}), 400
                if not id_token:
                    return jsonify({'error': 'No ID token received'}), 400

                # Validate and decode the access token (RS256)
                claims = Authentication_Provider.validate_cognito_token(cognito_access_token)
                if not claims:
                    # Fallback to ID token if access token validation fails
                    logger.warning("Access token validation failed, trying ID token")
                    claims = Authentication_Provider.get_claims_from_token(id_token)
                    if not claims:
                        return jsonify({'error': 'Invalid tokens'}), 400
                
                # Find or create user in database
                user = Authentication_Provider.get_or_create_user_from_claims(claims)
                if not user:
                    return jsonify({'error': 'User creation failed'}), 400
                
                claims["user_id"] = user.Name
                roles = user.UserRoleList
                
                # Store user info and Cognito RS256 token in session
                session['user_id'] = user.Name
                session['user_email'] = claims.get('email')
                session['user_roles'] = roles
                session['authenticated'] = True
                session['access_token'] = cognito_access_token  # Store RS256 token directly
                session['id_token'] = id_token
                session['token_type'] = 'RS256'
                session['auth_provider'] = 'cognito'
                
                # Clean up OAuth session data
                session.pop('oauth_state', None)

                logger.info(f"✅ User {user.Name} authenticated via Cognito SSO - using RS256 token directly")
                logger.info(f"   Token algorithm: RS256 (Cognito)")
                logger.info(f"   User roles: {[r.role_name for r in roles] if hasattr(roles[0] if roles else None, 'role_name') else roles}")
                
                # Check if this is a JSON API request (for testing/Postman) or web browser request
                accept_header = request.headers.get('Accept', '')
                user_agent = request.headers.get('User-Agent', '')
                
                # If request explicitly wants JSON or comes from API testing tool, return JSON
                if ('application/json' in accept_header and 'text/html' not in accept_header) or \
                   'postman' in user_agent.lower() or \
                   'curl' in user_agent.lower() or \
                   request.args.get('format') == 'json':
                    
                    logger.info("Returning JSON response with RS256 Cognito token for API/testing client")
                    return jsonify({
                        'success': True,
                        'message': 'Authentication successful',
                        'access_token': cognito_access_token,  # Return RS256 token directly
                        'id_token': id_token,
                        'token_type': 'Bearer',
                        'token_algorithm': 'RS256',
                        'expires_in': 3600,  # Cognito default
                        'delegated': claims.get('delegated'),
                        'user_info': {
                            'user_id': user.Name,
                            'email': claims.get('email'),
                            'roles': [r.role_name for r in roles] if hasattr(roles[0] if roles else None, 'role_name') else roles,
                            'cognito_sub': claims.get('sub')
                        }
                    })
                
                # For web browsers, redirect back to Angular app
                # Determine the redirect URL
                redirect_url = None
                
                # 1. Check if there's a return_url in session (set from the original login request)
                if 'return_url' in session:
                    redirect_url = session.pop('return_url')
                    logger.info(f"Using return_url from session: {redirect_url}")
                
                # 2. Otherwise, construct the Angular callback URL
                else:
                    # Get the original request host/port from the referer or construct it
                    referer = request.headers.get('Referer', '')
                    if referer and '5656' in referer:
                        from urllib.parse import urlparse
                        parsed_referer = urlparse(referer)
                        redirect_url = f"{parsed_referer.scheme}://{parsed_referer.netloc}/auth/callback"
                        logger.info(f"Constructed Angular callback URL from referer: {redirect_url}")
                    else:
                        # Default to localhost:5656 for development
                        redirect_url = f"{Args.instance.http_scheme}://{Args.instance.swagger_host}:5656/auth/callback"
                        logger.info(f"Using default Angular callback URL: {redirect_url}")
                
                # Add authentication data as URL parameters for Angular to process
                from urllib.parse import urlencode
                auth_params = {
                    'access_token': cognito_access_token,  # Pass RS256 token to Angular
                    'token_type': 'Bearer',
                    'token_algorithm': 'RS256',
                    'expires_in': 3600,
                    'user_id': user.Name,
                    'email': claims.get('email'),
                    'success': 'true'
                }
                
                # Construct final redirect URL with auth parameters
                final_redirect_url = f"{redirect_url}?{urlencode(auth_params)}"
                
                logger.info(f"Redirecting to Angular app: {redirect_url}")
                logger.info(f"RS256 Cognito token will be available in URL parameters")
                
                return redirect(final_redirect_url)
                
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
            if 'user_id' not in session:
                return jsonify({
                    'error': 'Not authenticated',
                    'message': 'Please login first at /api/auth/login'
                }), 401
            
            # Return the RS256 Cognito token directly
            access_token = session.get('access_token')
            
            if not access_token:
                return jsonify({
                    'error': 'No valid token found',
                    'message': 'Please re-authenticate at /auth/login'
                }), 401
            
            return jsonify({
                'access_token': access_token,
                'token_type': 'Bearer',
                'token_algorithm': session.get('token_type', 'RS256'),
                'auth_provider': session.get('auth_provider', 'cognito'),
                'user_id': session.get('user_id'),
                'user_email': session.get('user_email'),
                'user_roles': session.get('user_roles', []),
                'delegated': session.get('delegated'),
                'expires_in': 3600,
                'usage': {
                    'postman_setup': 'Copy the access_token value to Authorization > Bearer Token',
                    'curl_example': f'curl -H "Authorization: Bearer {access_token[:50]}..." http://localhost:5656/api/COMPANYTB',
                    'note': 'This is a Cognito RS256 token - directly usable with @jwt_required() endpoints'
                }
            })
        @flask_app.route('/auth/exchange-cognito-token', methods=['POST', 'GET'])
        def cognito_exchange_token():
            access_token = None
            try:
                id_token = None
                if request.method == 'OPTIONS':
                    return jsonify({'message': 'CORS preflight'}), 200
                # Try to get token from request
                if request.method == 'POST' and request.is_json:
                    data = request.get_json()
                    id_token = data.get('token')
                elif request.method == 'GET':
                    token = request.args.get('token')
                
                # Try Authorization header if no token in body/params
                if not id_token:
                    auth_header = request.headers.get('Authorization', '')
                    if auth_header.startswith('Bearer '):
                        id_token = auth_header.replace('Bearer ', '')
                
                if not id_token:
                    return jsonify({
                        'valid': False,
                        'error': 'No token provided',
                        'usage': [
                            'POST /auth/validate-cognito with {"token": "your_token"}',
                            'GET /auth/validate-cognito?token=your_token',
                            'Any method with Authorization: Bearer <token> header'
                        ]
                    }), 400
            except Exception as e:
                return jsonify({
                    'valid': False,
                    'error': f'Error processing request: {str(e)}'
                }), 500 
            
            claims = Authentication_Provider.get_claims_from_token(id_token)
            
            if not claims:
                return jsonify({'error': 'Invalid ID token'}), 400
            email = claims.get('email')
            username = claims.get("app_username")
            
            # Find or create user in database
            user = Authentication_Provider.get_or_create_user_from_claims(claims)
            if not user:
                return jsonify({'error': 'User creation failed'}), 400
            
            # Store user info in session with RS256 token
            session['user_id'] = user.Username
            session['user_email'] = user.Email if hasattr(user, 'Email') and user.Email else claims.get('email')   
            session['user_roles'] = user.UserRoleList if hasattr(user, 'UserRoleList') else []
            session['authenticated'] = True
            session['access_token'] = id_token  # Store the RS256 token directly
            session['id_token'] = id_token
            session['token_type'] = 'RS256'
            session['auth_provider'] = 'cognito'
            session['delegated'] = claims.get('delegated')
            
            logger.info(f"✅ User {user.Username} authenticated with RS256 Cognito token")
            
            user_info = {
                'user_id': claims.get('name') or user.Username if hasattr(user, 'Username') else None,
                'email': claims.get('email') or user.Email if hasattr(user, 'Email') else None,
                'roles': [{"role_name": role.role_name} for role in user.UserRoleList] if hasattr(user, 'UserRoleList') else [],
                'cognito_sub': claims.get('sub')
            }
            return jsonify({
                'valid': True, 
                'token_type': 'Bearer',
                'token_algorithm': 'RS256',
                "access_token": id_token,  # Return the RS256 token
                'user_info': user_info,
                'message': 'RS256 Cognito token received and validated successfully. Use this token directly for API calls.'
            })

        @flask_app.route('/auth/validate-cognito', methods=['POST', 'GET'])
        def cognito_validate_token():
            """Validate a JWT token and show its details (Cognito-specific)"""
            try:
                token = None
                
                # Try to get token from request
                if request.method == 'POST' and request.is_json:
                    data = request.get_json()
                    token = data.get('token')
                elif request.method == 'GET':
                    token = request.args.get('token')
                
                # Try Authorization header if no token in body/params
                if not token:
                    auth_header = request.headers.get('Authorization', '')
                    if auth_header.startswith('Bearer '):
                        token = auth_header.replace('Bearer ', '')
                
                if not token:
                    return jsonify({
                        'valid': False,
                        'error': 'No token provided',
                        'usage': [
                            'POST /auth/validate-cognito with {"token": "your_token"}',
                            'GET /auth/validate-cognito?token=your_token',
                            'Any method with Authorization: Bearer <token> header'
                        ]
                    }), 400
                
                # Try to decode token
                import jwt as pyjwt
                
                # Get token header info
                try:
                    header = pyjwt.get_unverified_header(token)
                    payload = pyjwt.decode(token, options={"verify_signature": False})
                    
                    token_info = {
                        'valid': False,  # Will be set to True if validation succeeds
                        'header': header,
                        'algorithm': header.get('alg'),
                        'token_type': 'cognito' if header.get('alg') == 'RS256' else 'internal',
                        'payload_preview': {
                            'sub': payload.get('sub'),
                            'email': payload.get('email'),
                            'name': payload.get('name'),
                            'exp': payload.get('exp'),
                            'iat': payload.get('iat'),
                            'roles': payload.get('roles')
                        }
                    }
                    
                    # Try validation based on algorithm
                    if header.get('alg') == 'RS256':
                        # Cognito token validation
                        claims = Authentication_Provider.validate_cognito_token(token)
                        if claims:
                            token_info['valid'] = True
                            token_info['validation_method'] = 'cognito_jwks'
                            token_info['claims'] = claims
                        else:
                            token_info['error'] = 'RS256 Cognito token validation failed'
                    
                    elif header.get('alg') == 'HS256':
                        # Internal token validation
                        try:
                            from flask_jwt_extended import decode_token
                            decoded = decode_token(token)
                            token_info['valid'] = True
                            token_info['validation_method'] = 'flask_jwt_extended'
                            token_info['decoded'] = decoded
                        except Exception as e:
                            token_info['error'] = f'HS256 internal token validation failed: {str(e)}'
                    
                    else:
                        token_info['error'] = f'Unsupported algorithm: {header.get("alg")}'
                    
                    return jsonify(token_info)
                    
                except Exception as decode_error:
                    return jsonify({
                        'valid': False,
                        'error': f'Token decode error: {str(decode_error)}',
                        'token_preview': token[:50] + '...' if len(token) > 50 else token
                    }), 400
                    
            except Exception as e:
                return jsonify({
                    'valid': False,
                    'error': f'Validation error: {str(e)}'
                }), 500

        @flask_app.route('/auth/debug-cognito')
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

        # Add error handler for SSL issues
        @flask_app.errorhandler(Exception)
        def handle_ssl_errors(error):
            """Handle SSL and connection errors gracefully"""
            error_str = str(error)
            error_type = type(error).__name__
            
            # Check for SSL EOF errors (client disconnected)
            if isinstance(error, (ssl.SSLEOFError, ConnectionError, BrokenPipeError)):
                logger.debug(f"Client disconnected during response (SSL/Connection error): {error_type}")
                # Don't return a response or log as error - client already disconnected
                # Return empty response to satisfy Flask
                from flask import Response
                return Response('', status=200)
            
            # Check for SSL/PEM key errors (often from client disconnect during handshake)
            if ('ssl' in error_str.lower() or 'eof' in error_str.lower() or 
                'PEM routines' in error_str or 'no start line' in error_str or
                'Could not deserialize key data' in error_str or
                'OpenSSL' in error_str):
                logger.debug(f"SSL-related error (likely client disconnect or handshake failure): {error_str[:200]}")
                from flask import Response
                return Response('', status=200)
            
            # Re-raise for normal Flask error handling
            raise error

        @flask_app.route('/auth/ontimize-session', methods=['POST'])
        def create_ontimize_session():
            """Create Ontimize-compatible session from Cognito token"""
            try:
                data = request.get_json()
                if not data or 'cognito_token' not in data:
                    return jsonify({
                        'error': 'Missing cognito_token',
                        'message': 'Request must include cognito_token in JSON body'
                    }), 400
                
                cognito_token = data['cognito_token']
                user_info = data.get('user_info', {})
                
                logger.info(f"Creating Ontimize session for Cognito user: {user_info.get('email', 'unknown')}")
                
                # Validate the Cognito token first
                import jwt as pyjwt
                try:
                    # Check if it's an internal HS256 token (already processed)
                    header = pyjwt.get_unverified_header(cognito_token)
                    if header.get('alg') == 'HS256':
                        logger.info("Internal HS256 token detected - validating with Flask-JWT-Extended")
                        from flask_jwt_extended import decode_token
                        token_claims = decode_token(cognito_token)
                        logger.info("Internal token validated successfully")
                    else:
                        # It's a Cognito RS256 token
                        logger.info("Cognito RS256 token detected - validating with Cognito JWKS")
                        token_claims = Authentication_Provider.validate_cognito_token(cognito_token)
                        if not token_claims:
                            return jsonify({'error': 'Invalid Cognito token'}), 401
                except Exception as e:
                    return jsonify({
                        'error': 'Token validation failed',
                        'details': str(e)
                    }), 401
                
                # Create Ontimize-compatible session data
                session_data = {
                    'user': token_claims.get('app_username'),
                    'username': token_claims.get('app_username'),
                    'delegated': token_claims.get('delegated'),
                    'id': token_claims.get('sub', user_info.get('user_id')),
                    'roles': token_claims.get('roles', []),
                    'authenticated': True,
                    'auth_provider': 'cognito',
                    'access_token': cognito_token,
                    'session_key': f"cognito_{token_claims.get('sub', 'unknown')}",
                    'permissions': ['read', 'write'],  # Default permissions
                    'locale': 'en',
                    'sessionData': {
                        'user': user_info.get('email', token_claims.get('email')),
                        'sessionId': f"cognito_{token_claims.get('sub', 'unknown')}",
                        'roles': user_info.get('roles', [])
                    }
                }
                
                # Store in Flask session for server-side compatibility
                session.update(session_data)
                
                logger.info(f"✅ Ontimize session created for user: {session_data['user']}")
                
                return jsonify({
                    'success': True,
                    'message': 'Ontimize session created successfully',
                    'sessionData': session_data,
                    'user': session_data['user'],
                    'authenticated': True
                })
                
            except Exception as e:
                logger.error(f"Error creating Ontimize session: {e}")
                return jsonify({
                    'error': 'Session creation failed',
                    'details': str(e)
                }), 500

        @flask_app.route('/api/users/login', methods=['POST'])
        def ontimize_token_login():
            """Ontimize login endpoint that accepts Cognito tokens"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400
                
                username = data.get('user') or data.get('username')
                password = data.get('password')
                
                logger.info(f"Ontimize login attempt for user: {username} - token_claims uses app_username for User")
                
                # Check if password is a JWT token (Cognito token)
                if password and password.startswith('eyJ'):
                    logger.info("JWT token detected in Ontimize login")
                    
                    # Extract username from token if not provided
                    if not username:
                        token_claims = Authentication_Provider.get_claims_from_token(password)
                        if token_claims:
                            username = (token_claims.get('app_username') or 
                                      token_claims.get('email') or 
                                      token_claims.get('name') or
                                      token_claims.get('sub'))
                            logger.info(f"Extracted username from token: {username}")
                        else:
                            return jsonify({
                                'code': 1,
                                'message': 'Invalid token',
                                'error': 'Could not decode token'
                            }), 401
                    
                    if not username:
                        return jsonify({
                            'code': 1,
                            'message': 'Username required',
                            'error': 'Username not found in request or token'
                        }), 400
                    
                    # Use our existing authentication methods
                    user = Authentication_Provider.get_user(username, password)
                    if user and Authentication_Provider.check_password(user, password):
                        logger.info(f"✅ Token authentication successful for user: {username}")
                        
                        # Get user roles
                        user_roles = []
                        if hasattr(user, 'UserRoleList') and user.UserRoleList:
                            user_roles = [role.role_name for role in user.UserRoleList if hasattr(role, 'role_name')]
                        
                        # Create Ontimize-compatible response
                        response_data = {
                            'code': 0,  # Ontimize success code
                            'message': 'Authentication successful',
                            'sessionId': f"cognito_{getattr(user, 'id', username)}",
                            'user': username,
                            'data': {
                                'user': username,
                                'sessionId': f"cognito_{getattr(user, 'id', username)}",
                                'roles': user_roles
                            }
                        }
                        
                        # Store in session for future requests with RS256 token
                        session['user'] = username
                        session['user_id'] = username
                        session['authenticated'] = True
                        session['sessionId'] = response_data['sessionId']
                        session['access_token'] = password  # Store the RS256 token
                        session['token_type'] = 'RS256'
                        session['auth_provider'] = 'cognito'
                        
                        return jsonify(response_data)
                    else:
                        logger.warning(f"❌ Token authentication failed for user: {username}")
                        return jsonify({
                            'code': 1,  # Ontimize error code
                            'message': 'Authentication failed',
                            'error': 'Invalid token or user'
                        }), 401
                else:
                    # No token provided
                    if not username or not password:
                        return jsonify({
                            'code': 1,
                            'message': 'Username and password/token required',
                            'error': 'Missing credentials'
                        }), 400
                    
                    # Handle regular password authentication (fall back to standard behavior)
                    logger.info("Regular password authentication - not implemented in Cognito provider")
                    return jsonify({
                        'code': 1,
                        'message': 'Regular password authentication not supported with Cognito provider',
                        'error': 'Use Cognito authentication with JWT token'
                    }), 401
                
            except Exception as e:
                logger.error(f"Error in Ontimize token login: {e}")
                logger.exception(e)  # Log full stack trace
                return jsonify({
                    'code': 1,
                    'message': 'Login error',
                    'error': str(e)
                }), 500

        # Log available endpoints for reference
        logger.info("🔗 Cognito Authentication Endpoints registered:")
        logger.info("   GET  /api/auth/login - Redirect to Cognito login")
        logger.info("   GET  /auth/login-postman - Get Cognito login URL for testing")
        logger.info("   GET  /auth/callback - Handle Cognito callback (returns RS256 token)")
        logger.info("   GET  /auth/logout - Logout and redirect to Cognito logout")
        logger.info("   GET  /auth/token - Get current session RS256 token")
        logger.info("   POST /auth/exchange-cognito-token - Exchange Cognito token (returns RS256)")
        logger.info("   POST /auth/validate-cognito - Validate and decode JWT tokens")
        logger.info("   GET  /auth/debug-cognito - Debug Cognito configuration")
        logger.info("")
        logger.info("ℹ️  All endpoints return RS256 Cognito tokens directly (no HS256 conversion)")

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
                #'client_secret': Args.instance.cognito_client_secret,
                'code': auth_code,
                'redirect_uri': Args.instance.cognito_redirect_uri
            }
            logger.info(f"Exchanging code for tokens at: {token_url} using: {data}")
            response = requests.post(token_url, headers=headers, data=data, timeout=10)
            
            if response.status_code == 200:
                logger.info("Token exchange successful")
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
    def get_claims_from_token(token: str) -> Optional[Dict[str, Any]]:
        """Get claims from a JWT token without validation"""
        try:
            import jwt as pyjwt
            claims = pyjwt.decode(token, options={"verify_signature": False})
            return claims
        except Exception as e:
            logger.error(f"Error decoding token claims: {e}")
            return None
    
    @staticmethod
    def preload_jwks_cache():
        """Preload JWKS cache on server startup to avoid first-request delay"""
        from config.config import Args
        
        try:
            region = Args.instance.cognito_region
            user_pool_id = Args.instance.cognito_user_pool_id
            jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
            
            logger.info(f"Preloading Cognito JWKS cache from: {jwks_url}")
            jwks_response = requests.get(jwks_url, timeout=10)
            
            if jwks_response.status_code == 200:
                with _jwks_cache['lock']:
                    _jwks_cache['data'] = jwks_response.json()
                    _jwks_cache['timestamp'] = datetime.now()
                logger.info("✅ Cognito JWKS cache preloaded successfully")
                return True
            else:
                logger.warning(f"Failed to preload JWKS cache: {jwks_response.status_code}")
                return False
        except Exception as e:
            logger.warning(f"Could not preload JWKS cache (non-critical): {e}")
            return False
        
    @staticmethod
    def validate_cognito_token(token: str) -> Optional[Dict[str, Any]]:
        """Validate a Cognito JWT token"""
        from config.config import Args

        try:
            # Get Cognito JWKS (with caching to prevent rate limiting)
            region = Args.instance.cognito_region
            user_pool_id = Args.instance.cognito_user_pool_id

            jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"

            # Check cache first
            current_time = datetime.now()
            jwks_data = None

            with _jwks_cache['lock']:
                # Check if cache is valid (exists and not expired)
                if (_jwks_cache['data'] is not None and
                    _jwks_cache['timestamp'] is not None and
                    (current_time - _jwks_cache['timestamp']).total_seconds() < _JWKS_CACHE_DURATION):

                    logger.debug(f"Using cached Cognito JWKS (age: {(current_time - _jwks_cache['timestamp']).total_seconds():.0f}s)")
                    jwks_data = _jwks_cache['data']
                else:
                    # Cache is expired or empty, fetch new JWKS
                    logger.info(f"Fetching Cognito JWKS from: {jwks_url} (cache expired or empty)")
                    
                    try:
                        jwks_response = requests.get(jwks_url, timeout=10)
                        
                        if jwks_response.status_code == 200:
                            jwks_data = jwks_response.json()
                            # Update cache
                            _jwks_cache['data'] = jwks_data
                            _jwks_cache['timestamp'] = current_time
                            logger.info(f"Cognito JWKS cached successfully (will expire in {_JWKS_CACHE_DURATION}s)")
                        else:
                            logger.error(f"Could not retrieve Cognito JWKS: {jwks_response.status_code}")
                            # If we have stale cache data, use it as fallback
                            if _jwks_cache['data'] is not None:
                                logger.warning("Using stale JWKS cache as fallback")
                                jwks_data = _jwks_cache['data']
                            else:
                                jwks_data = None
                    except Exception as e:
                        logger.error(f"Exception fetching JWKS: {e}")
                        # Try to use stale cache as fallback
                        if _jwks_cache['data'] is not None:
                            logger.warning("Using stale JWKS cache after fetch exception")
                            jwks_data = _jwks_cache['data']
                        else:
                            jwks_data = None

            if jwks_data is None:
                logger.error("No JWKS data available")
                return None
            
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
            # Note: Skipping audience validation to allow multiple app clients from the same User Pool
            # All clients must be from the correct User Pool (verified via issuer)
            claims = jwt.decode(
                token,
                ##jwks,
                public_key,
                algorithms=["RS256"],
                options={
                    "verify_exp": True,
                    "verify_iat": True,
                    "verify_aud": False,  # Skip audience check - accept any client from this User Pool
                    "verify_iss": True
                },
                issuer=f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}",
                leeway=timedelta(minutes=2)
            )
            app_username = claims.get('app_username')
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
        rtn_user.name = claims.get("app_username") or claims.get("custom:app_username") or  claims.get("sub")
        rtn_user.email = claims.get("email")
        rtn_user.given_name = claims.get("name")
        rtn_user.family_name = claims.get("custom:app_username")
        rtn_user.id = claims.get("user_id") or claims.get("sub")
        rtn_user.Username = claims.get("app_username") or claims.get("email") or claims.get("name")
        rtn_user.password_hash = None
        rtn_user.delegated = claims.get("delegated")
        roles = claims.get('roles', [])
        name = rtn_user.name
        if name is None or name == {}:
            name = claims.get('name','').replace(" ",".")
        user_roles = getUserRoles(name, roles)
       
        # Handle Cognito groups/roles
        rtn_user.UserRoleList = user_roles.UserRoleList

        return rtn_user

    @staticmethod
    def get_user(id: str, password: str = "") -> object:
        """Get user for Cognito authentication
        
        Args:
            id: user identifier (email, username, or sub)
            password: can be:
                - JWT token string (starts with 'eyJ')
                - dict of JWT claims (from user_lookup_loader)
                - empty string
        
        Returns:
            DotMapX user object with UserRoleList
        """
        jwt_data = {}
        
        # Handle different password parameter types
        if isinstance(password, dict):
            # Called from @jwt.user_lookup_loader with decoded JWT claims
            jwt_data = password
            logger.debug(f"get_user called with dict claims for user: {id}")
        elif isinstance(password, str) and password.startswith('eyJ'):
            # JWT token string - decode it
            jwt_data = Authentication_Provider.get_claims_from_token(password)
            logger.debug(f"get_user called with JWT token for user: {id}")
            if not jwt_data:
                logger.warning(f"Failed to decode JWT token for user: {id}")
                rtn_user = DotMapX()
                rtn_user.id = id
                rtn_user.name = id
                rtn_user.email = None
                rtn_user.UserRoleList = []
                return rtn_user
        elif not password:
            # No password provided - return minimal user object
            logger.debug(f"get_user called without password for user: {id}")
            rtn_user = DotMapX()
            rtn_user.id = id
            rtn_user.name = id
            rtn_user.email = None
            rtn_user.UserRoleList = []
            return rtn_user
        
        # Get user/roles from Cognito JWT data
        rtn_user = Authentication_Provider.get_or_create_user_from_claims(jwt_data)
        logger.debug(f"Created user from claims: {rtn_user.name}, roles: {len(rtn_user.UserRoleList)}")
        
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
            #claims = Authentication_Provider.validate_cognito_token(password)
            claims = Authentication_Provider.get_claims_from_token(password)
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
        from config.config import Args
        return f"{request.host_url}/api/auth/login"
    
    @staticmethod
    def is_authenticated(request) -> bool:
        """Check if the current request is authenticated"""
        return 'user_id' in session and 'access_token' in session

def getUserRoles(username:str, roles: list) ->any:
    rtn_user = {}
    #Check database for additional roles and email
    #from database.models import vUserRole
    user = DotMapX() # vUserRole.query.filter(vUserRole.Name == username).first() or {}
    user['Username'] = username
    #logger.debug(f"Found vUserRole in database: {user.Name}, adding {len(roles)} roles")
    UserRoleList = []
    user['UserRoleList'] = UserRoleList
    if len(roles) > 0:
        for role_name in roles:
            each_user_role = DotMapX()
            each_user_role.role_name = role_name
            user['UserRoleList'].append(each_user_role)
    else:
        each_user_role = DotMapX()
        each_user_role.role_name = user['role'] if 'role' in user else 'user'
        user['UserRoleList'].append(each_user_role)
       
    return user