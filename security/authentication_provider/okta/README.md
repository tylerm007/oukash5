# OKTA Authentication Provider

This document describes how to configure and use OKTA authentication with your API Logic Server application.

## Overview

The OKTA authentication provider integrates your API Logic Server with OKTA's identity platform, providing enterprise-grade authentication and authorization capabilities.

## Features

- **JWT Token Validation**: Validates OKTA-issued JWT tokens
- **User Role Mapping**: Maps OKTA groups to application roles
- **OpenID Connect Support**: Full OIDC integration with OKTA
- **Flexible Configuration**: Environment-based configuration
- **Seamless Integration**: Drop-in replacement for other auth providers

## Setup Instructions

### 1. OKTA Application Configuration

1. Log into your OKTA Admin Console
2. Navigate to **Applications** → **Create App Integration**
3. Choose **OIDC - OpenID Connect** and **Web Application**
4. Configure your application:
   - **App Name**: Your application name
   - **Grant Types**: Authorization Code, Implicit (Hybrid)
   - **Sign-in Redirect URIs**: `http://localhost:5656/auth/callback`
   - **Sign-out Redirect URIs**: `http://localhost:5656/logout`
   - **Trusted Origins**: `http://localhost:5656`

### 2. Environment Configuration

Create a `.env` file or set environment variables:

```bash
# OKTA Configuration
OKTA_DOMAIN=https://your-domain.okta.com
OKTA_CLIENT_ID=your-client-id
OKTA_CLIENT_SECRET=your-client-secret
OKTA_REDIRECT_URI=http://localhost:5656/auth/callback

# Security Configuration
SECURITY_ENABLED=true
SECURITY_PROVIDER=okta
```

### 3. Group/Role Configuration

In your OKTA application:

1. Navigate to **Directory** → **Groups**
2. Create groups that match your application roles:
   - `admin`
   - `user`
   - `manager` (or any custom roles)
3. Assign users to appropriate groups
4. In your OKTA app, go to **Sign On** → **OpenID Connect ID Token**
5. Add a claim for groups:
   - **Name**: `groups`
   - **Include in token type**: ID Token, Always
   - **Value type**: Groups
   - **Filter**: Matches regex `.*`

## Code Integration

### Basic Usage

```python
from security.authentication_provider.okta.auth_provider import Authentication_Provider

# The auth provider is automatically configured when SECURITY_PROVIDER=okta
# JWT tokens from OKTA will be automatically validated

# To manually validate a token:
claims = Authentication_Provider.validate_okta_token(jwt_token)
if claims:
    user = Authentication_Provider.get_user_from_jwt(claims)
    print(f"User: {user.name}, Roles: {[r.role_name for r in user.UserRoleList]}")
```

### JWT Token Structure

Expected JWT token claims:

```json
{
  "sub": "user-id",
  "email": "user@example.com",
  "preferred_username": "username",
  "given_name": "First",
  "family_name": "Last",
  "groups": ["admin", "user"],
  "iss": "https://your-domain.okta.com/oauth2/default",
  "aud": "your-client-id"
}
```

## API Usage

### Protected Endpoints

With OKTA authentication enabled, all API endpoints require valid JWT tokens:

```bash
# Request with Authorization header
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \\
     http://localhost:5656/api/YourEndpoint
```

### Login Flow

1. **Frontend redirects to OKTA**:
   ```
   https://your-domain.okta.com/oauth2/default/v1/authorize?
     client_id=your-client-id&
     response_type=code&
     scope=openid profile email&
     redirect_uri=http://localhost:5656/auth/callback&
     state=random-state
   ```

2. **User authenticates with OKTA**

3. **OKTA redirects back with authorization code**

4. **Exchange code for tokens**:
   ```bash
   curl -X POST https://your-domain.okta.com/oauth2/default/v1/token \\
        -H "Content-Type: application/x-www-form-urlencoded" \\
        -d "grant_type=authorization_code&code=AUTH_CODE&redirect_uri=REDIRECT_URI&client_id=CLIENT_ID&client_secret=CLIENT_SECRET"
   ```

## Testing

Run the test script to verify your configuration:

```bash
python test/test_okta_auth.py
```

## Troubleshooting

### Common Issues

1. **"Could not retrieve JWKS"**
   - Check OKTA_DOMAIN is correct
   - Ensure network connectivity to OKTA
   - Verify OKTA application is active

2. **"Token validation failed"**
   - Check token expiration
   - Verify audience (aud) claim matches OKTA_CLIENT_ID
   - Ensure issuer (iss) claim matches your OKTA domain

3. **"No groups in token"**
   - Verify groups claim is configured in OKTA app
   - Check user is assigned to groups
   - Ensure groups filter includes all needed groups

### Debug Mode

Enable debug logging to see detailed auth flow:

```python
import logging
logging.getLogger('security.authentication_provider.okta').setLevel(logging.DEBUG)
```

## Security Considerations

1. **HTTPS in Production**: Always use HTTPS in production environments
2. **Secret Management**: Store OKTA_CLIENT_SECRET securely
3. **Token Expiration**: Implement token refresh logic in your frontend
4. **CORS Configuration**: Configure CORS properly for your frontend domain
5. **Group Validation**: Validate user groups/roles for each protected resource

## Integration Examples

### React Frontend

```javascript
// Login redirect
const loginUrl = `https://your-domain.okta.com/oauth2/default/v1/authorize?` +
  `client_id=your-client-id&` +
  `response_type=token id_token&` +
  `scope=openid profile email&` +
  `redirect_uri=${encodeURIComponent(window.location.origin)}/callback&` +
  `state=random-state&` +
  `nonce=random-nonce`;

window.location.href = loginUrl;

// API calls with token
const response = await fetch('/api/endpoint', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

### Angular Frontend

```typescript
// Use @okta/okta-angular for seamless integration
import { OktaAuthService } from '@okta/okta-angular';

// API service
async callAPI(endpoint: string) {
  const accessToken = await this.oktaAuth.getAccessToken();
  return this.http.get(endpoint, {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  });
}
```

## Advanced Configuration

### Custom Claims Mapping

Modify `get_user_from_jwt()` in `auth_provider.py` to handle custom claims:

```python
@staticmethod
def get_user_from_jwt(jwt_data: dict) -> object:
    rtn_user = DotMapX()
    
    # Map custom OKTA attributes
    rtn_user.department = jwt_data.get("department")
    rtn_user.employee_id = jwt_data.get("employee_id")
    
    # Custom role mapping logic
    groups = jwt_data.get("groups", [])
    if "IT-Admin" in groups:
        groups.append("admin")
    
    # ... rest of implementation
```

### Multiple OKTA Orgs

To support multiple OKTA organizations, modify the configuration to accept dynamic domains.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review OKTA's developer documentation
3. Check API Logic Server documentation
4. Enable debug logging for detailed error information
