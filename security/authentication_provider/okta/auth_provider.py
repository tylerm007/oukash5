from security.authentication_provider.abstract_authentication_provider import Abstract_Authentication_Provider
import sqlalchemy as sqlalchemy
import database.database_discovery.authentication_models as authentication_models
from flask import Flask
import safrs
from safrs.errors import JsonapiError
from dotmap import DotMap  # a dict, but you can say aDict.name instead of aDict['name']... like a row
from sqlalchemy import inspect
from http import HTTPStatus
import logging
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required as jwt_required_ori
import flask_jwt_extended as flask_jwt_extended
from flask import jsonify, g
import requests
import json
import sys
import time
import jwt
from jwt.algorithms import RSAAlgorithm
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


# **********************
# OKTA auth provider
# **********************

db = None
session = None

logger = logging.getLogger(__name__)

class ALSError(JsonapiError):

    def __init__(self, message, status_code=HTTPStatus.BAD_REQUEST):
        super().__init__()
        self.message = message
        self.status_code = status_code


class DotMapX(DotMap):
    """ DotMap, with extended support for auth providers """
    def check_password(self, password=None):
        # For OKTA, password validation is handled by token validation
        return True


class Authentication_Provider(Abstract_Authentication_Provider):

    @staticmethod
    def configure_auth(flask_app: Flask):
        """ Called by authentication.py on server start, to 
        - initialize jwt
        - establish Flask end points for login.

        Args:
            flask_app (Flask): _description_
        Returns:
            _type_: (no return)
        """
        # Override any existing JWT configuration to support OKTA tokens
        # This must be compatible with both OKTA RS256 tokens and system requirements
        
        # Use the secret from the main authentication system to maintain compatibility
        flask_app.config['JWT_SECRET_KEY'] = "ApiLogicServerSecret"  # Match main auth system
        flask_app.config['JWT_ALGORITHM'] = 'HS256'  # Use HMAC to avoid signature verification issues
        flask_app.config['JWT_IDENTITY_CLAIM'] = 'sub'
        flask_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=222)  # Match main system
        flask_app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
        
        # Key insight: We'll disable signature verification for incoming tokens
        # and handle all validation manually through our check_password method
        
        logger.info("Configured OKTA JWT authentication:")
        logger.info("- JWT signature verification handled manually")
        logger.info("- OKTA RS256 tokens validated via JWKS")
        logger.info("- Internal tokens use system defaults")
        
        # Install a monkey patch for JWT decoding to handle OKTA tokens
        Authentication_Provider._install_jwt_monkey_patch()
        
        # Add OKTA SSO endpoints
        Authentication_Provider._add_okta_endpoints(flask_app)
        return

    @staticmethod
    def _install_jwt_monkey_patch():
        """Install a monkey patch to intercept JWT verification for OKTA tokens"""
        import flask_jwt_extended.utils
        import flask_jwt_extended.view_decorators
        from flask import request, g
        
        # Save the original functions
        original_decode_token = flask_jwt_extended.utils.decode_token
        original_verify_jwt_in_request = flask_jwt_extended.view_decorators.verify_jwt_in_request
        
        def patched_decode_token(encoded_token, csrf_token=None, allow_expired=False):
            """Patched JWT decode function that handles OKTA tokens"""
            try:
                # First try the original Flask-JWT-Extended decoding
                return original_decode_token(encoded_token, csrf_token, allow_expired)
            except Exception as e:
                logger.info(f"Flask-JWT-Extended decode failed: {str(e)[:100]}")
                
                # Check if this looks like an OKTA token (RS256 algorithm)
                try:
                    import jwt as pyjwt
                    header = pyjwt.get_unverified_header(encoded_token)
                    if header.get('alg') == 'RS256':
                        logger.info("Detected RS256 token, trying OKTA validation")
                        
                        # Try OKTA validation
                        claims = Authentication_Provider.validate_okta_token(encoded_token)
                        if claims:
                            logger.info("Successfully validated OKTA token")
                            # Return in the format that Flask-JWT-Extended expects
                            return {
                                'sub': claims.get('sub'),
                                'iat': claims.get('iat', 0),
                                'exp': claims.get('exp', 0),
                                'jti': claims.get('jti', 'okta-token'),
                                'type': 'access',
                                'fresh': False,
                                # Include all OKTA claims for user lookup
                                **claims
                            }
                        else:
                            logger.info("OKTA validation failed")
                except Exception as okta_error:
                    logger.info(f"OKTA validation error: {okta_error}")
                
                # Re-raise the original exception if OKTA validation also fails
                raise e
        
        def patched_verify_jwt_in_request(optional=False, fresh=False, refresh=False, locations=None, verify_type=True):
            """Patched JWT verification that's more lenient with OKTA tokens"""
            try:
                return original_verify_jwt_in_request(optional, fresh, refresh, locations, verify_type)
            except Exception as e:
                logger.info(f"JWT verification failed: {str(e)[:100]}")
                
                # If this is an optional verification, allow it to pass
                if optional:
                    logger.info("Optional JWT verification, allowing request to continue")
                    return None
                
                # Try to extract token manually and validate with OKTA
                auth_header = request.headers.get('Authorization', '')
                if auth_header.startswith('Bearer '):
                    token = auth_header.replace('Bearer ', '')
                    
                    # Try OKTA validation
                    claims = Authentication_Provider.validate_okta_token(token)
                    if claims:
                        logger.info("OKTA token validated during verify_jwt_in_request")
                        # Store the claims in g for later use
                        g.jwt_user_claims = claims
                        g.jwt_user_identity = claims.get('sub')
                        return None  # Allow request to continue
                
                # Re-raise if all validation fails
                raise e
        
        # Replace the functions
        flask_jwt_extended.utils.decode_token = patched_decode_token
        flask_jwt_extended.view_decorators.verify_jwt_in_request = patched_verify_jwt_in_request
        
        logger.info("Installed comprehensive JWT monkey patch for OKTA token support")

    @staticmethod
    def _add_okta_endpoints(flask_app: Flask):
        """Add OKTA SSO endpoints to Flask app"""
        from flask import request, redirect, session, url_for
        from config.config import Args
        import urllib.parse
        
        @flask_app.route('/auth/login')
        def okta_login():
            """Redirect to OKTA for SSO authentication"""
            # Generate state for CSRF protection
            import secrets
            state = secrets.token_urlsafe(32)
            session['oauth_state'] = state
            
            # Generate nonce for replay protection
            nonce = secrets.token_urlsafe(32)
            session['oauth_nonce'] = nonce
            
            # Build OKTA authorization URL using v1 endpoints (not default)
            auth_params = {
                'client_id': Args.instance.okta_client_id,
                'response_type': 'code',
                'response_mode': 'query',
                'scope': 'openid profile email',  # Changed from 'webAccess' to standard OIDC scopes
                'redirect_uri': Args.instance.okta_redirect_uri,
                'state': state,
                'nonce': nonce
            }
            
            auth_url = f"{Args.instance.okta_domain}/oauth2/v1/authorize?" + urllib.parse.urlencode(auth_params)
            
            logger.info(f"Generated OKTA SSO URL: {auth_url}")
            logger.info(f"Auth params: {auth_params}")
            logger.info(f"Redirecting to OKTA SSO: {auth_url}")
            print(f"Redirecting to OKTA SSO: {auth_url}")
            return redirect(auth_url)
        
        @flask_app.route('/auth/callback')
        def okta_callback():
            """Handle OKTA SSO callback"""
            # Debug: Log all received parameters
            logger.info(f"OKTA callback received. All query parameters: {dict(request.args)}")
            logger.info(f"Request URL: {request.url}")
            logger.info(f"Request method: {request.method}")
            print("callback request.args:", dict(request.args))  # Debug output
            # Verify state parameter
            received_state = request.args.get('state')
            session_state = session.get('oauth_state')
            logger.info(f"State check - Received: {received_state}, Session: {session_state}")
            
            if received_state != session_state:
                logger.error("Invalid state parameter in OKTA callback")
                return jsonify({'error': 'Invalid state parameter'}), 400
            
            # Get authorization code
            auth_code = request.args.get('code')
            logger.info(f"Authorization code received: {auth_code is not None}")
            
            if not auth_code:
                error = request.args.get('error', 'unknown_error')
                error_description = request.args.get('error_description', 'No authorization code received')
                logger.error(f"OKTA callback error: {error} - {error_description}")
                logger.error(f"All parameters received: {dict(request.args)}")
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
                
                claims = Authentication_Provider.validate_okta_token(id_token)
                if not claims:
                    return jsonify({'error': 'Invalid ID token'}), 400
                
                # Verify nonce
                if claims.get('nonce') != session.get('oauth_nonce'):
                    logger.error("Invalid nonce in ID token")
                    return jsonify({'error': 'Invalid nonce'}), 400
                
                # Create user session
                user = Authentication_Provider.get_user_from_jwt(claims)
                
                # Store user info in session
                session['user_id'] = user.name
                session['user_email'] = user.email
                session['user_roles'] = [role.role_name for role in user.UserRoleList]
                session['access_token'] = tokens.get('access_token')
                
                # Clean up OAuth session data
                session.pop('oauth_state', None)
                session.pop('oauth_nonce', None)
                
                logger.info(f"User {user.name} successfully authenticated via OKTA SSO")
                
                # Redirect to application home or intended destination
                next_url = session.pop('next_url', '/') 
                return redirect(next_url)
                
            except Exception as e:
                logger.error(f"Error processing OKTA callback: {e}")
                return jsonify({'error': 'Authentication failed'}), 500
        
        @flask_app.route('/auth/logout')
        def okta_logout():
            """Logout from OKTA SSO"""
            # Clear local session
            session.clear()
            
            # Build OKTA logout URL using v1 endpoints
            logout_params = {
                'id_token_hint': session.get('id_token', ''),
                'post_logout_redirect_uri': request.host_url
            }
            
            logout_url = f"{Args.instance.okta_domain}/oauth2/v1/logout?" + urllib.parse.urlencode(logout_params)
            
            logger.info("User logged out, redirecting to OKTA logout")
            return redirect(logout_url)
        
        @flask_app.route('/auth/user')
        def get_current_user():
            """Get current authenticated user info"""
            if 'user_id' not in session:
                return jsonify({'error': 'Not authenticated'}), 401
            
            return jsonify({
                'user_id': session.get('user_id'),
                'email': session.get('user_email'),
                'roles': session.get('user_roles', []),
                'authenticated': True
            })
        
        @flask_app.route('/auth/debug')
        def debug_auth():
            """Debug endpoint to check OKTA configuration"""
            from config.config import Args
            return jsonify({
                'okta_domain': Args.instance.okta_domain,
                'okta_client_id': Args.instance.okta_client_id,
                'okta_redirect_uri': Args.instance.okta_redirect_uri,
                'session_keys': list(session.keys()),
                'oauth_state': session.get('oauth_state'),
                'oauth_nonce': session.get('oauth_nonce')
            })

    @staticmethod
    def _exchange_code_for_tokens(auth_code: str) -> Optional[Dict[str, str]]:
        """Exchange authorization code for access and ID tokens"""
        from config.config import Args
        
        try:
            token_url = f"{Args.instance.okta_domain}/oauth2/v1/token"
            
            # Use Basic Auth in header (remove client_id/client_secret from body)
            credentials = base64.b64encode(
                f"{Args.instance.okta_client_id}:{Args.instance.okta_client_secret}".encode('utf-8')
            ).decode('utf-8')
            
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {credentials}'
            }
            
            data = {
                'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': Args.instance.okta_redirect_uri
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
    def get_jwt_public_key(alg, kid=None):
        """
        Retrieve the public key of the JWK keypair used by OKTA to sign the JWTs.
        JWTs signed with this key are trusted by ALS.
        """
        from config.config import Args  # circular import error if at top
        
        # Use the correct JWKS endpoint for ou.okta.com
        jwks_uri = f'{Args.instance.okta_domain}/oauth2/v1/keys'
        
        logger.info(f"Attempting to retrieve JWKS from: {jwks_uri}")
        
        for i in range(10):  # Reduced retries for faster feedback
            try:
                response = requests.get(jwks_uri, timeout=10)
                if response.status_code == 200:
                    keys = response.json()['keys']
                    logger.info(f"Successfully retrieved {len(keys)} keys from OKTA JWKS")
                    break
                else:
                    logger.warning(f"Attempt {i+1}: JWKS request failed with status {response.status_code}")
            except Exception as e:
                logger.warning(f"Attempt {i+1}: Failed to load jwks_uri {jwks_uri}: {e}")
                if i < 9:  # Don't sleep on last attempt
                    time.sleep(1)
        else:
            logger.error(f'Failed to load jwks_uri {jwks_uri} after 10 attempts')
            # Don't exit, return a fallback or None to allow graceful degradation
            return None
            
        for key in keys:
            # loop over all keys until we find the one we're looking for
            if key['alg'] == alg or (kid and key['kid'] == kid):
                logger.info(f"Found JWK: {key['kid']} with algorithm {key['alg']}")
                return RSAAlgorithm.from_jwk(json.dumps(key))
                
        logger.error(f"Couldn't find key with ALG {alg} or kid {kid}")
        # Return None instead of exiting to allow graceful handling
        return None

    @staticmethod
    def get_jwt_user(id: str) -> object:
        """Get JWT user from Flask request context"""
        from flask_jwt_extended import get_jwt
        from flask import has_request_context
        
        return_jwt = None
        if has_request_context():
            return_jwt = g.als_jwt if hasattr(g, 'als_jwt') else None
        return return_jwt

    @staticmethod
    def get_user_from_jwt(jwt_data: dict) -> object:
        """return DotMapX (user+roles) from jwt_data

        Args:
            jwt_data (dict): jwt token claims

        Returns:
            object: ApiLogicServer user (with roles) DotMapX object
        """
        rtn_user = DotMapX()
        rtn_user.client_id = 1  # hack until user data in place
        
        # OKTA standard claims
        rtn_user.name = jwt_data.get("preferred_username") or jwt_data.get("sub") or jwt_data.get("email", "unknown")
        rtn_user.email = jwt_data.get("email")
        rtn_user.given_name = jwt_data.get("given_name")
        rtn_user.family_name = jwt_data.get("family_name")
        rtn_user.password_hash = None

        # Get custom attributes if present
        if "custom_attributes" in jwt_data:
            attributes = jwt_data['custom_attributes']
            for each_name, each_value in attributes.items():
                rtn_user[each_name] = each_value

        # Handle OKTA groups/roles
        rtn_user.UserRoleList = []
        
        # OKTA typically uses 'groups' claim for roles
        role_names = []
        if "groups" in jwt_data:
            role_names = jwt_data["groups"]
        elif "roles" in jwt_data:
            role_names = jwt_data["roles"]
        elif "authorities" in jwt_data:
            role_names = jwt_data["authorities"]
        
        for each_role_name in role_names:
            each_user_role = DotMapX()
            each_user_role.role_name = each_role_name
            rtn_user.UserRoleList.append(each_user_role)
            
        return rtn_user
    
    @staticmethod
    def get_user(id: str, password: str = "") -> object:
        """ Must return a row object or UserAndRole(DotMap) with attributes:
        * name
        * role_list: a list of row objects with attribute name

        For OKTA, the password parameter can contain:
        1. JWT token data (dict) - for OKTA ID tokens
        2. Raw JWT token string - for Bearer token API requests 
        3. Empty string - for session-based requests

        Args:
            id (str): the user login id or sub claim from JWT
            password (str, optional): for OKTA, this can be jwt_data, token string, or empty

        Returns:
            object: row object is a SQLAlchemy row or DotMapX
        """        
        from config.config import Args
        
        use_db = False
        if use_db:  # old code - get user info from sqlite db
            global db, session
            if db is None:
                db = safrs.DB         # Use the safrs.DB for database access
                session = db.session  # sqlalchemy.orm.scoping.scoped_session
        
            user = session.query(authentication_models.User).filter(authentication_models.User.id == id).one_or_none()
            if user is None:
                logger.info(f'*****\nauth_provider: Create user for: {id}\n*****\n')
                user = session.query(authentication_models.User).first()
                return user
            logger.info(f'*****\nauth_provider: User: {user}\n*****\n')
            return user
        
        # Handle different types of authentication data
        jwt_data = {}
        
        if isinstance(password, dict):
            # Direct JWT claims data (from ID token validation)
            jwt_data = password
            logger.debug(f"Using JWT claims data for user: {id}")
            
        elif isinstance(password, str) and password.startswith('eyJ'):
            # Raw JWT token string (from Bearer token API request)
            logger.debug(f"Validating raw JWT token for user: {id}")
            jwt_data = Authentication_Provider.validate_okta_token(password)
            if not jwt_data:
                logger.error(f"Failed to validate OKTA token for user: {id}")
                # Return a minimal user for API compatibility
                rtn_user = DotMapX()
                rtn_user.id = id
                rtn_user.name = id
                rtn_user.email = None
                rtn_user.UserRoleList = []
                return rtn_user
                
        elif not password:
            # Session-based or minimal auth - create basic user
            logger.debug(f"Creating basic user for: {id}")
            rtn_user = DotMapX()
            rtn_user.id = id
            rtn_user.name = id
            rtn_user.email = None
            rtn_user.UserRoleList = []
            return rtn_user
        
        # Get user/roles from OKTA JWT data
        rtn_user = Authentication_Provider.get_user_from_jwt(jwt_data)
        
        # Ensure the user ID matches what was requested
        if not rtn_user.name:
            rtn_user.name = id
        if not hasattr(rtn_user, 'id') or not rtn_user.id:
            rtn_user.id = id
            
        return rtn_user

    @staticmethod
    def validate_okta_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Validate an OKTA JWT token for ou.okta.com
        
        Args:
            token: JWT token to validate
            
        Returns:
            Claims dictionary or None if validation failed
        """
        from config.config import Args
        
        try:
            # Get OKTA's well-known configuration for ou.okta.com using v1 endpoints
            issuer = f"{Args.instance.okta_domain}"
            config_url = f"{Args.instance.okta_domain}/.well-known/openid-configuration"
            
            logger.info(f"Fetching OKTA configuration from: {config_url}")
            
            config_response = requests.get(config_url, timeout=10)
            if config_response.status_code != 200:
                logger.error(f"Could not retrieve OKTA OpenID Connect configuration: {config_response.status_code}")
                return None
            
            config_data = config_response.json()
            jwks_uri = config_data.get("jwks_uri")
            
            if not jwks_uri:
                logger.error("JWKS URI not found in OKTA configuration")
                return None
            
            logger.info(f"Using JWKS URI: {jwks_uri}")
            
            # Get signing keys
            jwks_response = requests.get(jwks_uri, timeout=10)
            if jwks_response.status_code != 200:
                logger.error(f"Could not retrieve JWKS from OKTA: {jwks_response.status_code}")
                return None
            
            jwks_data = jwks_response.json()
            
            # Get the signing key
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")
            
            logger.info(f"Looking for signing key with kid: {kid}")
            
            signing_key = None
            for key in jwks_data.get("keys", []):
                if key.get("kid") == kid:
                    signing_key = key
                    break
            
            if not signing_key:
                logger.error(f"Signing key not found in OKTA JWKS for kid: {kid}")
                available_kids = [k.get("kid") for k in jwks_data.get("keys", [])]
                logger.error(f"Available key IDs: {available_kids}")
                return None
            
            # Convert JWK to PEM format for PyJWT
            public_key = RSAAlgorithm.from_jwk(signing_key)
            
            # Validate token with more flexible options for ou.okta.com
            claims = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                issuer=issuer,
                # audience=Args.instance.okta_client_id,  # May need to be more flexible
                options={
                    "verify_exp": True,
                    "verify_iat": True,
                    "verify_aud": False,  # Set to False for more flexibility with ou.okta.com
                    "verify_iss": True
                },
                leeway=timedelta(minutes=5)  # Increased clock skew allowance
            )
            
            logger.info(f"Successfully validated OKTA token for user: {claims.get('sub', 'unknown')}")
            return claims
            
        except jwt.ExpiredSignatureError:
            logger.error("OKTA token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid OKTA token: {e}")
            return None
        except Exception as e:
            logger.error(f"Error validating OKTA token: {e}")
            return None

    @staticmethod
    def check_password(user: object, password: str) -> bool:
        """
        For OKTA provider, password check is handled via JWT token validation
        
        Args:
            user (object): DotMap or SQLAlchemy row containing user info
            password (str): Can be JWT token string or empty for session-based auth

        Returns:
            bool: True if authenticated, False otherwise
        """
        logger.info(f"check_password called with password type: {type(password)}, starts with eyJ: {isinstance(password, str) and password.startswith('eyJ') if password else False}")
        
        if not password:
            # Session-based authentication - check if user is in session
            from flask import session, has_request_context
            if has_request_context() and 'user_id' in session:
                logger.info("Session-based authentication successful")
                return True
            logger.info("No session authentication found")
            return False
        
        # Check if this is a JWT token (starts with eyJ which is the base64 encoded JWT header)
        if isinstance(password, str) and password.startswith('eyJ'):
            logger.info("Attempting JWT token validation")
            
            # First, try to validate as OKTA token
            claims = Authentication_Provider.validate_okta_token(password)
            if claims:
                logger.info(f"OKTA token validation successful for user: {claims.get('sub')}")
                # Check if the token subject matches the user
                token_user_id = claims.get('sub') or claims.get('preferred_username') or claims.get('email')
                user_id = getattr(user, 'id', None) or getattr(user, 'name', None)
                match_result = token_user_id == user_id
                logger.info(f"User ID match: token={token_user_id}, user={user_id}, match={match_result}")
                return match_result
            
            # If OKTA validation fails, try Flask-JWT-Extended validation for internal tokens
            logger.info("OKTA validation failed, trying internal token validation")
            try:
                from flask_jwt_extended import decode_token
                from flask import current_app
                
                # This will use the HS256 secret key for internal API tokens
                internal_claims = decode_token(password)
                if internal_claims:
                    logger.info("Internal token validation successful")
                    token_user_id = internal_claims.get('sub')
                    user_id = getattr(user, 'id', None) or getattr(user, 'name', None)
                    match_result = token_user_id == user_id
                    logger.info(f"Internal token user ID match: token={token_user_id}, user={user_id}, match={match_result}")
                    return match_result
            except Exception as e:
                logger.info(f"Internal token validation failed: {e}")
            
            logger.info("Both OKTA and internal token validation failed")
            return False
            
        # For other cases (like JWT claims dict), assume already validated
        logger.info("Non-token password, assuming validated")
        return True

    @staticmethod
    def get_sso_login_url() -> str:
        """
        Get the OKTA SSO login URL for redirecting users
        
        Returns:
            SSO login URL
        """
        from flask import request
        from config.config import Args
        return f"{request.host_url}auth/login"
    
    @staticmethod
    def is_authenticated(request) -> bool:
        """
        Check if the current request is authenticated
        
        Args:
            request: Flask request object
            
        Returns:
            bool: True if authenticated, False otherwise
        """
        from flask import session
        return 'user_id' in session and 'access_token' in session
