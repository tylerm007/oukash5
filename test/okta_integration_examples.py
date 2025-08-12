#!/usr/bin/env python3
"""
OKTA Integration Example
Shows how to combine OKTA token validation with user information retrieval
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def example_jwt_token_to_user_info(jwt_token: str):
    """
    Example: From JWT token to full user information
    
    Args:
        jwt_token: OKTA JWT token
    """
    from security.authentication_provider.okta.auth_provider import Authentication_Provider
    
    print("🔍 Validating JWT token and retrieving user info...")
    
    # Step 1: Validate the token
    claims = Authentication_Provider.validate_okta_token(jwt_token)
    
    if not claims:
        print("❌ Invalid JWT token")
        return None
    
    print(f"✅ Token validated for user: {claims.get('sub')}")
    
    # Step 2: Get email from token claims
    email = claims.get('email') or claims.get('preferred_username')
    
    if not email:
        print("❌ No email found in token claims")
        return None
    
    # Step 3: Get full user information from OKTA
    user_info = Authentication_Provider.get_user_by_email(email)
    
    if user_info:
        print(f"✅ Retrieved full user info for: {user_info['displayName']}")
        print(f"   Roles: {[g['name'] for g in user_info.get('groups', [])]}")
        return user_info
    else:
        print(f"❌ Could not retrieve user info for email: {email}")
        return None


def example_email_to_auth_session(email: str):
    """
    Example: Create authentication session from email
    
    Args:
        email: User's email address
    """
    from security.authentication_provider.okta.auth_provider import Authentication_Provider
    from flask_jwt_extended import create_access_token
    
    print(f"🔍 Creating auth session for: {email}")
    
    # Get user object suitable for authentication
    user = Authentication_Provider.create_user_from_okta_email(email)
    
    if not user:
        print(f"❌ User not found: {email}")
        return None
    
    # Create session data
    session_data = {
        'user_id': user.name,
        'email': user.email,
        'display_name': user.display_name,
        'roles': [role.role_name for role in user.UserRoleList],
        'okta_user_id': user.okta_user_id
    }
    
    print(f"✅ Session created for: {user.display_name}")
    print(f"   User ID: {user.name}")
    print(f"   Roles: {session_data['roles']}")
    
    # You could also create a JWT token:
    # token = create_access_token(identity=user.name)
    
    return session_data


def example_role_based_access_control(email: str, required_role: str):
    """
    Example: Role-based access control
    
    Args:
        email: User's email
        required_role: Role required for access
    """
    from security.authentication_provider.okta.auth_provider import Authentication_Provider
    
    print(f"🔐 Checking if {email} has role: {required_role}")
    
    # Get user roles
    user_roles = Authentication_Provider.get_user_roles_by_email(email)
    
    if required_role in user_roles:
        print(f"✅ Access granted - user has required role")
        return True
    else:
        print(f"❌ Access denied - user roles: {user_roles}")
        return False


def example_bulk_user_processing(email_list: list):
    """
    Example: Process multiple users
    
    Args:
        email_list: List of email addresses
    """
    from security.authentication_provider.okta.auth_provider import Authentication_Provider
    
    print(f"📊 Processing {len(email_list)} users...")
    
    results = []
    
    for email in email_list:
        user_info = Authentication_Provider.get_user_by_email(email)
        
        if user_info:
            result = {
                'email': email,
                'status': 'found',
                'name': user_info['displayName'],
                'roles': [g['name'] for g in user_info.get('groups', [])],
                'okta_status': user_info['status']
            }
        else:
            result = {
                'email': email,
                'status': 'not_found',
                'name': None,
                'roles': [],
                'okta_status': None
            }
        
        results.append(result)
        print(f"   {email}: {result['status']}")
    
    return results


def main():
    """
    Main function with examples
    """
    print("🚀 OKTA Integration Examples")
    print("=" * 40)
    
    # Example 1: Email to user info
    print("\n1️⃣ Example: Get user info by email")
    example_email = "your.user@example.com"  # Replace with actual email
    
    if len(sys.argv) > 1:
        example_email = sys.argv[1]
    else:
        example_email = input("Enter email address for examples: ").strip()
    
    if example_email:
        # Get full user info
        from security.authentication_provider.okta.auth_provider import Authentication_Provider
        user_info = Authentication_Provider.get_user_by_email(example_email)
        
        if user_info:
            print(f"✅ User found: {user_info['displayName']}")
            print(f"   Status: {user_info['status']}")
            print(f"   Roles: {[g['name'] for g in user_info.get('groups', [])]}")
            
            # Example 2: Create auth session
            print(f"\n2️⃣ Example: Create authentication session")
            session_data = example_email_to_auth_session(example_email)
            
            # Example 3: Role-based access control
            print(f"\n3️⃣ Example: Role-based access control")
            example_role_based_access_control(example_email, "Administrators")
            example_role_based_access_control(example_email, "Users")
            
        else:
            print(f"❌ User not found: {example_email}")
    
    # Example 4: Bulk processing
    print(f"\n4️⃣ Example: Bulk user processing")
    example_emails = [
        example_email,
        "nonexistent@example.com"
    ]
    
    results = example_bulk_user_processing(example_emails)
    
    print(f"\n📋 Bulk processing results:")
    for result in results:
        status_icon = "✅" if result['status'] == 'found' else "❌"
        print(f"   {status_icon} {result['email']}: {result['status']}")


if __name__ == "__main__":
    main()
