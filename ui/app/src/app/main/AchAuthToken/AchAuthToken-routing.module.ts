import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AchAuthTokenHomeComponent } from './home/AchAuthToken-home.component';
import { AchAuthTokenNewComponent } from './new/AchAuthToken-new.component';
import { AchAuthTokenDetailComponent } from './detail/AchAuthToken-detail.component';

const routes: Routes = [
  {path: '', component: AchAuthTokenHomeComponent},
  { path: 'new', component: AchAuthTokenNewComponent },
  { path: ':Id', component: AchAuthTokenDetailComponent,
    data: {
      oPermission: {
        permissionId: 'AchAuthToken-detail-permissions'
      }
    }
  }
];

export const ACHAUTHTOKEN_MODULE_DECLARATIONS = [
    AchAuthTokenHomeComponent,
    AchAuthTokenNewComponent,
    AchAuthTokenDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AchAuthTokenRoutingModule { }