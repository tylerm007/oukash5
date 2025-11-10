import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { CognitoAuthService } from '../shared/cognito-auth.service';
import { AuthService } from 'ontimize-web-ngx';

@Injectable({
  providedIn: 'root'
})
export class CognitoAuthGuardService implements CanActivate {

  constructor(
    private cognitoAuth: CognitoAuthService,
    private ontimizeAuth: AuthService,
    private router: Router
  ) {}

  canActivate(): Observable<boolean> | Promise<boolean> | boolean {
    console.log('🛡️ CognitoAuthGuard: Checking authentication for route access...');
    console.log('📍 Current URL:', window.location.href);
    
    // First check if user is authenticated with Cognito
    const cognitoAuthenticated = this.cognitoAuth.isLoggedIn();
    const cognitoToken = this.cognitoAuth.getToken();
    const cognitoUser = this.cognitoAuth.getCurrentUser();
    
    console.log('🔍 Cognito authentication status:', cognitoAuthenticated);
    console.log('🎫 Has Cognito token:', !!cognitoToken);
    console.log('👤 Has Cognito user:', !!cognitoUser);
    
    if (cognitoAuthenticated && cognitoToken) {
      console.log('✅ Cognito authentication confirmed - allowing access to protected route');
      console.log('👤 Authenticated user:', cognitoUser?.email || 'unknown');
      return true;
    }
    
    // Also check Ontimize authentication as fallback
    try {
      const ontimizeAuthenticated = this.ontimizeAuth.isLoggedIn();
      console.log('🔍 Ontimize authentication status:', ontimizeAuthenticated);
      
      if (ontimizeAuthenticated) {
        console.log('✅ Ontimize authentication confirmed - allowing access');
        return true;
      }
    } catch (error) {
      console.log('⚠️ Could not check Ontimize authentication:', error);
    }
    
    // If neither authentication method confirms user is logged in, redirect to login
    console.log('❌ No valid authentication found - redirecting to login');
    console.log('🔄 Redirecting from:', window.location.pathname);
    this.router.navigate(['/login']);
    return false;
  }
}