/**
 * Authentication Service
 * Handles login, token management, and authentication status
 */

class AuthService {
    constructor() {
        this.baseApiUrl = 'http://172.30.3.133:5656';
        this.tokenKey = 'plant_app_bearer_token';
    }

    /**
     * Get current bearer token from localStorage
     */
    getToken() {
        return localStorage.getItem(this.tokenKey);
    }

    /**
     * Set bearer token in localStorage
     */
    setToken(token) {
        const formattedToken = token.startsWith('Bearer ') ? token : `Bearer ${token}`;
        localStorage.setItem(this.tokenKey, formattedToken);
        return formattedToken;
    }

    /**
     * Remove token from localStorage
     */
    clearToken() {
        localStorage.removeItem(this.tokenKey);
    }

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        const token = this.getToken();
        return !!token;
    }

    /**
     * Login with username and password
     */
    async login(username, password) {
        try {
            const response = await fetch(`${this.baseApiUrl}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            if (!response.ok) {
                if (response.status === 401 || response.status === 422) {
                    throw new Error('Invalid username or password');
                }
                throw new Error(`Login failed with status ${response.status}`);
            }

            const data = await response.json();

            // Assuming the API returns the token in a 'token' or 'access_token' field
            const token = data.token || data.access_token || data.bearer_token;

            if (!token) {
                throw new Error('No token received from server');
            }

            this.setToken(token);
            return { success: true, token };

        } catch (error) {
            console.error('Login error:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * Logout user
     */
    logout() {
        this.clearToken();
        // Optionally reload the page to reset the application state
        window.location.reload();
    }

    /**
     * Check if an error indicates authentication failure
     */
    isAuthError(status) {
        return status === 401 || status === 422 || status === 403;
    }
}

// Create global instance
window.authService = new AuthService();