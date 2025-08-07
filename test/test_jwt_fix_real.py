#!/usr/bin/env python3
"""
Test the JWT fix with a real REST API call
"""

import requests
import json

def test_jwt_fix():
    """Test the JWT algorithm fix with actual REST API calls"""
    
    print("🔧 Testing JWT Fix with REST API Calls")
    print("=" * 50)
    
    base_url = "http://localhost:5656"
    
    # Test 1: Call without authentication (should get 401)
    print("\n1️⃣ Testing API call without authentication...")
    try:
        response = requests.get(f"{base_url}/api/COMPANYTB", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Expected 401 - authentication required")
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Call with invalid Bearer token (should get 422 before fix, different after fix)
    print("\n2️⃣ Testing API call with invalid Bearer token...")
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkY2NDk2NzAxLTdDMjAtNDc3Ri1BNjdELUI1NTY3RjM5NTc3RiJ9.invalid.signature'
    }
    
    try:
        response = requests.get(f"{base_url}/api/COMPANYTB", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 422:
            response_data = response.json() if response.content else {}
            if "Signature verification failed" in response.text:
                print("   ❌ Still getting signature verification failed - fix didn't work")
            elif "alg value is not allowed" in response.text:
                print("   ❌ Still getting alg value not allowed - fix didn't work")
            else:
                print(f"   📝 422 response: {response_data}")
        elif response.status_code == 401:
            print("   ✅ Now getting 401 instead of 422 - signature issue resolved!")
        else:
            print(f"   📝 Status {response.status_code}: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Check OKTA login endpoint
    print("\n3️⃣ Testing OKTA login endpoint...")
    try:
        response = requests.get(f"{base_url}/auth/login", allow_redirects=False, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 302:
            location = response.headers.get('Location', '')
            if 'ou.okta.com' in location:
                print("   ✅ OKTA login redirect working")
            else:
                print(f"   ⚠️  Unexpected redirect: {location}")
        else:
            print(f"   📝 Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Summary
    print("\n📋 Test Results Summary:")
    print("- If you see 'Signature verification failed' or 'alg value not allowed', the fix needs work")
    print("- If you get 401 errors instead of 422, the JWT signature issue is resolved")
    print("- Next step: Get a valid OKTA token to test full authentication flow")

if __name__ == "__main__":
    test_jwt_fix()
