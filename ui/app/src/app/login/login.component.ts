import { Component, Inject, Injector, OnInit, ViewEncapsulation } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService, LocalStorageService, NavigationService } from 'ontimize-web-ngx';
import { Observable } from 'rxjs';
import { CognitoAuthService } from '../shared/cognito-auth.service';

@Component({
  selector: 'login',
  styleUrls: ['./login.component.scss'],
  templateUrl: './login.component.html',
  encapsulation: ViewEncapsulation.None
})
export class LoginComponent implements OnInit {

  loginForm: FormGroup = new FormGroup({});
  userCtrl: FormControl = new FormControl('', Validators.required);
  pwdCtrl: FormControl = new FormControl('', Validators.required);
  sessionExpired = false;
  useCognito = true; // Toggle between Cognito and traditional login
  cognitoDebugInfo: any = null;
  loading = false;

  router: Router;

  constructor(
    private actRoute: ActivatedRoute,
    router: Router,
    @Inject(NavigationService) public navigation: NavigationService,
    @Inject(AuthService) private authService: AuthService,
    @Inject(LocalStorageService) private localStorageService,
    private cognitoAuth: CognitoAuthService,
    public injector: Injector
  ) {
    this.router = router;

    const qParamObs: Observable<any> = this.actRoute.queryParams;
    qParamObs.subscribe(params => {
      if (params) {
        const isDetail = params['session-expired'];
        if (isDetail === 'true') {
          this.sessionExpired = true;
        } else {
          this.sessionExpired = false;
        }
      }
    });

  }

  ngOnInit(): any {
    this.navigation.setVisible(false);

    this.loginForm.addControl('username', this.userCtrl);
    this.loginForm.addControl('password', this.pwdCtrl);

    // Check authentication based on the selected method
    if (this.useCognito) {
      if (this.cognitoAuth.isLoggedIn()) {
        this.router.navigate(['../'], { relativeTo: this.actRoute });
      } else {
        this.cognitoAuth.clearSessionData();
      }
      
      // Load Cognito debug info for troubleshooting
      this.loadCognitoDebugInfo();
    } else {
      // Traditional Ontimize authentication
      if (this.authService.isLoggedIn()) {
        this.router.navigate(['../'], { relativeTo: this.actRoute });
      } else {
        // Clear any existing session data for Ontimize
        this.authService.logout().subscribe({
          next: () => {
            console.log('Session cleared successfully');
          },
          error: (error) => {
            console.log('No existing session to clear or logout failed:', error);
          }
        });
      }
    }
  }

  login() {
    if (this.useCognito) {
      this.loginWithCognito();
    } else {
      this.loginWithOntimize();
    }
  }

  loginWithCognito() {
    this.loading = true;
    console.log('Redirecting to Cognito login...');
    
    // Construct return URL for post-authentication redirect
    const returnUrl = `${window.location.origin}/auth/callback`;
    console.log('Return URL for Cognito:', returnUrl);
    
    // Redirect to Cognito Hosted UI with return URL
    this.cognitoAuth.redirectToLogin(returnUrl);
  }

  loginWithOntimize() {
    const userName = this.loginForm.value.username;
    const password = this.loginForm.value.password;
    
    if (userName && userName.length > 0 && password && password.length > 0) {
      this.loading = true;
      const self = this;
      
      this.authService.login(userName, password)
        .subscribe(() => {
          self.loading = false;
          self.sessionExpired = false;
          self.router.navigate(['../'], { relativeTo: this.actRoute });
        }, (error) => {
          self.loading = false;
          self.handleError(error);
        });
    }
  }

  toggleAuthMethod() {
    this.useCognito = !this.useCognito;
    console.log('Switched to:', this.useCognito ? 'Cognito' : 'Traditional');
  }

  loadCognitoDebugInfo() {
    this.cognitoAuth.getCognitoDebugInfo().subscribe({
      next: (info) => {
        this.cognitoDebugInfo = info;
        console.log('Cognito debug info:', info);
      },
      error: (error) => {
        console.error('Failed to load Cognito debug info:', error);
      }
    });
  }

  testCognitoSession() {
    this.cognitoAuth.checkSessionToken().subscribe({
      next: (response) => {
        console.log('Session token check:', response);
        alert('Session check successful! Check console for details.');
      },
      error: (error) => {
        console.error('Session token check failed:', error);
        alert('Session check failed. Check console for details.');
      }
    });
  }

  // Debug method to test navigation after Cognito authentication
  testManualNavigation() {
    console.log('🧪 Testing manual navigation to /main...');
    console.log('🔍 Current authentication state:');
    console.log('  - Cognito logged in:', this.cognitoAuth.isLoggedIn());
    console.log('  - Cognito token exists:', !!this.cognitoAuth.getToken());
    console.log('  - Cognito user:', this.cognitoAuth.getCurrentUser());
    
    try {
      console.log('  - Ontimize logged in:', this.authService.isLoggedIn());
    } catch (error) {
      console.log('  - Ontimize auth check error:', error);
    }
    
    if (this.cognitoAuth.isLoggedIn()) {
      console.log('✅ Cognito authentication confirmed - attempting navigation');
      this.cognitoAuth.navigateToMain();
    } else {
      console.log('❌ No valid Cognito authentication found');
      alert('Please login with Cognito first');
    }
  }

  // Force navigation bypass (for troubleshooting)
  forceNavigateToMain() {
    console.log('🔧 Force navigating to main (bypass all checks)...');
    this.cognitoAuth.forceNavigateToMain();
  }

  // Test API call with Authorization Bearer header
  testApiCall() {
    console.log('🧪 Testing API call with Authorization Bearer header...');
    this.cognitoAuth.testApiCall();
  }

  handleError(error) {
    switch (error.status) {
      case 401:
        console.error('Email or password is wrong.');
        break;
      default: break;
    }
  }

}
