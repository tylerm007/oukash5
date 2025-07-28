import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AchPlaidLambdaResponseHomeComponent } from './home/AchPlaidLambdaResponse-home.component';
import { AchPlaidLambdaResponseNewComponent } from './new/AchPlaidLambdaResponse-new.component';
import { AchPlaidLambdaResponseDetailComponent } from './detail/AchPlaidLambdaResponse-detail.component';

const routes: Routes = [
  {path: '', component: AchPlaidLambdaResponseHomeComponent},
  { path: 'new', component: AchPlaidLambdaResponseNewComponent },
  { path: ':Id', component: AchPlaidLambdaResponseDetailComponent,
    data: {
      oPermission: {
        permissionId: 'AchPlaidLambdaResponse-detail-permissions'
      }
    }
  }
];

export const ACHPLAIDLAMBDARESPONSE_MODULE_DECLARATIONS = [
    AchPlaidLambdaResponseHomeComponent,
    AchPlaidLambdaResponseNewComponent,
    AchPlaidLambdaResponseDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AchPlaidLambdaResponseRoutingModule { }