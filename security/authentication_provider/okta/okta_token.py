import json
import base64
import requests
import jwt
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs, urlencode
from typing import Optional, Tuple, Dict, Any
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
            "Content-Type": "application/json",
            "User-Agent": "API-Logic-Server/1.0"
        }
        
        body = {
            "username": username,
            "password": password,
            "options": {
                "multiOptionalFactorEnroll": False,
                "warnBeforePasswordExpired": False
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
            
            print(f"OKTA Auth Response: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Body: {response.text}")
            
            if response.status_code == 200 and response.text:
                response_data = response.json()
                session_token = response_data.get("sessionToken")
                
                if session_token:
                    print(f"Session token obtained: {session_token[:20]}...")
                    
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
                        
            elif response.status_code == 401:
                response_data = response.json() if response.text else {}
                error_code = response_data.get("errorCode", "Unknown")
                error_summary = response_data.get("errorSummary", "Authentication failed")
                error_causes = response_data.get("errorCauses", [])
                
                print(f"OKTA Authentication Error:")
                print(f"  Error Code: {error_code}")
                print(f"  Error Summary: {error_summary}")
                if error_causes:
                    print(f"  Error Causes: {error_causes}")
                
                # Handle specific error codes
                if error_code == "E0000004":
                    print("  This typically means invalid username/password or account locked")
                    print("  Check credentials and account status in OKTA admin console")
                elif error_code == "E0000014":
                    print("  Update of credentials failed - check password policy")
                elif error_code == "E0000001":
                    print("  API validation failed - check request format")
                    
                logging.error(f"OKTA authentication failed: {error_code} - {error_summary}")
                
            else:
                print(f"Unexpected response status: {response.status_code}")
                print(f"Response: {response.text}")
                        
        except requests.exceptions.RequestException as e:
            logging.error(f"Error getting ID token: {e}")
            print(f"Network error connecting to OKTA: {e}")
            
        return ret
    
    def test_okta_connectivity(self) -> Dict[str, Any]:
        """
        Test connectivity and configuration for OKTA domain
        
        Returns:
            Dictionary with test results
        """
        results = {
            "domain_accessible": False,
            "auth_endpoint_accessible": False,
            "oauth_config_accessible": False,
            "jwks_accessible": False,
            "errors": []
        }
        
        try:
            # Test 1: Basic domain connectivity
            print(f"Testing basic connectivity to {self.domain}...")
            basic_response = requests.get(self.domain, timeout=10)
            results["domain_accessible"] = basic_response.status_code < 400
            print(f"  Domain connectivity: {results['domain_accessible']} (Status: {basic_response.status_code})")
            
        except Exception as e:
            results["errors"].append(f"Domain connectivity failed: {e}")
            print(f"  Domain connectivity failed: {e}")
        
        try:
            # Test 2: Auth endpoint
            auth_endpoint = f"{self.domain}/api/v1/authn"
            print(f"Testing auth endpoint: {auth_endpoint}")
            
            # Try a basic POST to see if endpoint exists (should return 400/401, not 404)
            auth_response = requests.post(
                auth_endpoint,
                headers={"Content-Type": "application/json"},
                json={"username": "test", "password": "test"},
                timeout=10
            )
            # Endpoint exists if we get 400/401 (bad request/unauthorized) rather than 404
            results["auth_endpoint_accessible"] = auth_response.status_code in [400, 401]
            print(f"  Auth endpoint accessible: {results['auth_endpoint_accessible']} (Status: {auth_response.status_code})")
            
            if auth_response.status_code == 404:
                results["errors"].append("Auth endpoint not found - check OKTA domain configuration")
                
        except Exception as e:
            results["errors"].append(f"Auth endpoint test failed: {e}")
            print(f"  Auth endpoint test failed: {e}")
        
        try:
            # Test 3: OAuth configuration using the correct endpoint for ou.okta.com
            config_url = f"{self.domain}/.well-known/openid-configuration"
            print(f"Testing OAuth config: {config_url}")
            
            config_response = requests.get(config_url, timeout=10)
            results["oauth_config_accessible"] = config_response.status_code == 200
            print(f"  OAuth config accessible: {results['oauth_config_accessible']} (Status: {config_response.status_code})")
            
            if config_response.status_code == 200:
                config_data = config_response.json()
                print(f"  Issuer: {config_data.get('issuer', 'Not found')}")
                print(f"  Authorization endpoint: {config_data.get('authorization_endpoint', 'Not found')}")
                print(f"  Token endpoint: {config_data.get('token_endpoint', 'Not found')}")
                
                # Test 4: JWKS endpoint
                jwks_uri = config_data.get("jwks_uri")
                if jwks_uri:
                    print(f"Testing JWKS endpoint: {jwks_uri}")
                    jwks_response = requests.get(jwks_uri, timeout=10)
                    results["jwks_accessible"] = jwks_response.status_code == 200
                    print(f"  JWKS accessible: {results['jwks_accessible']} (Status: {jwks_response.status_code})")
                    
                    if jwks_response.status_code == 200:
                        jwks_data = jwks_response.json()
                        key_count = len(jwks_data.get("keys", []))
                        print(f"  Available signing keys: {key_count}")
                else:
                    results["errors"].append("JWKS URI not found in OAuth configuration")
                    
        except Exception as e:
            results["errors"].append(f"OAuth configuration test failed: {e}")
            print(f"  OAuth configuration test failed: {e}")
        
        # Summary
        all_accessible = all([
            results["domain_accessible"],
            results["auth_endpoint_accessible"],
            results["oauth_config_accessible"],
            results["jwks_accessible"]
        ])
        
        print(f"\nConnectivity Test Summary:")
        print(f"  Overall Status: {'✅ Pass' if all_accessible else '❌ Issues detected'}")
        if results["errors"]:
            print(f"  Errors: {len(results['errors'])}")
            for error in results["errors"]:
                print(f"    - {error}")
        
        return results
    
    def create_web_access_token(self, authorization_code: str) -> Optional[OktaAccessToken]:
        """
        Exchange authorization code for access token
        
        Args:
            authorization_code: The authorization code from OAuth callback
            
        Returns:
            OktaAccessToken object or None if failed
        """
        if not self.client_secret:
            raise ValueError("Client secret is required for web access token")
            
        if not authorization_code:
            raise ValueError("Authorization code is required")
            
        if not self.redirect_url:
            raise ValueError("Redirect URL is required for authorization code exchange")
            
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
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "code": authorization_code,
            "redirect_uri": self.redirect_url,
            "scope": "openid profile email"
        }
        
        token_url = f"{self.domain}/oauth2/v1/token"
        print("token_url:", token_url)  # Debugging line, remove in production
        try:
            response = requests.post(token_url, headers=headers, data=data, timeout=10)
            print(f"Token exchange response: {response.status_code}")  # Debugging line, remove in production
            print(f"Response headers: {dict(response.headers)}")  # Debugging line, remove in production
            
            if response.status_code == 200:
                token_data = response.json()
                print(f"Token data received: {list(token_data.keys())}")  # Debugging line, remove in production
                ret = OktaAccessToken(
                    token_type=token_data.get("token_type"),
                    expires_in=str(token_data.get("expires_in", 0)),
                    access_token=token_data.get("access_token"),
                    scope=token_data.get("scope")
                )
            else:
                print(f"Token exchange failed: {response.text}")  # Debugging line, remove in production
                logging.error(f"Token exchange failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Error exchanging authorization code for tokens: {e}")
            print(f"Network error during token exchange: {e}")
            
        return ret
    
    def create_client_credentials_token(self) -> Optional[OktaAccessToken]:
        """
        Create an Okta access token using client credentials grant (for server-to-server)
        
        Returns:
            OktaAccessToken object or None if failed
        """
        if not self.client_secret:
            raise ValueError("Client secret is required for client credentials grant")
            
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
            "scope": "openid profile email"
        }
        
        token_url = f"{self.domain}/oauth2/v1/token"
        
        try:
            response = requests.post(token_url, headers=headers, data=data, timeout=10)
            if response.status_code == 200:
                token_data = response.json()
                ret = OktaAccessToken(
                    token_type=token_data.get("token_type"),
                    expires_in=str(token_data.get("expires_in", 0)),
                    access_token=token_data.get("access_token"),
                    scope=token_data.get("scope")
                )
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Error creating client credentials token: {e}")
            
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
            
            # Get key parameters synchronously
            e, n = self._get_key_parameters_sync(self.domain, kid)
            
            if not e or not n:
                raise ValueError("Could not retrieve key parameters")
            
            # Validate token using OktaAuthenticator equivalent
            return self._validate_token_with_key_params(token, e, n)
            
        except Exception as e:
            logging.error(f"Error validating PKCE token: {e}")
            return None
    
    def _get_key_parameters_sync(self, domain: str, kid: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Get key parameters from Okta synchronously
        
        Args:
            domain: Okta domain
            kid: Key ID from token header
            
        Returns:
            Tuple of (e, n) parameters or (None, None) if not found
        """
        try:
            response = requests.get(f"{domain}/oauth2/v1/keys", timeout=10)
            if response.status_code == 200:
                jwks_data = response.json()
                
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
        issuer = self.domain
        
        try:
            # Get OpenID Connect configuration using the correct endpoint for ou.okta.com
            config_url = f"{self.domain}/.well-known/openid-configuration"
            config_response = requests.get(config_url, timeout=10)
            
            if config_response.status_code != 200:
                raise ValueError("Could not retrieve OpenID Connect configuration")
            
            config_data = config_response.json()
            jwks_uri = config_data.get("jwks_uri")
            
            if not jwks_uri:
                raise ValueError("JWKS URI not found in configuration")
            
            # Get signing keys
            jwks_response = requests.get(jwks_uri, timeout=10)
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
