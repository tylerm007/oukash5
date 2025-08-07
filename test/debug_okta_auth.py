#!/usr/bin/env python3
"""
OKTA Authentication Debug Script
===============================

This script helps debug OKTA authentication issues, specifically the E0000004 error.

Usage:
    python debug_okta_auth.py
"""

import os
import sys
import json

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_okta_token_class():
    """Test the OktaToken class with ou.okta.com"""
    print("🔧 Testing OktaToken class with ou.okta.com...")
    
    try:
        from security.authentication_provider.okta.okta_token import OktaToken
        '''
        OKTA_CLIENT_ID = '0oa1crjfiwoxRYadi0x8'
        OKTA_CLIENT_SECRET = 'eVdobSwZgx8ANVRwPTxX6lce24t4e5ZBuAQSn_QPopvi69Xa36SWoyPjH4WcjAI7'
        OKTA_REDIRECT_URI = 'http://localhost:5656/auth/callback'
        '''
        # Initialize with ou.okta.com using HTTPS (as detected by the debug)
        okta_token = OktaToken(
            domain="https://ou.okta.com",
            client_id="0oa1crjfiwoxRYadi0x8d",
            redirect_url="http://localhost:5656/auth/callback",
            client_secret="eVdobSwZgx8ANVRwPTxX6lce24t4e5ZBuAQSn_QPopvi69Xa36SWoyPjH4WcjAI7"
        )
        
        print(f"✅ OktaToken initialized with domain: {okta_token.domain}")
        
        # Test connectivity
        print("\n🌐 Testing OKTA connectivity...")
        connectivity_results = okta_token.test_okta_connectivity()
        
        return connectivity_results["domain_accessible"] and connectivity_results["auth_endpoint_accessible"]
        
    except Exception as e:
        print(f"❌ Error testing OktaToken class: {e}")
        return False

def test_manual_auth_request():
    """Test manual authentication request to ou.okta.com"""
    print("\n🔐 Testing manual authentication request...")
    
    import requests
    
    auth_url = "https://ou.okta.com/api/v1/authn"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "API-Logic-Server-Debug/1.0"
    }
    
    # Test with intentionally invalid credentials to see the response structure
    test_payload = {
        "username": "tyler.band@ou.org",
        "password": "Tyleraum$2908",
        "options": {
            "multiOptionalFactorEnroll": False,
            "warnBeforePasswordExpired": False
        }
    }
    
    try:
        print(f"Making request to: {auth_url}")
        print(f"Headers: {json.dumps(headers, indent=2)}")
        print(f"Payload: {json.dumps(test_payload, indent=2)}")
        
        response = requests.post(
            auth_url,
            headers=headers,
            json=test_payload,
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {json.dumps(response.text, indent=2)}")
        
        if response.status_code == 401:
            try:
                error_data = response.json()
                print(f"\n📋 Error Analysis:")
                print(f"  Error Code: {error_data.get('errorCode', 'Unknown')}")
                print(f"  Error Summary: {error_data.get('errorSummary', 'Unknown')}")
                print(f"  Error Causes: {error_data.get('errorCauses', [])}")
                print(f"  Error Link: {error_data.get('errorLink', 'None')}")
                
                # Provide specific guidance based on error code
                error_code = error_data.get('errorCode')
                if error_code == "E0000004":
                    print(f"\n💡 E0000004 Troubleshooting:")
                    print(f"  1. Check if the username/password are correct")
                    print(f"  2. Verify the user account exists in OKTA")
                    print(f"  3. Check if the account is locked or disabled")
                    print(f"  4. Verify the OKTA domain is correct")
                    print(f"  5. Check if your IP is allowed in OKTA network policies")
                    print(f"  6. Verify the application has permission to authenticate users")
                elif error_code == "E0000001":
                    print(f"\n💡 E0000001 Troubleshooting:")
                    print(f"  1. Check the request format and required fields")
                    print(f"  2. Verify Content-Type is application/json")
                    print(f"  3. Check if all required parameters are present")
                
            except json.JSONDecodeError:
                print("  Could not parse error response as JSON")
        
        return response.status_code in [200, 401]  # Both are valid responses
        
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        print("💡 This could mean:")
        print("  1. ou.okta.com is not accessible from your network")
        print("  2. The domain doesn't exist or is misconfigured")
        print("  3. Firewall blocking the connection")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_oauth_endpoints():
    """Test OAuth-related endpoints"""
    print("\n🔑 Testing OAuth endpoints...")
    
    import requests
    
    base_domain = "https://ou.okta.com"
    
    # Test well-known configuration endpoints
    endpoints_to_test = [
        "/oauth2/.well-known/openid-configuration",
        "/oauth2/.well-known/oauth-authorization-server",
        "/.well-known/openid-configuration"
    ]
    
    for endpoint in endpoints_to_test:
        url = f"{base_domain}{endpoint}"
        try:
            print(f"Testing: {url}")
            response = requests.get(url, timeout=10)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    config = response.json()
                    print(f"  ✅ Valid OpenID configuration found")
                    print(f"    Issuer: {config.get('issuer', 'Not found')}")
                    print(f"    Auth endpoint: {config.get('authorization_endpoint', 'Not found')}")
                    print(f"    Token endpoint: {config.get('token_endpoint', 'Not found')}")
                    print(f"    JWKS URI: {config.get('jwks_uri', 'Not found')}")
                    return True
                except json.JSONDecodeError:
                    print(f"  ⚠️  Response not valid JSON")
            else:
                print(f"  ❌ Endpoint not accessible")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    return False

def provide_troubleshooting_guide():
    """Provide comprehensive troubleshooting guide"""
    print("\n📚 OKTA E0000004 Troubleshooting Guide:")
    print("=" * 50)
    
    print("\n1. **Verify OKTA Domain Configuration:**")
    print("   - Check if 'http://ou.okta.com' is the correct domain")
    print("   - Try with 'https://ou.okta.com' if HTTP doesn't work")
    print("   - Verify the domain in your OKTA admin console")
    
    print("\n2. **Check User Credentials:**")
    print("   - Verify username format (email vs username)")
    print("   - Ensure password is correct")
    print("   - Check if account is active in OKTA")
    
    print("\n3. **Application Configuration:**")
    print("   - Verify the OKTA application is configured correctly")
    print("   - Check if the application has 'Authentication' permission")
    print("   - Ensure the client ID and secret are correct")
    
    print("\n4. **Network and Security:**")
    print("   - Check firewall settings")
    print("   - Verify network policies in OKTA allow your IP")
    print("   - Test from different network if possible")
    
    print("\n5. **API Endpoint Verification:**")
    print("   - Test if /api/v1/authn endpoint exists")
    print("   - Try OAuth 2.0 flow instead of direct authentication")
    print("   - Check OKTA API version compatibility")
    
    print("\n6. **Alternative Approaches:**")
    print("   - Use OAuth 2.0 Authorization Code flow instead")
    print("   - Implement SAML authentication if available")
    print("   - Contact OKTA administrator for domain verification")

def main():
    """Main debug function"""
    print("🔍 OKTA Authentication Debug Tool")
    print("=" * 50)
    print("This tool helps debug the E0000004 authentication error")
    
    # Test 1: OktaToken class
    okta_token_working = test_okta_token_class()
    
    # Test 2: Manual auth request
    manual_auth_working = test_manual_auth_request()
    
    # Test 3: OAuth endpoints
    oauth_working = test_oauth_endpoints()
    
    # Test 4: Provide troubleshooting guide
    provide_troubleshooting_guide()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 Debug Summary:")
    print(f"   OktaToken Class:    {'✅ Working' if okta_token_working else '❌ Issues'}")
    print(f"   Manual Auth Test:   {'✅ Working' if manual_auth_working else '❌ Issues'}")
    print(f"   OAuth Endpoints:    {'✅ Working' if oauth_working else '❌ Issues'}")
    
    if not any([okta_token_working, manual_auth_working, oauth_working]):
        print("\n⚠️  All tests failed - likely connectivity or domain configuration issue")
        print("Recommended actions:")
        print("1. Verify 'http://ou.okta.com' is the correct domain")
        print("2. Check network connectivity")
        print("3. Contact your OKTA administrator")
    elif manual_auth_working:
        print("\n✅ OKTA endpoints are accessible!")
        print("The E0000004 error is likely due to:")
        print("1. Invalid username/password")
        print("2. Account locked/disabled")
        print("3. Application configuration issues")

if __name__ == "__main__":
    main()
