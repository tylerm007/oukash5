#!/usr/bin/env python3
"""
Test script to verify OKTA JWT token validation after algorithm fix
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

import requests
import json
from typing import Optional, Dict, Any

def test_rest_api_with_bearer_token():
    """Test REST API calls with Bearer token authentication"""
    
    print("🧪 Testing REST API with Bearer Token Authentication")
    print("=" * 60)
    
    # First, let's test if we can get a valid OKTA token
    print("\n1️⃣ Testing OKTA Token Retrieval...")
    
    # You'll need to get a real token from the OKTA SSO flow
    # For now, let's test the server's capability to handle different token types
    
    base_url = "http://localhost:5656"  # Default API Logic Server port
    
    # Test endpoints to try
    test_endpoints = [
        "/api/Customer",
        "/api/Product", 
        "/api/Order"
    ]
    
    print(f"\n2️⃣ Testing API endpoints at {base_url}")
    
    # Test without authentication first
    print("\n   📝 Testing without authentication:")
    for endpoint in test_endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            print(f"      {endpoint}: Status {response.status_code}")
            if response.status_code == 401:
                print(f"        ✅ Correctly requires authentication")
            elif response.status_code == 200:
                print(f"        ⚠️  No authentication required (check security config)")
            else:
                print(f"        ❓ Unexpected status code")
        except requests.exceptions.RequestException as e:
            print(f"      {endpoint}: Connection error - {e}")
    
    # Test with a sample Bearer token (this will fail validation but shows token processing)
    print("\n   📝 Testing with sample Bearer token:")
    
    # Create a sample token header for testing token processing
    sample_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImhKQmdZODdtQ0JJVkUwaWM2MXBpWFVUelhLLUNBQmlkaGxGTkhBZ1F1cWMifQ.eyJzdWIiOiIwMHVtaXIwNzUyVWhPSHRIaTB4OCIsIm5hbWUiOiJUZXN0IFVzZXIiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJpYXQiOjE3MzQwNzQ0MzQsImV4cCI6MTczNDA3ODAzNCwiaXNzIjoiaHR0cHM6Ly9vdS5va3RhLmNvbSIsImF1ZCI6ImFwaTovL2RlZmF1bHQifQ.sample_signature"
    
    headers = {
        "Authorization": f"Bearer {sample_token}",
        "Content-Type": "application/json"
    }
    
    for endpoint in test_endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, headers=headers, timeout=5)
            print(f"      {endpoint}: Status {response.status_code}")
            
            if response.status_code == 401:
                error_msg = response.text
                if "alg value is not allowed" in error_msg:
                    print(f"        ❌ Still getting algorithm error: {error_msg[:100]}...")
                else:
                    print(f"        ❓ Authentication failed (expected): {error_msg[:100]}...")
                    
        except requests.exceptions.RequestException as e:
            print(f"      {endpoint}: Connection error - {e}")
    
    print("\n3️⃣ Manual JWT Token Analysis")
    print("   You can test with a real OKTA token by:")
    print("   1. Login via OKTA SSO in your browser")
    print("   2. Get the access token from the session or network tab")
    print("   3. Use it in API calls with: Authorization: Bearer <token>")
    
    return True

def test_jwt_configuration():
    """Test the JWT configuration in the application"""
    
    print("\n4️⃣ Testing JWT Configuration...")
    
    try:
        # Import our authentication provider
        from security.authentication_provider.okta.auth_provider import Authentication_Provider
        
        print("   ✅ Successfully imported OKTA Authentication Provider")
        
        # Test JWKS retrieval
        print("   📝 Testing JWKS retrieval...")
        public_key = Authentication_Provider.get_jwt_public_key('RS256')
        
        if public_key:
            print("   ✅ Successfully retrieved OKTA public key")
            print(f"      Key type: {type(public_key)}")
        else:
            print("   ❌ Could not retrieve OKTA public key")
            
        # Test token validation method exists
        if hasattr(Authentication_Provider, 'validate_okta_token'):
            print("   ✅ validate_okta_token method exists")
        else:
            print("   ❌ validate_okta_token method missing")
            
        return True
        
    except ImportError as e:
        print(f"   ❌ Could not import authentication provider: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error testing JWT configuration: {e}")
        return False

def main():
    """Main test function"""
    
    print("🔧 OKTA JWT Algorithm Fix Verification")
    print("=" * 50)
    print("This script tests the JWT token handling after the algorithm fix.")
    print("Make sure the API Logic Server is running on localhost:5656")
    
    # Test JWT configuration
    config_ok = test_jwt_configuration()
    
    if config_ok:
        # Test REST API
        test_rest_api_with_bearer_token()
    
    print("\n📋 Summary:")
    print("- If you see 'alg value is not allowed' errors, the fix may need adjustment")
    print("- If you see 401 authentication errors, that's normal without a valid token")
    print("- The key is that JWT processing should work without algorithm errors")
    print("\n🔄 Next Steps:")
    print("1. Run the API Logic Server: python api_logic_server_run.py")
    print("2. Test with a real OKTA SSO login to get a valid Bearer token")
    print("3. Use the token in REST API calls to verify end-to-end functionality")

if __name__ == "__main__":
    main()
