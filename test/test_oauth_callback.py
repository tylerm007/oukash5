#!/usr/bin/env python3
"""
OKTA OAuth Callback Debug Script
===============================

This script helps debug issues with the OAuth callback not receiving the authorization code.

Usage:
    python test_oauth_callback.py
"""

import requests
import urllib.parse
from urllib.parse import urlparse, parse_qs

def test_oauth_flow():
    """Test the OAuth flow step by step"""
    print("🔍 Testing OKTA OAuth Flow")
    print("=" * 50)
    
    # Configuration (update with your actual values)
    okta_domain = "https://ou.okta.com"
    client_id = "your-client-id"  # Replace with actual client ID
    redirect_uri = "http://localhost:5656/auth/callback"
    
    print(f"OKTA Domain: {okta_domain}")
    print(f"Client ID: {client_id}")
    print(f"Redirect URI: {redirect_uri}")
    
    # Step 1: Test authorization URL generation
    print("\n📋 Step 1: Authorization URL Generation")
    auth_params = {
        'client_id': client_id,
        'response_type': 'code',
        'response_mode': 'query',
        'scope': 'openid profile email',
        'redirect_uri': redirect_uri,
        'state': 'test-state-123',
        'nonce': 'test-nonce-456'
    }
    
    auth_url = f"{okta_domain}/oauth2/v1/authorize?" + urllib.parse.urlencode(auth_params)
    print(f"Generated URL: {auth_url}")
    
    # Parse and verify URL components
    parsed_url = urlparse(auth_url)
    query_params = parse_qs(parsed_url.query)
    
    print(f"\n📋 URL Components:")
    print(f"  Domain: {parsed_url.scheme}://{parsed_url.netloc}")
    print(f"  Path: {parsed_url.path}")
    print(f"  Response Type: {query_params.get('response_type', ['Not found'])[0]}")
    print(f"  Scope: {query_params.get('scope', ['Not found'])[0]}")
    print(f"  Redirect URI: {query_params.get('redirect_uri', ['Not found'])[0]}")
    
    # Step 2: Test authorization endpoint
    print(f"\n🌐 Step 2: Testing Authorization Endpoint")
    try:
        # Make a HEAD request to check if endpoint exists
        response = requests.head(f"{okta_domain}/oauth2/v1/authorize", timeout=10)
        print(f"  Endpoint Status: {response.status_code}")
        
        if response.status_code in [200, 302, 400]:
            print(f"  ✅ Authorization endpoint accessible")
        else:
            print(f"  ⚠️  Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Error testing authorization endpoint: {e}")
    
    # Step 3: Test callback endpoint (your local server)
    print(f"\n🔗 Step 3: Testing Local Callback Endpoint")
    try:
        # Test if your local server is running
        callback_response = requests.get("http://localhost:5656/auth/debug", timeout=5)
        if callback_response.status_code == 200:
            debug_info = callback_response.json()
            print(f"  ✅ Local server accessible")
            print(f"  Server OKTA Domain: {debug_info.get('okta_domain', 'Not set')}")
            print(f"  Server Client ID: {debug_info.get('okta_client_id', 'Not set')}")
            print(f"  Server Redirect URI: {debug_info.get('okta_redirect_uri', 'Not set')}")
        else:
            print(f"  ⚠️  Debug endpoint returned: {callback_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"  ❌ Local server not running on http://localhost:5656")
        print(f"  Start your API Logic Server first")
    except Exception as e:
        print(f"  ❌ Error testing local server: {e}")

def test_manual_callback_simulation():
    """Simulate a callback with parameters to test the endpoint"""
    print(f"\n🧪 Step 4: Simulating OAuth Callback")
    
    # Simulate what OKTA would send back
    callback_params = {
        'code': 'test-authorization-code-123',
        'state': 'test-state-123'
    }
    
    callback_url = "http://localhost:5656/auth/callback?" + urllib.parse.urlencode(callback_params)
    print(f"Simulated callback URL: {callback_url}")
    
    try:
        response = requests.get(callback_url, timeout=10)
        print(f"Callback response status: {response.status_code}")
        print(f"Callback response: {response.text[:200]}...")
        
        if response.status_code == 400:
            print("  ⚠️  This is expected if state doesn't match session state")
        elif response.status_code == 500:
            print("  ⚠️  Server error - check logs for details")
        else:
            print("  ✅ Callback endpoint processed the request")
            
    except requests.exceptions.ConnectionError:
        print("  ❌ Cannot connect to callback endpoint - server not running")
    except Exception as e:
        print(f"  ❌ Error testing callback: {e}")

def provide_troubleshooting_steps():
    """Provide troubleshooting steps for common issues"""
    print(f"\n📚 Troubleshooting Steps:")
    print("=" * 50)
    
    print("\n1. **Check OKTA Application Configuration:**")
    print("   - Login to ou.okta.com admin console")
    print("   - Go to Applications → Your App")
    print("   - Verify Grant Types include 'Authorization Code'")
    print("   - Check Sign-in redirect URIs include: http://localhost:5656/auth/callback")
    
    print("\n2. **Verify Response Type:**")
    print("   - Ensure response_type=code (not token or id_token)")
    print("   - Check response_mode=query (not fragment)")
    
    print("\n3. **Check Scopes:**")
    print("   - Use standard OpenID scopes: 'openid profile email'")
    print("   - Avoid custom scopes like 'webAccess' for authorization code flow")
    
    print("\n4. **Debug the Actual Flow:**")
    print("   - Navigate to: http://localhost:5656/auth/login")
    print("   - Check browser network tab for redirect URLs")
    print("   - Look at the URL when OKTA redirects back")
    
    print("\n5. **Common Issues:**")
    print("   - Client ID mismatch between app and OKTA configuration")
    print("   - Redirect URI not exactly matching OKTA config")
    print("   - Application not assigned to users")
    print("   - Application disabled or in wrong state")

def main():
    """Main test function"""
    test_oauth_flow()
    test_manual_callback_simulation()
    provide_troubleshooting_steps()
    
    print(f"\n🎯 Next Steps:")
    print("1. Start your API Logic Server")
    print("2. Navigate to http://localhost:5656/auth/login")
    print("3. Check the browser network tab during the redirect")
    print("4. Look at server logs for callback debugging info")

if __name__ == "__main__":
    main()
