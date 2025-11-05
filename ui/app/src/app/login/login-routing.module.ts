import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LoginComponent } from './login.component';
import { CognitoCallbackComponent } from './cognito-callback.component';

const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'callback', component: CognitoCallbackComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LoginRoutingModule { }
