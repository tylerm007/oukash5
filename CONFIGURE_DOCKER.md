# Configure Backend to Use Cognito Authentication in Docker

## Problem
The backend supports multiple authentication methods (SQL, Keycloak, Okta, Cognito). If not configured, it defaults to **SQL authentication**, which is why you're getting 403 errors.

## Solution
Set the environment variable `SECURITY_PROVIDER=cognito` in the Docker container.

---

## Step 1: Check Current Configuration

SSH to 172.30.3.133 and run:

```bash
# Find the Docker container
sudo docker ps

# Check current environment variables (replace <container-name> with actual name)
sudo docker inspect <container-name> | grep -A 20 "Env"

# Look for SECURITY_PROVIDER in the output
```

## Step 2: Locate Docker Configuration

```bash
cd /home/tyler.band/oukash5

# Check for docker-compose.yml
ls -la docker-compose.yml

# Check for .env file
ls -la .env

# Check for Dockerfile
ls -la Dockerfile
```

## Step 3: Configure Authentication Method

### **Option A: If Using docker-compose.yml**

1. Edit the docker-compose.yml file:
```bash
cd /home/tyler.band/oukash5
nano docker-compose.yml  # or vi docker-compose.yml
```

2. Add or update the environment variables:
```yaml
version: '3'
services:
  api:
    # ... other settings ...
    environment:
      - SECURITY_ENABLED=true
      - SECURITY_PROVIDER=cognito
      - COGNITO_REGION=us-east-1
      - COGNITO_USER_POOL_ID=us-east-1_d38hiE2QM
      - COGNITO_CLIENT_ID=6o1m2bjh8bc8iihtufmhpq79gq
      # Add other settings as needed
```

3. Restart the container:
```bash
sudo docker-compose down
sudo docker-compose up -d
```

### **Option B: If Using .env File**

1. Create or edit .env file:
```bash
cd /home/tyler.band/oukash5
nano .env
```

2. Add these lines:
```bash
SECURITY_ENABLED=true
SECURITY_PROVIDER=cognito
COGNITO_REGION=us-east-1
COGNITO_USER_POOL_ID=us-east-1_d38hiE2QM
COGNITO_CLIENT_ID=6o1m2bjh8bc8iihtufmhpq79gq
```

3. Restart the container:
```bash
sudo docker-compose restart
```

### **Option C: If Running Docker Directly (No docker-compose)**

1. Stop the current container:
```bash
sudo docker ps  # Get the container ID/name
sudo docker stop <container-name>
sudo docker rm <container-name>
```

2. Run with environment variables:
```bash
sudo docker run -d \
  --name kashrus-api \
  -p 5656:5656 \
  -v /home/tyler.band/oukash5:/app \
  -e SECURITY_ENABLED=true \
  -e SECURITY_PROVIDER=cognito \
  -e COGNITO_REGION=us-east-1 \
  -e COGNITO_USER_POOL_ID=us-east-1_d38hiE2QM \
  -e COGNITO_CLIENT_ID=6o1m2bjh8bc8iihtufmhpq79gq \
  <image-name>
```

### **Option D: Quick Fix - Set Environment Variable in Running Container**

If you need a quick test without restarting:

```bash
# Find the container
sudo docker ps

# Get the container ID or name
CONTAINER_NAME=<your-container-name>

# This won't persist across restarts, but useful for testing:
sudo docker exec $CONTAINER_NAME sh -c "export SECURITY_PROVIDER=cognito"

# Better: Restart with the variable
sudo docker restart $CONTAINER_NAME
```

## Step 4: Verify the Configuration

```bash
# Check container logs
sudo docker logs <container-name> | grep -i "security"

# Look for a line like:
# "config.py - security enabled: True using SECURITY_PROVIDER: <class '...COGNITO_Authentication_Provider'>"

# Should show COGNITO_Authentication_Provider, not SQL_Authentication_Provider
```

## Step 5: Check Backend Logs

```bash
# Follow the logs in real-time
sudo docker logs -f <container-name>

# Look for:
# ✓ "using SECURITY_PROVIDER: COGNITO_Authentication_Provider"
# ✓ "Successfully validated Cognito token"
# ✗ "Invalid token" or "Authentication failed"
```

## Step 6: Test from Browser

1. Clear browser cache and sessionStorage:
   - Press F12
   - Go to Application tab
   - Clear Session Storage
   - Clear Cookies

2. Navigate to: `https://172.30.3.147`
3. Click "Sign In"
4. Login with Cognito
5. Click "Companies"
6. Should load successfully!

---

## Troubleshooting

### Still Getting 403 Errors?

**Check if Cognito is actually enabled:**
```bash
sudo docker logs <container-name> | tail -50 | grep -E "SECURITY_PROVIDER|authentication"
```

Should show:
```
config.py - security enabled: True using SECURITY_PROVIDER: <class 'security.authentication_provider.cognito.auth_provider.Authentication_Provider'>
```

If it shows `SQL_Authentication_Provider` instead, the environment variable didn't take effect.

### Environment Variable Not Taking Effect?

1. **Restart is required** - Environment variables are read at container startup
2. **Check spelling** - Must be exactly `SECURITY_PROVIDER=cognito` (lowercase)
3. **Check docker-compose.yml syntax** - YAML is indent-sensitive

### How to Check What Auth Method is Active?

```bash
# Make a test API call with your Cognito token
# Get token from browser (F12 → Console):
# sessionStorage.getItem('cognito_access_token')

TOKEN="<your-token-here>"

curl -H "Authorization: Bearer $TOKEN" http://172.30.3.133:5656/api/

# If 403 → Using wrong auth method (probably SQL)
# If 401/422 → Using Cognito but token validation failing
# If 200 → Working!
```

---

## Quick Reference: Authentication Methods

The backend supports 4 authentication methods:

| Method | Environment Variable | Use Case |
|--------|---------------------|----------|
| **SQL** | `SECURITY_PROVIDER=sql` or unset | Default - uses local database |
| **Keycloak** | `SECURITY_PROVIDER=keycloak` | Enterprise SSO |
| **Okta** | `SECURITY_PROVIDER=okta` | Okta SSO |
| **Cognito** | `SECURITY_PROVIDER=cognito` | AWS Cognito (what we want) |

**Default:** If `SECURITY_PROVIDER` is not set, it defaults to **SQL authentication**.

---

## Complete Example docker-compose.yml

```yaml
version: '3'
services:
  kashrus-api:
    build: .
    ports:
      - "5656:5656"
    volumes:
      - .:/app
    environment:
      # Security Configuration
      - SECURITY_ENABLED=true
      - SECURITY_PROVIDER=cognito

      # Cognito Configuration
      - COGNITO_REGION=us-east-1
      - COGNITO_USER_POOL_ID=us-east-1_d38hiE2QM
      - COGNITO_CLIENT_ID=6o1m2bjh8bc8iihtufmhpq79gq
      - COGNITO_CLIENT_SECRET=rev05ljd8067sbigkhlk153eluh78qgsh8dfptueehdalk42dmg

    restart: unless-stopped
```

---

## Next Steps After Configuration

1. Update the auth_provider.py file (as we did earlier)
2. Set `SECURITY_PROVIDER=cognito` in Docker
3. Restart the container
4. Test from browser
5. Should work!

## Files to Share with Server Admin

If someone else manages the Docker deployment, send them:
- This file (CONFIGURE_DOCKER.md)
- The modified auth_provider.py
- The environment variables they need to set
