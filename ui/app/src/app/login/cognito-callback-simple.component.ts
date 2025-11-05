import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CognitoAuthService, CognitoAuthResponse } from '../shared/cognito-auth.service';

@Component({
  selector: 'app-cognito-callback',
  template: `
    <div class="callback-container" style="display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column;">
      <div *ngIf="loading" class="loading">
        <mat-progress-spinner diameter="50" mode="indeterminate"></mat-progress-spinner>
        <p style="margin-top: 20px;">Processing authentication...</p>
      </div>
      
      <div *ngIf="error" class="error" style="text-align: center; color: red;">
        <mat-icon style="font-size: 48px; color: red;">error</mat-icon>
        <h3>Authentication Error</h3>
        <p>{{ errorMessage }}</p>
        <button mat-raised-button color="primary" (click)="retryLogin()">
          Try Again
        </button>
      </div>
      
      <div *ngIf="success" class="success" style="text-align: center; color: green;">
        <mat-icon style="font-size: 48px; color: green;">check_circle</mat-icon>
        <h3>Authentication Successful</h3>
        <p>Redirecting to application...</p>
      </div>
    </div>
  `,
  styles: [`
    .callback-container {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    
    .loading, .error, .success {
      background: rgba(255, 255, 255, 0.9);
      color: #333;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      min-width: 300px;
    }
  `]
})
export class CognitoCallbackComponent implements OnInit {
  loading = true;
  error = false;
  success = false;
  errorMessage = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private cognitoAuth: CognitoAuthService
  ) {}

  ngOnInit(): void {
    // Get query parameters from the callback URL
    this.route.queryParams.subscribe(params => {
      console.log('Callback received with params:', params);
      
      // Check if there's an error in the callback
      if (params['error']) {
        this.handleError(params['error'], params['error_description']);
        return;
      }
      
      // Check if we have authentication success with access token (from backend redirect)
      if (params['success'] === 'true' && params['access_token']) {
        console.log('🎉 Authentication successful - processing token from URL params');
        this.handleAuthenticationSuccess(params);
        return;
      }
      
      // Check if we have an authorization code (direct Cognito callback)
      if (params['code']) {
        console.log('📝 Authorization code received - processing...');
        this.handleAuthCode(params['code'], params['state']);
      } else {
        // Try to process existing session (user might have already been authenticated)
        this.processExistingSession();
      }
    });
  }

  private handleAuthenticationSuccess(params: any): void {
    console.log('🔑 Processing authentication success from backend redirect');
    
    // Extract authentication data from URL parameters
    const authData = {
      success: true,
      message: 'Authentication successful',
      access_token: params['access_token'],
      token_type: params['token_type'] || 'Bearer',
      expires_in: parseInt(params['expires_in']) || 86400,
      user_info: {
        user_id: params['user_id'],
        email: params['email'],
        roles: [], // Will be populated from token validation
        cognito_sub: params['cognito_sub']
      }
    };
    
    console.log('🎯 Auth data extracted from URL:', authData);
    
    // Store the token using the CognitoAuthService
    this.cognitoAuth.handleAuthCallback(authData);
    console.log('✅ Cognito token stored successfully');
    
    // Show success and redirect
    this.loading = false;
    this.success = true;
    
    // Clear URL parameters for security
    window.history.replaceState({}, document.title, window.location.pathname);
    
    // Try different navigation approaches
    setTimeout(() => {
      this.attemptNavigation();
    }, 2000);
  }

  private handleAuthCode(code: string, state: string): void {
    console.log('Processing authorization code...');
    
    // The backend should handle the code exchange automatically
    // We just need to check if the session now has valid tokens
    setTimeout(() => {
      this.processExistingSession();
    }, 2000); // Give the backend time to process the callback
  }

  private processExistingSession(): void {
    // First check if we already have a valid session token
    if (this.cognitoAuth.isLoggedIn()) {
      console.log('User already authenticated, redirecting...');
      this.loading = false;
      this.success = true;
      setTimeout(() => {
        this.attemptNavigation();
      }, 1000);
      return;
    }

    // Process the authentication callback
    this.cognitoAuth.processAuthCallback().subscribe({
      next: (response) => {
        console.log('Authentication callback processed successfully:', response);
        
        // Ensure the token is stored and X-Auth-Token header will be set
        if (response.access_token) {
          console.log('Access token received and stored for X-Auth-Token header');
        }
        
        this.loading = false;
        this.success = true;
        
        // Wait a moment before redirecting to show success message
        setTimeout(() => {
          this.attemptNavigation();
        }, 2000);
      },
      error: (error) => {
        console.error('Authentication callback processing failed:', error);
        this.handleError('session_error', 'Failed to process authentication session');
      }
    });
  }

  private attemptNavigation(): void {
    console.log('🎯 Starting navigation attempts...');
    console.log('Current authentication state:', this.cognitoAuth.isLoggedIn());
    console.log('Current token:', this.cognitoAuth.getToken()?.substring(0, 20) + '...');
    
    // Strategy 1: Try direct navigation to /main
    this.router.navigate(['/main']).then(
      (success) => {
        if (success) {
          console.log('✅ Strategy 1 - Direct /main navigation successful');
        } else {
          console.log('❌ Strategy 1 - Navigation returned false, trying Strategy 2...');
          this.tryAlternativeNavigation();
        }
      },
      (error) => {
        console.log('❌ Strategy 1 failed with error, trying Strategy 2...', error);
        this.tryAlternativeNavigation();
      }
    );
  }

  private tryAlternativeNavigation(): void {
    // Strategy 2: Try navigating to root and let it redirect
    this.router.navigate(['/']).then(
      (success) => {
        if (success) {
          console.log('✅ Strategy 2 - Root navigation successful');
        } else {
          console.log('❌ Strategy 2 failed, trying Strategy 3...');
          this.forcePageNavigation();
        }
      },
      (error) => {
        console.log('❌ Strategy 2 failed, trying Strategy 3...', error);
        this.forcePageNavigation();
      }
    );
  }

  private forcePageNavigation(): void {
    // Strategy 3: Force page navigation using window.location
    console.log('🔄 Strategy 3 - Using window.location to force navigation');
    
    // Try to go to the main page directly
    setTimeout(() => {
      console.log('Forcing navigation to main application...');
      window.location.href = '/main';
    }, 1000);
  }

  private handleError(error: string, description?: string): void {
    this.loading = false;
    this.error = true;
    
    switch (error) {
      case 'access_denied':
        this.errorMessage = 'Access denied. You cancelled the login or don\'t have permission.';
        break;
      case 'invalid_request':
        this.errorMessage = 'Invalid request. Please try logging in again.';
        break;
      case 'unauthorized_client':
        this.errorMessage = 'Unauthorized client. Please contact support.';
        break;
      case 'unsupported_response_type':
        this.errorMessage = 'Unsupported response type. Please contact support.';
        break;
      case 'invalid_scope':
        this.errorMessage = 'Invalid scope. Please contact support.';
        break;
      case 'server_error':
        this.errorMessage = 'Server error occurred. Please try again later.';
        break;
      case 'temporarily_unavailable':
        this.errorMessage = 'Service temporarily unavailable. Please try again later.';
        break;
      default:
        this.errorMessage = description || `Authentication error: ${error}`;
    }
  }

  retryLogin(): void {
    this.cognitoAuth.redirectToLogin();
  }
}