#!/usr/bin/env python3
"""
Quick OKTA User Lookup Test
Run this to test OKTA user information retrieval
"""

import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_setup():
    """Test if everything is configured correctly"""
    print("🔧 Testing OKTA Configuration...")
    
    # Check environment variables
    required_vars = ['OKTA_DOMAIN', 'OKTA_CLIENT_ID', 'OKTA_CLIENT_SECRET']
    optional_vars = ['OKTA_API_TOKEN']
    
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        status = "✅" if value else "❌"
        print(f"   {var}: {status}")
        if not value:
            all_good = False
    
    for var in optional_vars:
        value = os.getenv(var)
        status = "✅" if value else "⚠️ "
        print(f"   {var}: {status}")
        if not value:
            print(f"      Note: {var} needed for user lookup functionality")
    
    return all_good

def quick_test(email=None):
    """Quick test of user lookup functionality"""
    
    if not email:
        # Use a test email or get from user
        email = input("\nEnter email to test (or press Enter to skip): ").strip()
        if not email:
            print("Skipping user lookup test")
            return
    
    print(f"\n🔍 Testing user lookup for: {email}")
    
    try:
        # Test the authentication provider directly
        from security.authentication_provider.okta.auth_provider import Authentication_Provider
        
        # Method 1: Get full user info
        print("   Testing get_user_by_email...")
        user_info = Authentication_Provider.get_user_by_email(email)
        
        if user_info:
            print(f"   ✅ User found: {user_info.get('displayName')}")
            print(f"      Status: {user_info.get('status')}")
            groups = user_info.get('groups', [])
            print(f"      Groups: {[g['name'] for g in groups if g.get('name')]}")
        else:
            print(f"   ❌ User not found or error occurred")
        
        # Method 2: Get just roles
        print("   Testing get_user_roles_by_email...")
        roles = Authentication_Provider.get_user_roles_by_email(email)
        print(f"   Roles: {roles}")
        
        # Method 3: Create auth user object
        print("   Testing create_user_from_okta_email...")
        auth_user = Authentication_Provider.create_user_from_okta_email(email)
        if auth_user:
            print(f"   ✅ Auth user created: {auth_user.name}")
            print(f"      Roles in auth object: {[r.role_name for r in auth_user.UserRoleList]}")
        else:
            print(f"   ❌ Could not create auth user object")
            
    except Exception as e:
        print(f"   ❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main test function"""
    print("🚀 OKTA User Lookup Quick Test")
    print("=" * 40)
    
    # Test configuration
    config_ok = test_setup()
    
    if not config_ok:
        print("\n❌ Configuration incomplete!")
        print("\nRequired setup:")
        print("1. Set OKTA_DOMAIN, OKTA_CLIENT_ID, OKTA_CLIENT_SECRET in environment")
        print("2. Set OKTA_API_TOKEN for user lookup functionality")
        print("\nExample:")
        print('set OKTA_API_TOKEN=your_api_token_here')
        return
    
    # Check if API token is available
    api_token = os.getenv('OKTA_API_TOKEN')
    if not api_token:
        print("\n⚠️  OKTA_API_TOKEN not set!")
        print("User lookup functions will not work without this.")
        print("Get an API token from OKTA Admin Console > Security > API > Tokens")
        return
    
    print("\n✅ Configuration looks good!")
    
    # Run quick test
    quick_test()
    
    print("\n📋 If this worked, you can now use:")
    print("- Authentication_Provider.get_user_by_email(email)")
    print("- Authentication_Provider.get_user_roles_by_email(email)")
    print("- Authentication_Provider.create_user_from_okta_email(email)")

if __name__ == "__main__":
    main()
