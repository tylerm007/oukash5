import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CognitoAuthService } from './cognito-auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private cognitoAuth: CognitoAuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Get the auth token from the service
    const authToken = this.cognitoAuth.getToken();
    
    if (authToken) {
      console.log('🔑 Adding Authorization Bearer token to request:', req.url);
      console.log('🎫 Token (first 20 chars):', authToken.substring(0, 20) + '...');
      
      // Clone the request and set the Authorization Bearer header
      const authReq = req.clone({
        headers: req.headers.set('Authorization', `Bearer ${authToken}`)
      });
      
      console.log('✅ Request headers with Authorization:', authReq.headers.keys());
      return next.handle(authReq);
    }
    
    console.log('❌ No auth token available for request:', req.url);
    return next.handle(req);
  }
}