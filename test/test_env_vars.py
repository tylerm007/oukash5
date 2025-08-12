#!/usr/bin/env python3
"""
Test environment variables setup
"""

import os

def test_env_vars():
    """Test if OKTA environment variables are set"""
    print("🔧 Testing Environment Variables")
    print("=" * 40)
    
    required_vars = {
        'OKTA_DOMAIN': 'OKTA domain URL',
        'OKTA_CLIENT_ID': 'OAuth client ID', 
        'OKTA_CLIENT_SECRET': 'OAuth client secret',
        'OKTA_API_TOKEN': 'API token for user lookup'
    }
    
    all_set = True
    
    for var_name, description in required_vars.items():
        value = os.getenv(var_name)
        if value:
            # Show partial value for security
            if len(value) > 10:
                display_value = value[:4] + "..." + value[-4:]
            else:
                display_value = value[:2] + "..."
            print(f"✅ {var_name}: {display_value}")
        else:
            print(f"❌ {var_name}: Not set")
            print(f"   Description: {description}")
            all_set = False
    
    print("\n" + "=" * 40)
    if all_set:
        print("✅ All environment variables are set!")
        print("You can now use the OKTA user lookup functions.")
    else:
        print("❌ Some environment variables are missing.")
        print("\nTo set them:")
        print("Windows PowerShell:")
        print('$env:OKTA_API_TOKEN="your_token"')
        print("\nWindows Command Prompt:")
        print('set OKTA_API_TOKEN=your_token')
        print("\nOr add to your .env file:")
        print('OKTA_API_TOKEN=your_token')
    
    return all_set

if __name__ == "__main__":
    test_env_vars()
