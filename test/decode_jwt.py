#!/usr/bin/env python3
"""
JWT Token Decoder - Extract expiration and other claims from JWT tokens
Usage: python decode_jwt.py <token>
"""

import sys
import json
import base64
from datetime import datetime, timezone
import argparse

def decode_jwt_payload(token):
    """Decode JWT token payload without signature verification"""
    try:
        # Split token into parts
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid JWT format")
        
        # Get payload (second part)
        payload = parts[1]
        
        # Add padding if needed
        payload += '=' * (4 - len(payload) % 4)
        
        # Decode base64
        decoded_bytes = base64.urlsafe_b64decode(payload)
        payload_json = json.loads(decoded_bytes.decode('utf-8'))
        
        return payload_json
    
    except Exception as e:
        raise ValueError(f"Failed to decode token: {e}")

def format_timestamp(timestamp):
    """Convert Unix timestamp to readable format"""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

def main():
    parser = argparse.ArgumentParser(description='Decode JWT token and show expiration info')
    parser.add_argument('token', help='JWT token to decode')
    
    args = parser.parse_args()
    
    try:
        payload = decode_jwt_payload(args.token)
        
        print("🔓 JWT Token Decoded:")
        print(f"   Subject (sub): {payload.get('sub', 'N/A')}")
        print(f"   Token Type: {payload.get('type', 'N/A')}")
        print(f"   Fresh: {payload.get('fresh', 'N/A')}")
        print(f"   JTI: {payload.get('jti', 'N/A')}")
        print()
        
        # Timestamp information
        iat = payload.get('iat')
        exp = payload.get('exp')
        nbf = payload.get('nbf')
        
        print("⏰ Timestamp Information:")
        if iat:
            print(f"   Issued At (iat): {iat} -> {format_timestamp(iat)}")
        if nbf:
            print(f"   Not Before (nbf): {nbf} -> {format_timestamp(nbf)}")
        if exp:
            print(f"   Expires (exp): {exp} -> {format_timestamp(exp)}")
            
            # Check expiration
            now = datetime.now(timezone.utc).timestamp()
            if now > exp:
                print("   ⚠️  STATUS: TOKEN IS EXPIRED!")
            else:
                remaining = exp - now
                hours = int(remaining // 3600)
                minutes = int((remaining % 3600) // 60)
                seconds = int(remaining % 60)
                print(f"   ✅ STATUS: Valid for {hours}h {minutes}m {seconds}s")
        
        print()
        print("📋 Full Payload:")
        print(json.dumps(payload, indent=2))
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()