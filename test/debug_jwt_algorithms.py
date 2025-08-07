#!/usr/bin/env python3
"""
JWT Algorithm Debugging Script
This script helps diagnose JWT algorithm issues with OKTA tokens
"""

import jwt
import requests
import json
from typing import Dict, Any, Optional

def test_jwt_algorithms():
    """Test what algorithms OKTA is using"""
    
    print("🔍 OKTA JWT Algorithm Analysis")
    print("=" * 50)
    
    # Configuration
    OKTA_DOMAIN = "https://ou.okta.com"
    
    # Step 1: Get OKTA's OpenID configuration
    print("\n1️⃣ Checking OKTA OpenID Configuration...")
    try:
        config_url = f"{OKTA_DOMAIN}/.well-known/openid-configuration"
        response = requests.get(config_url, timeout=10)
        
        if response.status_code == 200:
            config = response.json()
            print(f"   ✅ Retrieved OKTA configuration")
            
            # Check supported algorithms
            algorithms = config.get('id_token_signing_alg_values_supported', [])
            print(f"   📝 Supported ID token algorithms: {algorithms}")
            
            token_endpoint_auth_methods = config.get('token_endpoint_auth_methods_supported', [])
            print(f"   📝 Token endpoint auth methods: {token_endpoint_auth_methods}")
            
            jwks_uri = config.get('jwks_uri')
            print(f"   📝 JWKS URI: {jwks_uri}")
            
            return jwks_uri, algorithms
        else:
            print(f"   ❌ Failed to get configuration: {response.status_code}")
            return None, []
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None, []

def analyze_jwks(jwks_uri: str):
    """Analyze OKTA's JWKS to see what keys are available"""
    
    print(f"\n2️⃣ Analyzing JWKS from {jwks_uri}")
    
    try:
        response = requests.get(jwks_uri, timeout=10)
        
        if response.status_code == 200:
            jwks = response.json()
            keys = jwks.get('keys', [])
            
            print(f"   ✅ Retrieved {len(keys)} keys")
            
            for i, key in enumerate(keys):
                print(f"\n   🔑 Key {i+1}:")
                print(f"      Kid: {key.get('kid', 'Not specified')}")
                print(f"      Algorithm: {key.get('alg', 'Not specified')}")
                print(f"      Key Type: {key.get('kty', 'Not specified')}")
                print(f"      Use: {key.get('use', 'Not specified')}")
                print(f"      Key Operations: {key.get('key_ops', 'Not specified')}")
                
            return keys
        else:
            print(f"   ❌ Failed to get JWKS: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []

def test_sample_token_decoding(keys: list):
    """Test decoding a sample token with different algorithms"""
    
    print(f"\n3️⃣ Testing Token Decoding...")
    
    # You would need to provide a real OKTA token here for testing
    sample_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkY2NDk2NzAxLTdDMjAtNDc3Ri1BNjdELUI1NTY3RjM5NTc3RiJ9.eyJ2ZXIiOjEsImp0aSI6IkFULlVVMmZaTlBocEdTekZ5R3VDUDNjUktKR1BzbTNnTUE4VjNhSHFhV0FiOUEiLCJpc3MiOiJodHRwczovL291Lm9rdGEuY29tIiwiYXVkIjoiYXBpOi8vZGVmYXVsdCIsImlhdCI6MTcyMzA3NDQzNCwiZXhwIjoxNzIzMDc4MDM0LCJjaWQiOiIwb2ExY3JqZml3b3hSWWFkaTB4OCIsInVpZCI6IjAwdW1pcjA3NTJVaE9IdEhpMHg4Iiwic2NwIjpbIm9wZW5pZCIsInByb2ZpbGUiLCJlbWFpbCJdLCJhdXRoX3RpbWUiOjE3MjMwNzQ0MzQsInN1YiI6IjAwdW1pcjA3NTJVaE9IdEhpMHg4In0.dummy_signature"  # This is just for header analysis
    
    try:
        # Decode just the header to see what algorithm is used
        header = jwt.get_unverified_header(sample_token)
        print(f"   📋 Sample Token Header: {json.dumps(header, indent=2)}")
        
        algorithm = header.get('alg')
        kid = header.get('kid')
        
        print(f"   📝 Token uses algorithm: {algorithm}")
        print(f"   📝 Token key ID (kid): {kid}")
        
        # Find matching key
        matching_key = None
        for key in keys:
            if key.get('kid') == kid:
                matching_key = key
                break
                
        if matching_key:
            print(f"   ✅ Found matching key in JWKS")
            print(f"      Key algorithm: {matching_key.get('alg')}")
            if algorithm != matching_key.get('alg'):
                print(f"   ⚠️  Algorithm mismatch!")
                print(f"      Token: {algorithm}")
                print(f"      Key: {matching_key.get('alg')}")
        else:
            print(f"   ❌ No matching key found for kid: {kid}")
            print(f"   Available key IDs: {[k.get('kid') for k in keys]}")
            
    except Exception as e:
        print(f"   ❌ Error analyzing token: {e}")

def test_algorithm_support():
    """Test what JWT algorithms are supported by the PyJWT library"""
    
    print(f"\n4️⃣ Testing PyJWT Algorithm Support...")
    
    try:
        from jwt.algorithms import RSAAlgorithm, HMACAlgorithm
        
        print("   📚 Supported algorithms:")
        
        # Test RSA algorithms
        rsa_algorithms = ['RS256', 'RS384', 'RS512', 'PS256', 'PS384', 'PS512']
        for alg in rsa_algorithms:
            try:
                # This will fail but tells us if the algorithm is recognized
                jwt.decode("dummy", "dummy", algorithms=[alg], options={"verify_signature": False})
                print(f"      ✅ {alg} - Supported")
            except jwt.InvalidAlgorithmError:
                print(f"      ❌ {alg} - Not supported")
            except:
                print(f"      ✅ {alg} - Supported (other error expected)")
                
    except Exception as e:
        print(f"   ❌ Error testing algorithms: {e}")

def check_flask_jwt_configuration():
    """Check how Flask-JWT-Extended is configured"""
    
    print(f"\n5️⃣ Flask-JWT-Extended Configuration Check...")
    
    try:
        import flask_jwt_extended
        from flask import Flask
        
        # Create a test app to check configuration
        test_app = Flask(__name__)
        test_app.config['JWT_ALGORITHM'] = 'RS256'
        test_app.config['JWT_SECRET_KEY'] = 'test'
        
        jwt_manager = flask_jwt_extended.JWTManager(test_app)
        
        with test_app.app_context():
            # Check what's configured
            print(f"   📝 Default algorithm: {test_app.config.get('JWT_ALGORITHM', 'Not set')}")
            print(f"   📝 Secret key set: {'JWT_SECRET_KEY' in test_app.config}")
            print(f"   📝 Public key set: {'JWT_PUBLIC_KEY' in test_app.config}")
            print(f"   📝 Identity claim: {test_app.config.get('JWT_IDENTITY_CLAIM', 'sub')}")
            
    except Exception as e:
        print(f"   ❌ Error checking Flask-JWT config: {e}")

def main():
    """Main function to run all tests"""
    
    # Run all diagnostic tests
    jwks_uri, algorithms = test_jwt_algorithms()
    
    if jwks_uri:
        keys = analyze_jwks(jwks_uri)
        if keys:
            test_sample_token_decoding(keys)
    
    test_algorithm_support()
    check_flask_jwt_configuration()
    
    # Summary
    print(f"\n📋 Summary and Recommendations:")
    print("=" * 50)
    print("1. Check that OKTA is using RS256 algorithm (most common)")
    print("2. Ensure Flask-JWT-Extended is configured for RS256")
    print("3. Verify that the JWT public key matches OKTA's JWKS")
    print("4. Consider using dynamic key resolution instead of static key")
    print("5. Check that 'alg' header in tokens matches configuration")
    
    print("\n🔧 Next Steps:")
    print("- Run this script to identify the exact algorithm mismatch")
    print("- Update JWT configuration to match OKTA's requirements")
    print("- Test with a real OKTA token from successful authentication")

if __name__ == "__main__":
    main()
