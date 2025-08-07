#!/usr/bin/env python3
"""
OKTA SSO Test Script
====================

This script tests the OKTA SSO redirection to http://ou.okta.com

Usage:
    python test_okta_sso.py
"""

import os
import sys
import requests
from urllib.parse import urlparse, parse_qs

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_environment():
    """Set up environment variables for ou.okta.com"""
    print("🔧 Setting up OKTA environment for ou.okta.com...")
    '''
Client ID: 0oa1crjfiwoxRYadi0x8
Secret: eVdobSwZgx8ANVRwPTxX6lce24t4e5ZBuAQSn_QPopvi69Xa36SWoyPjH4WcjAI7
'''
    env_vars = {
        'OKTA_DOMAIN': 'https://ou.okta.com',
        'OKTA_CLIENT_ID': '0oa1crjfiwoxRYadi0x8',
        'OKTA_CLIENT_SECRET': 'eVdobSwZgx8ANVRwPTxX6lce24t4e5ZBuAQSn_QPopvi69Xa36SWoyPjH4WcjAI7',
        'OKTA_REDIRECT_URI': 'http://localhost:5656/auth/callback',
        'SECURITY_ENABLED': 'true',
        'SECURITY_PROVIDER': 'okta'
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"   Set {key} = {value}")

def test_okta_connectivity():
    """Test connectivity to ou.okta.com"""
    print("\n🌐 Testing connectivity to ou.okta.com...")
    
    try:
        # Test basic connectivity
        response = requests.get('https://ou.okta.com', timeout=5)
        print(f"   ✅ Basic connectivity: {response.status_code}")
        
        # Test OKTA well-known configuration endpoint
        config_url = 'https://ou.okta.com/.well-known/openid-configuration'
        config_response = requests.get(config_url, timeout=5)
        
        if config_response.status_code == 200:
            config_data = config_response.json()
            print(f"   ✅ OpenID configuration accessible")
            print(f"   Issuer: {config_data.get('issuer', 'Not found')}")
            print(f"   Authorization endpoint: {config_data.get('authorization_endpoint', 'Not found')}")
            print(f"   Token endpoint: {config_data.get('token_endpoint', 'Not found')}")
            print(f"   JWKS URI: {config_data.get('jwks_uri', 'Not found')}")
            return True
        else:
            print(f"   ⚠️  OpenID configuration not accessible: {config_response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to ou.okta.com")
        return False
    except Exception as e:
        print(f"   ❌ Error testing connectivity: {e}")
        return False

def test_sso_redirection():
    """Test SSO redirection logic"""
    print("\n🔐 Testing SSO redirection logic...")
    
    try:
        from security.authentication_provider.okta.auth_provider import Authentication_Provider
        from config.config import Args as args
        
        #args = Args.instance
        print(f"   OKTA Domain: {args.okta_domain}")
        print(f"   Client ID: {args.okta_client_id}")
        print(f"   Redirect URI: {args.okta_redirect_uri}")
        
        # Test building authorization URL
        import urllib.parse
        auth_params = {
            'client_id': args.okta_client_id,
            'response_type': 'code',
            'response_mode': 'query',
            'scope':'openid profile email groups',
            'redirect_uri': args.okta_redirect_uri,
            'state': 'test-state-123',
            'nonce': 'test-nonce-456'
        }
        
        auth_url = f"{args.okta_domain}/oauth2/v1/authorize?" + urllib.parse.urlencode(auth_params)
        print(f"\n   📍 Generated SSO URL:")
        print(f"   {auth_url}")
        
        # Parse the URL to verify components
        parsed = urlparse(auth_url)
        params = parse_qs(parsed.query)
        
        print(f"\n   📋 URL Components:")
        print(f"   Domain: {parsed.scheme}://{parsed.netloc}")
        print(f"   Path: {parsed.path}")
        print(f"   Client ID: {params.get('client_id', ['Not found'])[0]}")
        print(f"   Response Type: {params.get('response_type', ['Not found'])[0]}")
        print(f"   Scope: {params.get('scope', ['Not found'])[0]}")
        print(f"   Redirect URI: {params.get('redirect_uri', ['Not found'])[0]}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing SSO redirection: {e}")
        return False

def test_api_server_endpoints():
    """Test that the API server endpoints are set up correctly"""
    print("\n🌐 Testing API server endpoints...")
    
    try:
        # Test if API server is running
        base_url = "http://localhost:5656"
        
        # Test basic connectivity
        response = requests.get(base_url, timeout=2)
        print(f"   ✅ API server accessible: {response.status_code}")
        
        # Test auth endpoints
        auth_endpoints = ['/auth/login', '/auth/callback', '/auth/logout', '/auth/user']

        for endpoint in auth_endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=2, allow_redirects=False)
                if response.status_code in [200, 302, 401]:  # Expected status codes
                    print(f"   ✅ {endpoint}: {response.status_code} - {response.reason} - {response.text}")
                else:
                    print(f"   ⚠️  {endpoint}: {response.status_code}")
            except requests.exceptions.ConnectionError:
                print(f"   ❌ {endpoint}: Not accessible (server may not be running)")
            except Exception as e:
                print(f"   ❌ {endpoint}: Error - {e}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ❌ API server not running on http://localhost:5656")
        print("   Start your API Logic Server to test endpoints")
        return False
    except Exception as e:
        print(f"   ❌ Error testing API server: {e}")
        return False

def show_integration_instructions():
    """Show instructions for integrating with frontend"""
    print("\n📚 Frontend Integration Instructions:")
    print("=" * 50)
    
    print("\n1. **HTML/JavaScript Integration:**")
    print("   ```html")
    print("   <button onclick=\"window.location.href='/auth/login'\">Login with OKTA</button>")
    print("   ```")
    
    print("\n2. **React Integration:**")
    print("   ```javascript")
    print("   const handleLogin = () => {")
    print("     window.location.href = '/auth/login';")
    print("   };")
    print("   ```")
    
    print("\n3. **Check Authentication Status:**")
    print("   ```javascript")
    print("   fetch('/auth/user')")
    print("     .then(response => response.json())")
    print("     .then(data => {")
    print("       if (data.authenticated) {")
    print("         console.log('User:', data.user_id);")
    print("         console.log('Roles:', data.roles);")
    print("       }")
    print("     });")
    print("   ```")
    
    print("\n4. **Logout:**")
    print("   ```javascript")
    print("   window.location.href = '/auth/logout';")
    print("   ```")

def main():
    """Main test function"""
    print("🚀 OKTA SSO Test for ou.okta.com")
    print("=" * 50)
    
    # Step 1: Setup environment
    setup_environment()
    
    # Step 2: Test OKTA connectivity
    okta_accessible = test_okta_connectivity()
    
    # Step 3: Test SSO redirection logic
    sso_working = test_sso_redirection()
    
    # Step 4: Test API server endpoints
    api_working = test_api_server_endpoints()
    
    # Step 5: Show integration instructions
    show_integration_instructions()
    
    print("\n" + "=" * 50)
    print("🎯 Test Results Summary:")
    print(f"   OKTA Connectivity: {'✅ Pass' if okta_accessible else '❌ Fail'}")
    print(f"   SSO Redirection:   {'✅ Pass' if sso_working else '❌ Fail'}")
    print(f"   API Endpoints:     {'✅ Pass' if api_working else '⚠️  Server not running'}")
    
    if okta_accessible and sso_working:
        print("\n🎉 OKTA SSO is configured correctly!")
        print("Next steps:")
        print("1. Start your API Logic Server")
        print("2. Navigate to http://localhost:5656/auth/login")
        print("3. You should be redirected to ou.okta.com for authentication")
    else:
        print("\n⚠️  Some issues detected:")
        if not okta_accessible:
            print("- Check network connectivity to ou.okta.com")
            print("- Verify OKTA domain configuration")
        if not sso_working:
            print("- Check OKTA client configuration")
            print("- Verify environment variables")

if __name__ == "__main__":
    main()
