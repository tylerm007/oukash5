#!/usr/bin/env python3
"""
Generate a test OKTA authorization URL to see a real authorization code
"""

import secrets
from urllib.parse import urlencode

def generate_test_url():
    """Generate a test authorization URL for OKTA"""
    
    # Your OKTA configuration
    OKTA_DOMAIN = "https://ou.okta.com"
    CLIENT_ID = "0oa1crjfiwoxRYadi0x8"
    REDIRECT_URI = "http://localhost:5555/auth/callback"  # Use callback inspector
    
    # Generate security parameters
    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)
    
    # Authorization parameters
    auth_params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'openid profile email',
        'state': state,
        'nonce': nonce
    }
    
    # Build authorization URL
    auth_url = f"{OKTA_DOMAIN}/oauth2/v1/authorize?{urlencode(auth_params)}"
    
    print("🔗 OKTA Authorization Test URL")
    print("=" * 50)
    print(f"📍 Redirect URI: {REDIRECT_URI}")
    print(f"📝 State: {state}")
    print(f"📝 Nonce: {nonce}")
    print()
    print("🌐 Copy this URL to your browser:")
    print(auth_url)
    print()
    print("📋 Steps to test:")
    print("1. Make sure the callback inspector is running on port 5555")
    print("2. Add this redirect URI to your OKTA app: http://localhost:5555/auth/callback")
    print("3. Copy the URL above and paste it in your browser")
    print("4. Log in with your OKTA credentials")
    print("5. Check the callback inspector console for the authorization code")
    print("6. Visit http://localhost:5555/auth/debug to see all received callbacks")
    print()
    print("🔍 What you'll see:")
    print("- In browser: You'll be redirected back with ?code=... in the URL")
    print("- In inspector: Console will show the authorization code details")
    print("- Authorization code will look like: 'AbC123XyZ456...' (30-50 characters)")

if __name__ == "__main__":
    generate_test_url()
