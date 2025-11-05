import { NgModule } from '@angular/core';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatExpansionModule } from '@angular/material/expansion';
import { FlexLayoutModule } from '@angular/flex-layout';

import { SharedModule } from '../shared/shared.module';
import { LoginRoutingModule } from './login-routing.module';
import { LoginComponent } from './login.component';
import { CognitoCallbackComponent } from './cognito-callback.component';
import { CognitoAuthService } from '../shared/cognito-auth.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    OntimizeWebModule,
    LoginRoutingModule,
    MatButtonModule,
    MatButtonToggleModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatExpansionModule,
    FlexLayoutModule
  ],
  declarations: [
    LoginComponent,
    CognitoCallbackComponent
  ],
  providers: [
    CognitoAuthService
  ]
})
export class LoginModule { }
