#!/usr/bin/env python3
"""
OKTA User Information Retrieval Utility
This script demonstrates how to retrieve user information including roles from OKTA by email address.
"""

import sys
import os
import logging
from typing import Optional, Dict, Any, List

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OKTA_CLIENT_ID = '0oa1crjfiwoxRYadi0x8'
OKTA_CLIENT_SECRET = 'eVdobSwZgx8ANVRwPTxX6lce24t4e5ZBuAQSn_QPopvi69Xa36SWoyPjH4WcjAI7'
OKTA_DOMAIN = "https://ou.okta.com"
OKTA_API_TOKEN = 'your_api_token_here'

def get_okta_user_info(email: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve OKTA user information by email address
    
    Args:
        email: User's email address
        
    Returns:
        Dictionary with user information and roles
    """
    try:
        # Import the authentication provider
        from security.authentication_provider.okta.auth_provider import Authentication_Provider
        
        print(f"🔍 Searching for OKTA user: {email}")
        user_info = Authentication_Provider.get_user_by_email(email)
        
        if user_info:
            print(f"✅ Found user: {user_info.get('displayName', user_info.get('login'))}")
            return user_info
        else:
            print(f"❌ User not found: {email}")
            return None
            
    except Exception as e:
        print(f"❌ Error retrieving user info: {e}")
        logger.error(f"Error in get_okta_user_info: {e}")
        return None


def display_user_info(user_info: Dict[str, Any]) -> None:
    """
    Display user information in a formatted way
    
    Args:
        user_info: User information dictionary
    """
    print("\n" + "="*60)
    print("📋 OKTA USER INFORMATION")
    print("="*60)
    
    # Basic Info
    print(f"👤 Name: {user_info.get('displayName', 'N/A')}")
    print(f"📧 Email: {user_info.get('email', 'N/A')}")
    print(f"🔑 Login: {user_info.get('login', 'N/A')}")
    print(f"🆔 User ID: {user_info.get('id', 'N/A')}")
    print(f"📊 Status: {user_info.get('status', 'N/A')}")
    
    # Timestamps
    if user_info.get('created'):
        print(f"📅 Created: {user_info['created']}")
    if user_info.get('lastLogin'):
        print(f"🕐 Last Login: {user_info['lastLogin']}")
    
    # Groups/Roles
    groups = user_info.get('groups', [])
    print(f"\n👥 Groups/Roles ({len(groups)}):")
    if groups:
        for i, group in enumerate(groups, 1):
            print(f"   {i}. {group.get('name', 'Unnamed Group')}")
            if group.get('description'):
                print(f"      Description: {group['description']}")
            print(f"      Type: {group.get('type', 'Unknown')}")
            print(f"      ID: {group.get('id', 'N/A')}")
            print()
    else:
        print("   No groups/roles assigned")
    
    # Additional Profile Info
    profile = user_info.get('profile', {})
    if profile:
        print("📝 Additional Profile Information:")
        for key, value in profile.items():
            if key not in ['email', 'firstName', 'lastName', 'login']:
                print(f"   {key}: {value}")


def get_user_roles_only(email: str) -> List[str]:
    """
    Get just the role names for a user
    
    Args:
        email: User's email address
        
    Returns:
        List of role names
    """
    try:
        from security.authentication_provider.okta.auth_provider import Authentication_Provider
        
        roles = Authentication_Provider.get_user_roles_by_email(email)
        return roles
        
    except Exception as e:
        print(f"❌ Error getting user roles: {e}")
        return []


def create_auth_user_object(email: str):
    """
    Create an authentication user object from OKTA email
    
    Args:
        email: User's email address
        
    Returns:
        DotMapX user object ready for authentication system
    """
    try:
        from security.authentication_provider.okta.auth_provider import Authentication_Provider
        
        user_obj = Authentication_Provider.create_user_from_okta_email(email)
        if user_obj:
            print(f"✅ Created user object for: {user_obj.name}")
            print(f"   Roles: {[role.role_name for role in user_obj.UserRoleList]}")
            return user_obj
        else:
            print(f"❌ Could not create user object for: {email}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating user object: {e}")
        return None


def test_okta_api_connectivity():
    """
    Test OKTA API connectivity and configuration
    """
    print("🔧 Testing OKTA API Connectivity")
    print("-" * 40)
    
    # Check environment variables
    import os
 
    api_token = os.getenv('OKTA_API_TOKEN','x')
    okta_domain = os.getenv('OKTA_DOMAIN','https://ou.okta.com')
    client_id = os.getenv('OKTA_CLIENT_ID','0oa1crjfiwoxRYadi0x8')
    client_secret = os.getenv('OKTA_CLIENT_SECRET','eVdobSwZgx8ANVRwPTxX6lce24t4e5ZBuAQSn_QPopvi69Xa36SWoyPjH4WcjAI7')
    
    print(f"OKTA_DOMAIN: {'✅ Set' if okta_domain else '❌ Not set'}")
    print(f"OKTA_CLIENT_ID: {'✅ Set' if client_id else '❌ Not set'}")
    print(f"OKTA_CLIENT_SECRET: {'✅ Set' if client_secret else '❌ Not set'}")
    print(f"OKTA_API_TOKEN: {'✅ Set' if api_token else '❌ Not set'}")
    
    if not api_token:
        print("\n⚠️  OKTA_API_TOKEN is not set!")
        print("To retrieve user information, you need to:")
        print("1. Go to your OKTA Admin Console")
        print("2. Navigate to Security > API > Tokens")
        print("3. Create a new API token")
        print("4. Set the OKTA_API_TOKEN environment variable")
        print("   Example: set OKTA_API_TOKEN=your_token_here")
        return False
    
    return True


def main():
    """
    Main function with usage examples
    """
    print("🚀 OKTA User Information Retrieval Tool")
    print("=" * 50)
    
    # Check connectivity first
    if not test_okta_api_connectivity():
        return
    
    # Get email from command line or prompt
    email = None
    if len(sys.argv) > 1:
        email = sys.argv[1] 
    else:
        email = input("\n📧 Enter user email address: ").strip()
    
    if not email:
        print("❌ No email address provided")
        return
    
    # Validate email format
    import re
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        print(f"❌ Invalid email format: {email}")
        return
    
    print(f"\n🔍 Looking up user: {email}")
    
    # Method 1: Get full user information
    print("\n1️⃣ Getting full user information...")
    user_info = get_okta_user_info(email)
    
    if user_info:
        display_user_info(user_info)
        
        # Method 2: Get just roles
        print("\n2️⃣ Getting just role names...")
        roles = get_user_roles_only(email)
        print(f"Roles: {roles}")
        
        # Method 3: Create authentication user object
        print("\n3️⃣ Creating authentication user object...")
        auth_user = create_auth_user_object(email)
        if auth_user:
            print(f"User object created successfully!")
            print(f"Can be used for authentication: user.name = {auth_user.name}")
    
    else:
        print(f"\n❌ User not found or error occurred")
        print("\nPossible issues:")
        print("- User doesn't exist in OKTA")
        print("- API token doesn't have sufficient permissions")
        print("- Network connectivity issues")
        print("- OKTA domain configuration incorrect")


def usage_examples():
    """
    Show usage examples for programmatic use
    """
    print("""
🔧 PROGRAMMATIC USAGE EXAMPLES:

1. Get full user information:
   ```python
   from security.authentication_provider.okta.auth_provider import Authentication_Provider
   
   user_info = Authentication_Provider.get_user_by_email("user@example.com")
   if user_info:
       print(f"User: {user_info['displayName']}")
       print(f"Roles: {[g['name'] for g in user_info['groups']]}")
   ```

2. Get just role names:
   ```python
   roles = Authentication_Provider.get_user_roles_by_email("user@example.com")
   print(f"User roles: {roles}")
   ```

3. Create authentication user object:
   ```python
   auth_user = Authentication_Provider.create_user_from_okta_email("user@example.com")
   if auth_user:
       # Use in authentication system
       session['user'] = auth_user
   ```

4. Integration with existing authentication:
   ```python
   # In your login endpoint
   email = request.json.get('email')
   user = Authentication_Provider.create_user_from_okta_email(email)
   if user:
       # Create JWT token or session
       token = create_access_token(identity=user.name)
       return {'token': token, 'user': user.name, 'roles': [r.role_name for r in user.UserRoleList]}
   ```

📋 Required Configuration:
- Set OKTA_API_TOKEN environment variable
- Ensure OKTA domain, client ID, and client secret are configured
- API token needs 'okta.users.read' and 'okta.groups.read' permissions
""")


if __name__ == "__main__":
    #if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
    #    usage_examples()
    #else:
    main()
