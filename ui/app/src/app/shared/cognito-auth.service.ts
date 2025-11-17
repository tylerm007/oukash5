import { Injectable, Injector } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, BehaviorSubject } from 'rxjs';
import { map, tap, switchMap } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { AuthService } from 'ontimize-web-ngx';

export interface CognitoAuthResponse {
  success: boolean;
  message: string;
  access_token: string;
  refresh_token?: string;
  token_type: string;
  expires_in: number;
  user_info: {
    user_id: string;
    email: string;
    roles: string[];
    cognito_sub?: string;
  };
}

export interface CognitoUser {
  user_id: string;
  email: string;
  roles: string[];
  cognito_sub?: string;
}

@Injectable({
  providedIn: 'root'
})
export class CognitoAuthService {
  private readonly API_BASE = environment.apiEndpoint.replace('/api', '');
  private readonly TOKEN_KEY = 'cognito_access_token';
  private readonly USER_KEY = 'cognito_user';
  
  private currentUserSubject: BehaviorSubject<CognitoUser | null>;
  public currentUser: Observable<CognitoUser | null>;
  
  constructor(
    private http: HttpClient,
    private router: Router,
    private injector: Injector
  ) {
    // Initialize current user from localStorage
    const storedUser = this.getStoredUser();
    this.currentUserSubject = new BehaviorSubject<CognitoUser | null>(storedUser);
    this.currentUser = this.currentUserSubject.asObservable();
  }

  /**
   * Check if user is currently authenticated (both Cognito and Ontimize)
   */
  isLoggedIn(): boolean {
    const token = this.getToken();
    const user = this.getStoredUser();
    
    if (!token || !user) {
      return false;
    }

    // Check if token is expired (basic check)
    try {
      const tokenPayload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Math.floor(Date.now() / 1000);
      
      if (tokenPayload.exp && tokenPayload.exp < currentTime) {
        console.log('Token expired, clearing session');
        this.clearSessionData();
        return false;
      }
      
      // Also check if Ontimize AuthService recognizes the user
      try {
        const authService = this.injector.get(AuthService);
        const ontimizeLoggedIn = authService.isLoggedIn();
        console.log('🔍 Ontimize login status:', ontimizeLoggedIn);
        
        // If Cognito says logged in but Ontimize doesn't, try to re-authenticate
        if (!ontimizeLoggedIn) {
          console.log('🔄 Re-authenticating with Ontimize...');
          this.authenticateWithOntimize(token, user);
        }
        
        return true; // Return true for Cognito auth, let Ontimize auth happen in background
      } catch (error) {
        console.log('Could not check Ontimize auth status:', error);
        return true; // Still return true for Cognito-only authentication
      }
      
    } catch (error) {
      console.error('Error parsing token:', error);
      this.clearSessionData();
      return false;
    }
  }

  /**
   * Get current authentication token
   */
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  /**
   * Get current user information
   */
  getCurrentUser(): CognitoUser | null {
    return this.currentUserSubject.value;
  }

  /**
   * Redirect to Cognito login page
   */
  redirectToLogin(returnUrl?: string): void {
    let loginUrl = `${this.API_BASE}/api/auth/login`;
    
    if (returnUrl) {
      const encodedReturnUrl = encodeURIComponent(returnUrl);
      loginUrl += `?return_url=${encodedReturnUrl}`;
      console.log('Cognito login with return URL:', returnUrl);
    }
    
    window.location.href = loginUrl;
  }

  /**
   * Get Cognito login URL for manual handling (useful for POSTMAN testing)
   */
  getCognitoLoginUrl(): Observable<any> {
    return this.http.get(`${this.API_BASE}/auth/login-postman`);
  }

  /**
   * Check session token status
   */
  checkSessionToken(): Observable<any> {
    return this.http.get(`${this.API_BASE}/auth/token`);
  }

  /**
   * Validate a JWT token
   */
  validateToken(token?: string): Observable<any> {
    const tokenToValidate = token || this.getToken();
    
    if (!tokenToValidate) {
      throw new Error('No token available for validation');
    }

    return this.http.post(`${this.API_BASE}/auth/validate-cognito`, {
      token: tokenToValidate
    });
  }

  /**
   * Handle successful authentication callback (called from callback page)
   */
  handleAuthCallback(authResponse: CognitoAuthResponse): void {
    if (authResponse.success && authResponse.access_token) {
      // Store token and user info for Authorization Bearer header usage
      localStorage.setItem(this.TOKEN_KEY, authResponse.access_token);
      localStorage.setItem(this.USER_KEY, JSON.stringify(authResponse.user_info));
      
      // Update current user subject
      this.currentUserSubject.next(authResponse.user_info);
      
      console.log('Cognito authentication successful - token stored for Authorization Bearer header:', authResponse.user_info);
      console.log('Access token stored:', authResponse.access_token.substring(0, 20) + '...');
      
      // Also authenticate with Ontimize AuthService for compatibility
      this.authenticateWithOntimize(authResponse.access_token, authResponse.user_info);
      
      // Also try force authentication as backup
      setTimeout(() => {
        this.forceOntimizeAuth(authResponse.user_info);
      }, 1000);
      
    } else {
      console.error('Authentication failed:', authResponse.message);
      this.clearSessionData();
    }
  }

  /**
   * Authenticate with Ontimize AuthService using Cognito token
   */
  private authenticateWithOntimize(token: string, userInfo: CognitoUser): void {
    console.log('🔗 Starting Ontimize AuthService integration...');
    console.log('📧 User email:', userInfo.email);
    console.log('🎫 Token type check:', typeof token, 'starts with eyJ:', token.startsWith('eyJ'));
    console.log('🎫 Token (first 30 chars):', token.substring(0, 30) + '...');
    
    // First, let's try our direct API call to verify the token works
    console.log('🧪 Testing direct API call first...');
    this.http.post(`${this.API_BASE}/api/users/login`, {
      user: userInfo.email,
      password: token
    }).subscribe({
      next: (response) => {
        console.log('✅ Direct API login successful:', response);
        
        // Now try with Ontimize AuthService
        this.tryOntimizeAuthService(token, userInfo);
      },
      error: (error) => {
        console.error('❌ Direct API login failed:', error);
        console.log('� API Response details:', error);
        
        // Still try Ontimize AuthService in case it uses a different endpoint
        this.tryOntimizeAuthService(token, userInfo);
      }
    });
  }

  private tryOntimizeAuthService(token: string, userInfo: CognitoUser): void {
    console.log('⏭️ Skipping Ontimize AuthService.login() to avoid error popup');
    console.log('📝 Reason: AuthService.login() expects traditional username/password, not Cognito tokens');
    console.log('🔄 Proceeding directly to session establishment...');
    
    // Skip the authService.login() call that triggers the "Login failed" popup
    // Instead, go directly to establishing the session
    this.establishOntimizeSession(token, userInfo);
  }

  /**
   * Establish Ontimize session using token-based endpoint
   */
  private establishOntimizeSession(token: string, userInfo: CognitoUser): void {
    console.log('🔧 Establishing Ontimize session with Cognito token...');
    console.log('🌐 Session API endpoint:', `${this.API_BASE}/auth/ontimize-session`);
    
    // Call a backend endpoint that accepts the Cognito token and returns Ontimize session
    this.http.post(`${this.API_BASE}/auth/ontimize-session`, {
      cognito_token: token,
      user_info: userInfo
    }).subscribe({
      next: (sessionResponse: any) => {
        console.log('✅ Ontimize session established successfully:', sessionResponse);
        
        // Store Ontimize session data if provided
        if (sessionResponse.sessionData) {
          try {
            // Store session data in multiple locations for compatibility
            localStorage.setItem('ontimize_session', JSON.stringify(sessionResponse.sessionData));
            localStorage.setItem('sessionData', JSON.stringify(sessionResponse.sessionData));
            
            // Also try to set in Ontimize's expected location
            const sessionId = sessionResponse.sessionData.sessionId;
            if (sessionId) {
              localStorage.setItem('session_id', sessionId);
              localStorage.setItem('user', sessionResponse.sessionData.user || userInfo.email);
            }
            
            console.log('💾 Stored Ontimize session data in multiple locations');
            console.log('🔑 Session ID:', sessionId);
            console.log('👤 User:', sessionResponse.sessionData.user);
            
            // Try to verify if Ontimize now recognizes the session
            setTimeout(() => {
              try {
                const authService = this.injector.get(AuthService);
                const isLoggedIn = authService.isLoggedIn();
                console.log('🔍 Post-session Ontimize login check:', isLoggedIn);
                
                if (isLoggedIn) {
                  console.log('🎉 Ontimize session fully established!');
                } else {
                  console.log('⚠️ Ontimize still not recognizing session - may need manual navigation');
                  // At this point, we might need to force navigation or show a message
                }
              } catch (error) {
                console.log('Unable to check Ontimize status:', error);
              }
            }, 200);
            
          } catch (error) {
            console.error('Error storing Ontimize session:', error);
          }
        } else {
          console.log('⚠️ No sessionData returned from server');
        }
      },
      error: (error) => {
        console.error('❌ Failed to establish Ontimize session:', error);
        console.log('🔍 Session establishment error details:', {
          status: error.status,
          statusText: error.statusText,
          url: error.url,
          message: error.message
        });
        console.log('⚠️ Continuing with Cognito-only authentication');
        
        // Even if session establishment fails, we still have Cognito auth
        // The user might be able to access some routes
        console.log('💡 Consider manually navigating to /main or refreshing the page');
      }
    });
  }

  /**
   * Navigate to main dashboard with authentication checks
   */
  navigateToMain(): void {
    console.log('🚀 Attempting to navigate to main dashboard...');
    console.log('🔍 Pre-navigation authentication check:');
    console.log('  - Is logged in:', this.isLoggedIn());
    console.log('  - Has token:', !!this.getToken());
    console.log('  - Has user:', !!this.getCurrentUser());
    console.log('  - Current URL:', window.location.href);
    
    // Ensure we have valid authentication before navigation
    if (!this.isLoggedIn() || !this.getToken()) {
      console.log('⚠️ Invalid authentication state - cannot navigate to main');
      this.router.navigate(['/login']);
      return;
    }
    
    console.log('✅ Authentication confirmed - proceeding to main');
    
    // Navigate with additional debugging
    this.router.navigate(['/main']).then(success => {
      if (success) {
        console.log('✅ Navigation to /main successful');
        console.log('🔍 Current route after navigation:', this.router.url);
      } else {
        console.log('❌ Navigation to /main failed - attempting alternative approach');
        console.log('🔄 Trying window.location redirect...');
        // If Angular routing fails, try direct navigation
        window.location.href = '/main';
      }
    }).catch(error => {
      console.log('❌ Navigation error:', error);
      console.log('🔄 Trying window.location redirect as fallback...');
      window.location.href = '/main';
    });
  }

  /**
   * Force navigation to main (for testing/debugging)
   */
  forceNavigateToMain(): void {
    console.log('🔧 Force navigating to main (bypassing checks)...');
    window.location.href = '/main';
  }

  /**
   * Test API call with Authorization Bearer header
   */
  testApiCall(): void {
    const token = this.getToken();
    console.log('🧪 Testing API call with Authorization Bearer header...');
    console.log('🎫 Token available:', !!token);
    
    if (!token) {
      console.log('❌ No token available for testing');
      return;
    }
    
    console.log('🎫 Token (first 30 chars):', token.substring(0, 30) + '...');
    
    // Test with a simple API endpoint
    const testUrl = `${this.API_BASE}/api/COMPANYTB`;
    console.log('🌐 Testing endpoint:', testUrl);
    
    this.makeAuthenticatedRequest(testUrl, { method: 'GET' }).subscribe({
      next: (response) => {
        console.log('✅ API test successful:', response);
        alert('API test successful! Check console for details.');
      },
      error: (error) => {
        console.log('❌ API test failed:', error);
        console.log('📊 Error details:', {
          status: error.status,
          statusText: error.statusText,
          message: error.message,
          headers: error.headers
        });
        alert(`API test failed (${error.status}): ${error.statusText}. Check console for details.`);
      }
    });
  }

  /**
   * Process callback response from server (for programmatic handling)
   */
  processAuthCallback(): Observable<CognitoAuthResponse> {
    // This would be called by a callback component that receives the auth response
    return this.checkSessionToken().pipe(
      map((response: any) => {
        console.log('Raw callback response:', response);
        
        // Handle the JSON response with access_token
        if (response.access_token) {
          const authResponse: CognitoAuthResponse = {
            success: true,
            message: 'Authentication successful',
            access_token: response.access_token,  // This will be used for Authorization Bearer header
            refresh_token: response.refresh_token,
            token_type: response.token_type || 'Bearer',
            expires_in: response.expires_in || 3600,
            user_info: {
              user_id: response.user_id || response.user_email,
              email: response.user_email || response.email,
              roles: response.user_roles || response.roles || [],
              cognito_sub: response.cognito_sub || response.sub
            }
          };
          
          // Store the access_token for Authorization Bearer header usage
          console.log('Storing access_token for Authorization Bearer header:', authResponse.access_token);
          this.handleAuthCallback(authResponse);
          return authResponse;
        } else {
          throw new Error('No access token in session response');
        }
      })
    );
  }

  /**
   * Logout user and redirect to Cognito logout
   */
  logout(): void {
    this.clearSessionData();
    // Redirect to Cognito logout endpoint
    window.location.href = `${this.API_BASE}/auth/logout`;
  }

  /**
   * Clear all session data
   */
  clearSessionData(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    this.currentUserSubject.next(null);
  }

  /**
   * Get user info from localStorage
   */
  private getStoredUser(): CognitoUser | null {
    try {
      const userStr = localStorage.getItem(this.USER_KEY);
      return userStr ? JSON.parse(userStr) : null;
    } catch (error) {
      console.error('Error parsing stored user:', error);
      return null;
    }
  }

  /**
   * Get authorization headers for HTTP requests (using Authorization Bearer format)
   */
  getAuthHeaders(): { [header: string]: string } {
    const token = this.getToken();
    return token ? { 'Authorization': `Bearer ${token}` } : {};
  }

  /**
   * Get Authorization Bearer header value
   */
  getAuthTokenHeader(): string | null {
    const token = this.getToken();
    return token ? `Bearer ${token}` : null;
  }

  /**
   * Debug method to get Cognito configuration info
   */
  getCognitoDebugInfo(): Observable<any> {
    return this.http.get(`${this.API_BASE}/auth/debug-cognito`);
  }

  /**
   * Make HTTP request with Authorization Bearer header
   */
  makeAuthenticatedRequest(url: string, options: any = {}): Observable<any> {
    const token = this.getToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    const headers = {
      ...options.headers,
      'Authorization': `Bearer ${token}`
    };

    console.log('🔑 Making authenticated request to:', url);
    console.log('🎫 Using Authorization Bearer header');

    return this.http.request(options.method || 'GET', url, {
      ...options,
      headers
    });
  }

  /**
   * Force Ontimize authentication bypass for testing
   */
  forceOntimizeAuth(userInfo: CognitoUser): void {
    console.log('🚀 Force-setting Ontimize authentication state...');
    
    try {
      // Set all possible session-related localStorage items that Ontimize might check
      const sessionData = {
        user: userInfo.email,
        username: userInfo.email,
        sessionId: `cognito_${userInfo.cognito_sub || Date.now()}`,
        roles: userInfo.roles || [],
        authenticated: true,
        auth_provider: 'cognito'
      };
      
      // Store in various formats that Ontimize might expect
      localStorage.setItem('user', userInfo.email);
      localStorage.setItem('username', userInfo.email);
      localStorage.setItem('sessionId', sessionData.sessionId);
      localStorage.setItem('session_id', sessionData.sessionId);
      localStorage.setItem('sessionData', JSON.stringify(sessionData));
      localStorage.setItem('ontimize_session', JSON.stringify(sessionData));
      localStorage.setItem('authenticated', 'true');
      
      console.log('💾 Force-stored Ontimize session data:', sessionData);
      
      // Try to get AuthService and check if it now recognizes auth
      try {
        const authService = this.injector.get(AuthService);
        console.log('🔍 Checking if Ontimize AuthService recognizes forced auth...');
        
        setTimeout(() => {
          const isLoggedIn = authService.isLoggedIn();
          console.log('🎯 Force auth result:', isLoggedIn);
          
          if (isLoggedIn) {
            console.log('🎉 Forced authentication successful!');
          } else {
            console.log('⚠️ Forced authentication not recognized by Ontimize');
            console.log('💡 User may need to refresh page or navigate manually');
          }
        }, 100);
        
      } catch (error) {
        console.log('Unable to check AuthService after force auth:', error);
      }
      
    } catch (error) {
      console.error('Error in force authentication:', error);
    }
  }
}