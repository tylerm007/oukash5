# Amazon Cognito Authentication Provider

This authentication provider integrates with Amazon Cognito User Pools to provide SSO authentication for your API Logic Server application.

## Features

- ✅ **Cognito User Pool Integration**: Authenticate users via Cognito Hosted UI
- ✅ **JWT Token Validation**: Validates Cognito JWT tokens using JWKS
- ✅ **SSO Support**: Single Sign-On with redirect flow
- ✅ **API Authentication**: Bearer token support for API endpoints
- ✅ **Role Management**: Maps Cognito groups to application roles
- ✅ **Session Management**: Maintains user sessions with token refresh

## Setup Instructions

### 1. Create Cognito User Pool

1. **Go to AWS Cognito Console**
   - Navigate to Amazon Cognito in AWS Console
   - Click "Create User Pool"

2. **Configure User Pool**
   ```
   Pool name: your-app-users
   Sign-in options: Email, Username (choose what you prefer)
   Password policy: Configure as needed
   MFA: Optional (recommended for production)
   ```

3. **Configure App Client**
   ```
   App client name: your-app-client
   Client secret: Generate a client secret ✓
   Allowed callback URLs: http://localhost:5656/auth/callback
   Allowed sign-out URLs: http://localhost:5656/
   OAuth 2.0 grants: Authorization code grant ✓
   OpenID Connect scopes: openid, profile, email ✓
   ```

4. **Configure Hosted UI Domain**
   ```
   Domain: your-domain (creates: your-domain.auth.region.amazoncognito.com)
   ```

### 2. Configure Environment Variables

Add these to your `.env` file or environment:

```bash
# Required Cognito Settings
COGNITO_REGION=us-east-1
COGNITO_USER_POOL_ID=us-east-1_XXXXXXXXX
COGNITO_CLIENT_ID=your-cognito-app-client-id
COGNITO_CLIENT_SECRET=your-cognito-app-client-secret
COGNITO_DOMAIN=https://your-domain.auth.us-east-1.amazoncognito.com
COGNITO_REDIRECT_URI=http://localhost:5656/auth/callback
```

### 3. Update Config Class

Add these properties to your `config/config.py` Args class:

```python
@property
def cognito_region(self) -> str:
    return os.getenv('COGNITO_REGION', 'us-east-1')

@property  
def cognito_user_pool_id(self) -> str:
    return os.getenv('COGNITO_USER_POOL_ID', '')

@property
def cognito_client_id(self) -> str:
    return os.getenv('COGNITO_CLIENT_ID', '')

@property
def cognito_client_secret(self) -> str:
    return os.getenv('COGNITO_CLIENT_SECRET', '')

@property
def cognito_domain(self) -> str:
    return os.getenv('COGNITO_DOMAIN', '')

@property
def cognito_redirect_uri(self) -> str:
    return os.getenv('COGNITO_REDIRECT_URI', 'http://localhost:5656/auth/callback')
```

### 4. Install Required Dependencies

```bash
pip install boto3 PyJWT cryptography
```

## Usage

### Web Browser Authentication

1. **Login**: Navigate to `http://localhost:5656/auth/login`
2. **Cognito Hosted UI**: Complete authentication in Cognito
3. **Callback**: Automatically redirected back with tokens
4. **Session**: User session established with access token

### API Authentication

1. **Get Token**: Use `/auth/token` endpoint after login
2. **Use Token**: Add to API requests as `Authorization: Bearer <token>`

### Postman Testing

1. **Get Auth URL**: `GET /auth/login-postman`
2. **Browser Login**: Open the returned `auth_url` in browser
3. **Copy Token**: Copy `access_token` from callback response
4. **Use in Postman**: Add to Authorization → Bearer Token

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/login` | GET | Redirects to Cognito Hosted UI |
| `/auth/login-postman` | GET | Returns auth URL for testing |
| `/auth/callback` | GET | Handles Cognito OAuth callback |
| `/auth/logout` | GET | Logs out and clears session |
| `/auth/token` | GET | Returns current session token |

## Token Validation

The provider validates Cognito JWT tokens by:

1. **JWKS Retrieval**: Downloads public keys from Cognito
2. **Signature Verification**: Validates token signature using RS256
3. **Claims Validation**: Checks issuer, audience, expiration
4. **User Creation**: Maps Cognito claims to application user

## Role Mapping

Cognito groups are automatically mapped to application roles:

```json
{
  "cognito:groups": ["admin", "user", "manager"],
  "roles": ["admin", "user", "manager"]
}
```

## Troubleshooting

### Common Issues

1. **Invalid redirect_uri**
   - Ensure callback URL matches exactly in Cognito app client settings
   - Check for trailing slashes

2. **Token validation fails**
   - Verify User Pool ID and region are correct
   - Check that client ID matches

3. **Groups not appearing**
   - Ensure user is assigned to Cognito groups
   - Check that groups are included in token claims

### Debug Endpoints

- `/auth/debug` - Shows current configuration
- Check server logs for detailed error messages

## Security Considerations

- **HTTPS in Production**: Always use HTTPS for production deployments
- **Client Secret**: Keep client secret secure and never expose in frontend
- **Token Expiration**: Cognito tokens typically expire in 1 hour
- **MFA**: Enable MFA for sensitive applications
- **Group Assignment**: Carefully manage Cognito group memberships

## Migration from OKTA

If migrating from OKTA:

1. **User Migration**: Export users from OKTA and import to Cognito
2. **Group Mapping**: Map OKTA groups to Cognito groups
3. **Configuration**: Update environment variables
4. **Testing**: Verify authentication flows work correctly

## Cost Considerations

- **Free Tier**: 50,000 monthly active users
- **Pricing**: $0.0055 per monthly active user beyond free tier
- **Additional Features**: MFA, advanced security features have additional costs

For more information, see [AWS Cognito Documentation](https://docs.aws.amazon.com/cognito/)