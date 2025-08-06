import json
import base64
import requests
import jwt
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs, urlencode
from typing import Optional, Tuple, Dict, Any
import asyncio
import aiohttp
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import logging


class OktaAccessToken:
    """Python equivalent of OktaAccessToken entity"""
    def __init__(self, token_type: str = None, expires_in: str = None, 
                 access_token: str = None, scope: str = None):
        self.token_type = token_type
        self.expires_in = expires_in
        self.access_token = access_token
        self.scope = scope


class OktaToken:
    """Python equivalent of C# OktaToken class for creating and validating Okta tokens"""
    
    def __init__(self, domain: str, client_id: str, redirect_url: str = None, client_secret: str = None):
        """
        Initialize OktaToken instance
        
        Args:
            domain: Okta domain (e.g., https://your-domain.okta.com)
            client_id: OAuth client ID
            redirect_url: OAuth redirect URL (optional)
            client_secret: OAuth client secret (optional)
        """
        self.domain = domain
        self.client_id = client_id
        self.redirect_url = redirect_url
        self.client_secret = client_secret
        self._configuration_manager = None
        
    def get_id_token(self, username: str, password: str) -> str:
        """
        Get ID token using username and password authentication
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            ID token string or empty string if failed
        """
        ret = ""
        
        # First request: Get session token
        session_token_url = f"{self.domain}/api/v1/authn"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        body = {
            "username": username,
            "password": password,
            "options": {
                "multiOptionalFactorEnroll": True,
                "warnBeforePasswordExpired": True
            }
        }
        
        try:
            response = requests.post(
                session_token_url,
                headers=headers,
                json=body,
                allow_redirects=False,
                timeout=10
            )
            print(response.status_code, response.text)  # Debugging line, remove in production
            if response.status_code == 200 and response.text:
                response_data = response.json()
                session_token = response_data.get("sessionToken")
                
                if session_token:
                    print(session_token)
                    
                    # Second request: Get ID token using session token
                    authorize_url = (
                        f"{self.domain}/oauth2/default/v1/authorize?"
                        f"client_id={self.client_id}&"
                        f"response_type=id_token&"
                        f"response_mode=fragment&"
                        f"scope=openid profile email&"
                        f"redirect_uri={self.redirect_url}&"
                        f"state=foreverInTheSameState&"
                        f"nonce=ff1cd991&"
                        f"sessionToken={session_token}"
                    )
                    
                    id_token_response = requests.get(
                        authorize_url,
                        headers={"Accept": "application/json"},
                        allow_redirects=False,
                        timeout=10
                    )
                    
                    location_header = id_token_response.headers.get("Location")
                    if location_header and "id_token=" in location_header:
                        start_index = location_header.find("id_token=") + len("id_token=")
                        end_index = location_header.find("&", start_index)
                        if end_index == -1:
                            end_index = len(location_header)
                        
                        ret = location_header[start_index:end_index]
                        
        except requests.exceptions.RequestException as e:
            logging.error(f"Error getting ID token: {e}")
            
        return ret
    
    def create_web_access_token(self) -> Optional[OktaAccessToken]:
        """
        Create an Okta web access token using client credentials
        
        Returns:
            OktaAccessToken object or None if failed
        """
        if not self.client_secret:
            raise ValueError("Client secret is required for web access token")
            
        ret = None
        
        # Create basic auth credentials
        credentials = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode('utf-8')
        ).decode('utf-8')
        
        headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "client_credentials",
            "scope": "webAccess"
        }
        
        token_url = f"{self.domain}/oauth2/default/v1/token"
        print("token_url:", token_url)  # Debugging line, remove in production
        try:
            response = requests.post(token_url, headers=headers, data=data)
            print(response.status_code, response.text)  # Debugging line, remove in production
            if response.status_code == 200:
                token_data = response.json()
                ret = OktaAccessToken(
                    token_type=token_data.get("token_type"),
                    expires_in=token_data.get("expires_in"),
                    access_token=token_data.get("access_token"),
                    scope=token_data.get("scope")
                )
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Error creating web access token: {e}")
            
        return ret
    
    def validate_okta_pkce_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate an Okta PKCE token
        
        Args:
            token: JWT token to validate
            
        Returns:
            Claims dictionary or None if validation failed
        """
        try:
            # Decode token header to get kid
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")
            
            if not kid:
                raise ValueError("Token header missing 'kid' parameter")
            
            # Get key parameters
            e, n = asyncio.run(self._get_key_parameters_async(self.domain, kid))
            
            if not e or not n:
                raise ValueError("Could not retrieve key parameters")
            
            # Validate token using OktaAuthenticator equivalent
            return self._validate_token_with_key_params(token, e, n)
            
        except Exception as e:
            logging.error(f"Error validating PKCE token: {e}")
            return None
    
    async def _get_key_parameters_async(self, domain: str, kid: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Asynchronously get key parameters from Okta
        
        Args:
            domain: Okta domain
            kid: Key ID from token header
            
        Returns:
            Tuple of (e, n) parameters or (None, None) if not found
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{domain}/oauth2/v1/keys") as response:
                    if response.status == 200:
                        jwks_data = await response.json()
                        
                        for key in jwks_data.get("keys", []):
                            if key.get("kid") == kid:
                                return key.get("e"), key.get("n")
                                
        except Exception as e:
            logging.error(f"Error getting key parameters: {e}")
            
        return None, None
    
    def _validate_token_with_key_params(self, token: str, e: str, n: str) -> Optional[Dict[str, Any]]:
        """
        Validate token using RSA key parameters (equivalent to OktaAuthenticator.ValidateToken)
        
        Args:
            token: JWT token
            e: RSA public exponent
            n: RSA modulus
            
        Returns:
            Claims dictionary or None if validation failed
        """
        try:
            # Convert base64url encoded parameters to integers
            from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
            
            e_int = int.from_bytes(self._base64url_decode(e), 'big')
            n_int = int.from_bytes(self._base64url_decode(n), 'big')
            
            # Create RSA public key
            public_numbers = RSAPublicNumbers(e_int, n_int)
            public_key = public_numbers.public_key(default_backend())
            
            # Validate and decode token
            claims = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                issuer=f"{self.domain}/oauth2/default",
                audience=self.client_id,
                options={"verify_exp": True, "verify_iat": True}
            )
            
            return claims
            
        except Exception as e:
            logging.error(f"Error validating token with key params: {e}")
            return None
    
    def validate_okta_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate an Okta token using OpenID Connect discovery
        
        Args:
            token: JWT token to validate
            
        Returns:
            Claims dictionary or None if validation failed
        """
        issuer = f"{self.domain}/oauth2/default"
        
        try:
            # Get OpenID Connect configuration
            config_url = f"{issuer}/.well-known/oauth-authorization-server"
            config_response = requests.get(config_url)
            
            if config_response.status_code != 200:
                raise ValueError("Could not retrieve OpenID Connect configuration")
            
            config_data = config_response.json()
            jwks_uri = config_data.get("jwks_uri")
            
            if not jwks_uri:
                raise ValueError("JWKS URI not found in configuration")
            
            # Get signing keys
            jwks_response = requests.get(jwks_uri)
            if jwks_response.status_code != 200:
                raise ValueError("Could not retrieve JWKS")
            
            jwks_data = jwks_response.json()
            
            # Validate token
            return self._validate_token_with_jwks(token, issuer, jwks_data)
            
        except Exception as e:
            logging.error(f"Error validating Okta token: {e}")
            return None
    
    def _validate_token_with_jwks(self, token: str, issuer: str, jwks_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Validate token using JWKS data
        
        Args:
            token: JWT token
            issuer: Token issuer
            jwks_data: JWKS data containing signing keys
            
        Returns:
            Claims dictionary or None if validation failed
        """
        try:
            # Get the signing key
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")
            
            signing_key = None
            for key in jwks_data.get("keys", []):
                if key.get("kid") == kid:
                    signing_key = key
                    break
            
            if not signing_key:
                raise ValueError("Signing key not found")
            
            # Convert JWK to PEM format for PyJWT
            from jwt.algorithms import RSAAlgorithm
            public_key = RSAAlgorithm.from_jwk(signing_key)
            
            # Validate token
            claims = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                issuer=issuer,
                options={
                    "verify_exp": True,
                    "verify_iat": True,
                    "verify_aud": False  # Set to False as mentioned in C# comment
                },
                leeway=timedelta(minutes=2)  # Clock skew allowance
            )
            
            return claims
            
        except Exception as e:
            logging.error(f"Error validating token with JWKS: {e}")
            return None
    
    @staticmethod
    def _base64url_decode(data: str) -> bytes:
        """
        Decode base64url encoded data
        
        Args:
            data: Base64url encoded string
            
        Returns:
            Decoded bytes
        """
        # Add padding if necessary
        padding = 4 - (len(data) % 4)
        if padding != 4:
            data += '=' * padding
        
        return base64.urlsafe_b64decode(data)


# Utility functions (equivalent to Utils.cs functionality)
def not_blank(value: str) -> bool:
    """Check if string is not None and not empty/whitespace"""
    return value is not None and value.strip() != ""
