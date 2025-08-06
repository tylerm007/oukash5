#!/usr/bin/env python3
"""
OKTA Authentication Provider Test Script
========================================

This script demonstrates how to use the OKTA authentication provider
with your API Logic Server application.

Requirements:
1. Set environment variables for OKTA configuration
2. Have a running API Logic Server instance
3. Valid OKTA domain and client credentials

Usage:
    python test_okta_auth.py
"""

import os
import sys
import json
import requests
from typing import Optional

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
'''
Client ID: 0oa1crjfiwoxRYadi0x8
Secret: eVdobSwZgx8ANVRwPTxX6lce24t4e5ZBuAQSn_QPopvi69Xa36SWoyPjH4WcjAI7
'''
# Configuration - these should be set as environment variables in production
OKTA_DOMAIN = os.getenv('OKTA_DOMAIN', 'https://ou.okta.com')
OKTA_CLIENT_ID = os.getenv('OKTA_CLIENT_ID', '0oa1crjfiwoxRYadi0x8')
OKTA_CLIENT_SECRET = os.getenv('OKTA_CLIENT_SECRET', 'eVdobSwZgx8ANVRwPTxX6lce24t4e5ZBuAQSn_QPopvi69Xa36SWoyPjH4WcjAI7')
OKTA_REDIRECT_URL = os.getenv('OKTA_REDIRECT_URL', 'http://localhost:5656/auth/callback')# 'http://localhost:5000/callback')

def setup_environment():
    """Set up environment variables for OKTA configuration"""
    print("🔧 Setting up OKTA environment variables...")
    
    # Example configuration - replace with your actual values
    env_vars = {
        'OKTA_DOMAIN': 'https://ou.okta.com',
        'OKTA_CLIENT_ID': '0oa1crjfiwoxRYadi0x8',
        'OKTA_CLIENT_SECRET': 'eVdobSwZgx8ANVRwPTxX6lce24t4e5ZBuAQSn_QPopvi69Xa36SWoyPjH4WcjAI7',
        'OKTA_REDIRECT_URI': 'http://localhost:5656/auth/callback',
        'SECURITY_ENABLED': 'true',
        'SECURITY_PROVIDER': 'okta'
    }
    
    for key, value in env_vars.items():
        if not os.getenv(key):
            os.environ[key] = value
            print(f"   Set {key} = {value}")
        else:
            print(f"   Using existing {key} = {os.getenv(key)}")

def test_okta_config():
    """Test OKTA configuration loading"""
    print("\n📋 Testing OKTA configuration...")
    
    try:
        from config.config import Args as args
        #args = Args.instance
        
        print(f"   OKTA Domain: {args.okta_domain}")
        print(f"   OKTA Client ID: {args.okta_client_id}")
        print(f"   OKTA Redirect URI: {args.okta_redirect_uri}")
        print(f"   Security Provider: {args.security_provider}")
        
        return True
    except Exception as e:
        print(f"   ❌ Error loading configuration: {e}")
        return False

def test_okta_auth_provider():
    """Test OKTA authentication provider"""
    print("\n🔐 Testing OKTA authentication provider...")
    
    try:
        from security.authentication_provider.okta.auth_provider import Authentication_Provider
        
        # Test JWT public key retrieval
        print("   Testing JWT public key retrieval...")
        try:
            public_key = Authentication_Provider.get_jwt_public_key('RS256')
            print(f"   ✅ Successfully retrieved public key: {type(public_key)}")
        except Exception as e:
            print(f"   ⚠️  Could not retrieve public key (OKTA may not be accessible): {e}")
        
        # Test user creation from JWT data
        print("   Testing user creation from JWT data...")
        sample_jwt_data = {
            "sub": "00u1234567890abcdef",
            "email": "test.user@example.com",
            "preferred_username": "testuser",
            "given_name": "Test",
            "family_name": "User",
            "groups": ["admin", "user"]
        }
        
        user = Authentication_Provider.get_user_from_jwt(sample_jwt_data)
        print(f"   ✅ Created user: {user.name}")
        print(f"   ✅ User roles: {[role.role_name for role in user.UserRoleList]}")
        
        return True
    except Exception as e:
        print(f"   ❌ Error testing auth provider: {e}")
        return False

def test_okta_token_validation():
    """Test OKTA token validation (requires valid token)"""
    print("\n🎫 Testing OKTA token validation...")
    
    # This would require a real token from OKTA
    print("   ⚠️  Token validation requires a real OKTA token")
    print("   To test token validation:")
    print("   1. Get a token from your OKTA application")
    print("   2. Call Authentication_Provider.validate_okta_token(token)")
    
    return True

def test_api_endpoint():
    """Test API endpoint with OKTA authentication"""
    print("\n🌐 Testing API endpoint accessibility...")
    
    try:
        # Test basic connectivity to API server
        api_url = "http://localhost:5656/api/Company"
        response = requests.get(api_url, timeout=5)
        
        if response.status_code == 401:
            print("   ✅ API requires authentication (expected with OKTA enabled)")
        elif response.status_code == 200:
            print("   ⚠️  API accessible without authentication (OKTA may not be active)")
        else:
            print(f"   ⚠️  API returned status code: {response.status_code}")
            
        return True
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to API server (http://localhost:5656)")
        print("   Make sure your API Logic Server is running")
        return False
    except Exception as e:
        print(f"   ❌ Error testing API endpoint: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 OKTA Authentication Provider Test")
    print("=" * 50)
    
    # Step 1: Setup environment
    setup_environment()
    
    # Step 2: Test configuration
    if not test_okta_config():
        print("\n❌ Configuration test failed")
        return
    
    # Step 3: Test auth provider
    if not test_okta_auth_provider():
        print("\n❌ Auth provider test failed")
        return
    
    # Step 4: Test token validation
    test_okta_token_validation()
    
    # Step 5: Test API endpoint
    test_api_endpoint()
    
    print("\n" + "=" * 50)
    print("🎉 OKTA Authentication Provider test completed!")
    print("\nNext steps:")
    print("1. Configure your OKTA application with correct redirect URIs")
    print("2. Set up proper environment variables with your OKTA credentials")
    print("3. Test with real OKTA tokens")
    print("4. Integrate with your frontend application")

if __name__ == "__main__":
    main()
