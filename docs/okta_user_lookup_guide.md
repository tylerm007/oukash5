# OKTA User Information Retrieval Setup Guide

## Overview

The OKTA authentication provider now includes functions to retrieve user information including roles/groups by email address. This is useful for:

- User profile lookups
- Role-based access control
- User management operations
- Bulk user processing

## Required Setup

### 1. OKTA API Token

To retrieve user information, you need an OKTA API token with appropriate permissions.

#### Steps to Create API Token:

1. **Log in to OKTA Admin Console**
   - Go to your OKTA admin console (e.g., https://ou.okta.com/admin)
   - Use admin credentials

2. **Navigate to API Tokens**
   - Go to **Security** → **API** → **Tokens**

3. **Create Token**
   - Click **Create Token**
   - Give it a name like "API Logic Server User Lookup"
   - Copy the token value (you won't see it again!)

4. **Set Environment Variable**
   ```bash
   # Windows (Command Prompt)
   set OKTA_API_TOKEN=your_token_here
   
   # Windows (PowerShell)
   $env:OKTA_API_TOKEN="your_token_here"
   
   # Linux/Mac
   export OKTA_API_TOKEN=your_token_here
   ```

5. **Or Add to .env File**
   ```
   OKTA_API_TOKEN=your_token_here
   ```

### 2. Required Permissions

The API token needs these permissions:
- `okta.users.read` - To read user information
- `okta.groups.read` - To read group/role memberships

### 3. Alternative: Client Credentials

If you can't use an API token, you can configure client credentials with appropriate scopes:

1. **In OKTA Admin Console:**
   - Go to **Applications** → Your Application
   - Go to **General** tab → **Grant Types**
   - Enable **Client Credentials**

2. **Add Required Scopes:**
   - `okta.users.read`
   - `okta.groups.read`

## Usage Examples

### Basic User Lookup

```python
from security.authentication_provider.okta.auth_provider import Authentication_Provider

# Get full user information
user_info = Authentication_Provider.get_user_by_email("user@example.com")
if user_info:
    print(f"User: {user_info['displayName']}")
    print(f"Status: {user_info['status']}")
    print(f"Roles: {[g['name'] for g in user_info['groups']]}")
```

### Get Just Role Names

```python
# Get only role names
roles = Authentication_Provider.get_user_roles_by_email("user@example.com")
print(f"User roles: {roles}")
```

### Create Authentication User Object

```python
# Create user object for authentication system
auth_user = Authentication_Provider.create_user_from_okta_email("user@example.com")
if auth_user:
    # Use in session or JWT creation
    session['user'] = auth_user
    user_roles = [role.role_name for role in auth_user.UserRoleList]
```

### Role-Based Access Control

```python
def check_admin_access(email):
    roles = Authentication_Provider.get_user_roles_by_email(email)
    return "Administrators" in roles

# Usage
if check_admin_access("user@example.com"):
    # Grant admin access
    pass
```

## Testing Scripts

Use the provided testing scripts:

### 1. User Lookup Tool
```bash
python test/okta_user_lookup.py user@example.com
```

### 2. Integration Examples
```bash
python test/okta_integration_examples.py user@example.com
```

## Returned User Information

The `get_user_by_email()` function returns:

```python
{
    'id': 'okta_user_id',
    'email': 'user@example.com',
    'login': 'user@example.com',
    'firstName': 'John',
    'lastName': 'Doe', 
    'displayName': 'John Doe',
    'status': 'ACTIVE',
    'created': '2024-01-01T00:00:00.000Z',
    'lastLogin': '2024-08-07T10:00:00.000Z',
    'groups': [
        {
            'id': 'group_id',
            'name': 'Users',
            'description': 'Standard Users',
            'type': 'OKTA_GROUP'
        }
    ],
    'roles': [...],  # Same as groups
    'profile': {...},  # Full OKTA profile
    'raw_user_data': {...}  # Complete OKTA API response
}
```

## Error Handling

The functions handle common errors gracefully:

- **User not found**: Returns `None` or empty list
- **API token missing**: Logs error and returns `None`
- **Network errors**: Logs error and returns `None`
- **Permission errors**: Logs error details

## Troubleshooting

### Common Issues:

1. **"No OKTA API token available"**
   - Set `OKTA_API_TOKEN` environment variable
   - Or configure client credentials with appropriate scopes

2. **"Failed to search OKTA users: 403"**
   - API token lacks required permissions
   - Add `okta.users.read` and `okta.groups.read` permissions

3. **"User not found"**
   - Check email address spelling
   - Verify user exists in OKTA
   - Check if user is active

4. **Network timeouts**
   - Check OKTA domain configuration
   - Verify network connectivity
   - Check firewall rules

### Debug Mode:

Enable detailed logging:
```python
import logging
logging.getLogger('security.authentication_provider.okta.auth_provider').setLevel(logging.DEBUG)
```

## Integration with Authentication System

### In JWT Token Validation:
```python
def validate_and_enrich_token(token):
    # Validate token
    claims = Authentication_Provider.validate_okta_token(token)
    if claims:
        # Get full user info
        email = claims.get('email')
        user_info = Authentication_Provider.get_user_by_email(email)
        # Combine token claims with user info
        return {**claims, 'user_info': user_info}
```

### In User Session Creation:
```python
def create_user_session(email):
    user = Authentication_Provider.create_user_from_okta_email(email)
    if user:
        session.update({
            'user_id': user.name,
            'roles': [r.role_name for r in user.UserRoleList],
            'display_name': user.display_name
        })
```

This provides a complete solution for retrieving OKTA user information including roles by email address.
