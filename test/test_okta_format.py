#!/usr/bin/env python3
"""
Test with a more realistic OKTA token format
"""

import requests
import json
import jwt
import base64

def test_with_okta_format():
    """Test with a token that looks like a real OKTA token"""
    
    print("🔧 Testing with OKTA Token Format")
    print("=" * 50)
    
    # Create a token with OKTA-like structure but invalid signature
    # This tests if our validate_okta_token method is being called
    header = {
        "alg": "RS256",
        "kid": "hJBgY87mCBIVE0ic61piXUTzXK-CABidhlFNHAgQuqc",  # Current OKTA key ID
        "typ": "JWT"
    }
    
    payload = {
        "ver": 1,
        "jti": "AT.test-token",
        "iss": "https://ou.okta.com",
        "aud": "api://default",
        "sub": "testuser",
        "exp": 9999999999,  # Far future
        "iat": 1723074434,
        "cid": "0oa1crjfiwoxRYadi0x8",
        "uid": "testuser",
        "scp": ["openid", "profile", "email"]
    }
    
    # Create token with invalid signature (we can't create valid signature without private key)
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    token = f"{header_b64}.{payload_b64}.invalid_signature"
    
    print(f"Testing with OKTA-format token (header shows RS256/OKTA kid)")
    
    base_url = "http://localhost:5656"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(f"{base_url}/api/COMPANYTB", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.content:
            try:
                response_data = response.json()
                print(f"Response: {response_data}")
            except:
                print(f"Response text: {response.text[:300]}")
        
        if response.status_code == 422:
            if "Invalid crypto padding" in response.text:
                print("❌ Still getting crypto padding error - monkey patch may not be working")
            elif "Signature verification failed" in response.text:
                print("❌ Still getting signature verification error")
            elif "Could not retrieve OKTA" in response.text:
                print("✅ Good! validate_okta_token is being called but failing on JWKS (expected)")
            else:
                print("📝 Different 422 error - need to investigate")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_with_okta_format()
