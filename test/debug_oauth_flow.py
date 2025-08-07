#!/usr/bin/env python3
"""
OAuth Flow Debug Script
This script helps diagnose OAuth authorization code issues

Common issues with "authorization code is invalid or has expired":
1. Authorization code used multiple times (codes are single-use)
2. Authorization code expired (typically 60 seconds or less)
3. Redirect URI mismatch between authorization and token requests
4. Client ID/Secret mismatch
5. Authorization code tampered with during redirect
6. Wrong token endpoint URL
"""

import requests
import json
import base64
import time
from urllib.parse import urlencode, parse_qs, urlparse
import secrets
import hashlib
from typing import Dict, Any, Optional


def test_okta_oauth_flow():
    """Test the complete OAuth flow step by step"""
    
    # Configuration - Update these with your actual values
    OKTA_DOMAIN = "https://ou.okta.com"
    CLIENT_ID = "0oa1crjfiwoxRYadi0x8"  # Real client ID from config
    CLIENT_SECRET = "eVdobSwZgx8ANVRwPTxX6lce24t4e5ZBuAQSn_QPopvi69Xa36SWoyPjH4WcjAI7"  # Real client secret
    REDIRECT_URI = "http://localhost:5656/auth/callback"
    
    print("🔍 OAuth Flow Debug Tool")
    print("=" * 50)
    
    # Step 1: Test OpenID Configuration
    print("\n1️⃣ Testing OpenID Configuration...")
    config_url = f"{OKTA_DOMAIN}/.well-known/openid-configuration"
    
    try:
        response = requests.get(config_url, timeout=10)
        if response.status_code == 200:
            config = response.json()
            print(f"   ✅ OpenID config accessible")
            print(f"   📍 Authorization endpoint: {config.get('authorization_endpoint')}")
            print(f"   📍 Token endpoint: {config.get('token_endpoint')}")
            print(f"   📍 JWKS URI: {config.get('jwks_uri')}")
            
            auth_endpoint = config.get('authorization_endpoint')
            token_endpoint = config.get('token_endpoint')
        else:
            print(f"   ❌ OpenID config failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ OpenID config error: {e}")
        return
    
    # Step 2: Generate Authorization URL
    print("\n2️⃣ Generating Authorization URL...")
    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)
    
    auth_params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri':  REDIRECT_URI,
        'scope': 'openid profile email',
        'state': state,
        'nonce': nonce
    }
    
    auth_url = f"{auth_endpoint}?{urlencode(auth_params)}"
    
    print(f"   📝 State: {state}")
    print(f"   📝 Nonce: {nonce}")
    print(f"   🔗 Authorization URL:")
    print(f"   {auth_url}")
    
    # Step 3: Simulate getting authorization code
    print("\n3️⃣ Authorization Code Exchange Simulation...")
    print("   ℹ️  You would normally get this from the callback URL")
    
    # Test with a dummy code to see the error message
    dummy_code = "dummy_authorization_code"
    
    print(f"\n4️⃣ Testing Token Exchange with Dummy Code...")
    result = exchange_code_for_tokens(
        token_endpoint, CLIENT_ID, CLIENT_SECRET, 
        dummy_code, REDIRECT_URI
    )
    
    if result:
        print("   ✅ Token exchange successful (unexpected with dummy code)")
    else:
        print("   ❌ Token exchange failed (expected with dummy code)")
    
    # Step 4: Provide troubleshooting steps
    print("\n5️⃣ Troubleshooting Steps:")
    print("""
   If you're getting 'authorization code is invalid or has expired':
   
   🔧 Check these common issues:
   
   1. REDIRECT URI EXACT MATCH:
      - Authorization request: {redirect_uri}
      - Token request: {redirect_uri}
      - OKTA app config: {redirect_uri}
      - These must be IDENTICAL (including trailing slash, protocol, port)
   
   2. AUTHORIZATION CODE USAGE:
      - Each code can only be used ONCE
      - Codes expire quickly (usually 60 seconds)
      - Don't refresh the callback page after successful auth
   
   3. CLIENT CONFIGURATION:
      - Verify client_id and client_secret are correct
      - Check that your OKTA app is configured for 'Authorization Code' flow
      - Ensure the app has the right scopes: openid, profile, email
   
   4. TIMING ISSUES:
      - Process the authorization code immediately after receiving it
      - Don't store codes for later use
   
   5. URL ENCODING:
      - Ensure the authorization code isn't double-encoded
      - Check for special characters in the code
   """.format(redirect_uri=REDIRECT_URI))


def exchange_code_for_tokens(token_endpoint: str, client_id: str, client_secret: str, 
                           auth_code: str, redirect_uri: str) -> Optional[Dict[str, Any]]:
    """Exchange authorization code for tokens"""
    
    print(f"   📤 Token endpoint: {token_endpoint}")
    print(f"   📤 Client ID: {client_id}")
    print(f"   📤 Auth code: {auth_code[:20]}..." if len(auth_code) > 20 else f"   📤 Auth code: {auth_code}")
    print(f"   📤 Redirect URI: {redirect_uri}")
    
    # Create basic auth header (DO NOT include client credentials in body)
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    # Only include grant_type, code, and redirect_uri in body
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri
    }
    
    try:
        print(f"   📡 Making token request...")
        response = requests.post(token_endpoint, headers=headers, data=data, timeout=10)
        
        print(f"   📊 Response status: {response.status_code}")
        print(f"   📊 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            tokens = response.json()
            print(f"   ✅ Success! Received tokens: {list(tokens.keys())}")
            return tokens
        else:
            error_data = {}
            try:
                error_data = response.json()
            except:
                error_data = {'raw_response': response.text}
            
            print(f"   ❌ Token exchange failed:")
            print(f"   📝 Error: {error_data.get('error', 'unknown')}")
            print(f"   📝 Description: {error_data.get('error_description', 'No description')}")
            print(f"   📝 Raw response: {response.text}")
            
            # Specific error handling
            error_code = error_data.get('error')
            if error_code == 'invalid_grant':
                print("\n   🔍 INVALID_GRANT Error Analysis:")
                print("   • Most common cause: Authorization code already used or expired")
                print("   • Check: Are you making this request twice?")
                print("   • Check: Did the authorization code expire? (Usually 60 seconds)")
                print("   • Check: Is the redirect_uri EXACTLY the same as in authorization request?")
            elif error_code == 'invalid_client':
                print("\n   🔍 INVALID_CLIENT Error Analysis:")
                print("   • Client ID or secret is incorrect")
                print("   • Check your OKTA app configuration")
            elif error_code == 'unsupported_grant_type':
                print("\n   🔍 UNSUPPORTED_GRANT_TYPE Error Analysis:")
                print("   • Your OKTA app might not be configured for Authorization Code flow")
                print("   • Check OKTA app settings: Grant Types should include 'Authorization Code'")
            elif error_code == 'invalid_request':
                desc = error_data.get('error_description', '')
                if 'multiple client credentials' in desc:
                    print("\n   🔍 MULTIPLE CLIENT CREDENTIALS Error:")
                    print("   • ✅ FIXED: Now using only Basic Auth header (not body credentials)")
                    print("   • This error should be resolved now")
            
            return None
            
    except requests.RequestException as e:
        print(f"   ❌ Network error: {e}")
        return None


def test_specific_error_scenarios():
    """Test specific error scenarios to understand the issue better"""
    
    print("\n6️⃣ Testing Specific Error Scenarios...")
    
    OKTA_DOMAIN = "https://ou.okta.com"
    CLIENT_ID = "0oa1crjfiwoxRYadi0x8"  # Real client ID
    CLIENT_SECRET = "eVdobSwZgx8ANVRwPTxX6lce24t4e5ZBuAQSn_QPopvi69Xa36SWoyPjH4WcjAI7"  # Real client secret
    REDIRECT_URI = "http://localhost:5656/auth/callback"
    
    token_endpoint = f"{OKTA_DOMAIN}/oauth2/v1/token"
    
    # Test 1: Empty authorization code
    print("\n   Test 1: Empty authorization code")
    exchange_code_for_tokens(token_endpoint, CLIENT_ID, CLIENT_SECRET, "", REDIRECT_URI)
    
    # Test 2: Malformed authorization code
    print("\n   Test 2: Malformed authorization code")
    exchange_code_for_tokens(token_endpoint, CLIENT_ID, CLIENT_SECRET, "invalid_code_123", REDIRECT_URI)
    
    # Test 3: Wrong redirect URI
    print("\n   Test 3: Wrong redirect URI")
    exchange_code_for_tokens(token_endpoint, CLIENT_ID, CLIENT_SECRET, "dummy_code", "http://wrong-redirect.com")
    
    print("\n   ℹ️  These tests help identify the specific error messages from your OKTA instance")


def create_test_authorization_url():
    """Create a test authorization URL you can use in a browser"""
    
    OKTA_DOMAIN = "https://ou.okta.com"
    CLIENT_ID = "0oa1crjfiwoxRYadi0x8"  # Real client ID
    REDIRECT_URI = "http://localhost:5656/auth/callback"
    
    # Get the correct authorization endpoint
    try:
        config_response = requests.get(f"{OKTA_DOMAIN}/.well-known/openid-configuration", timeout=10)
        if config_response.status_code == 200:
            config = config_response.json()
            auth_endpoint = config.get('authorization_endpoint')
        else:
            print(f"❌ Could not get OpenID config: {config_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error getting OpenID config: {e}")
        return
    
    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)
    
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'openid profile email',
        'state': state,
        'nonce': nonce
    }
    
    auth_url = f"{auth_endpoint}?{urlencode(params)}"
    
    print(f"\n🔗 Test Authorization URL (copy to browser):")
    print(f"{auth_url}")
    print(f"\n📝 Expected state in callback: {state}")
    print(f"📝 Expected nonce in ID token: {nonce}")


if __name__ == "__main__":
    print("Starting OAuth Flow Debug...")
    
    # Update the configuration at the top of the functions above with your actual values
    print("\n⚠️  IMPORTANT: Update the CLIENT_ID, CLIENT_SECRET in the functions above before running!")
    
    test_okta_oauth_flow()
    test_specific_error_scenarios() 
    create_test_authorization_url()
    
    print("\n✨ Debug complete!")
