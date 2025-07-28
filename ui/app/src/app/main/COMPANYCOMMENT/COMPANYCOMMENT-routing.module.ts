import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { COMPANYCOMMENTHomeComponent } from './home/COMPANYCOMMENT-home.component';
import { COMPANYCOMMENTNewComponent } from './new/COMPANYCOMMENT-new.component';
import { COMPANYCOMMENTDetailComponent } from './detail/COMPANYCOMMENT-detail.component';

const routes: Routes = [
  {path: '', component: COMPANYCOMMENTHomeComponent},
  { path: 'new', component: COMPANYCOMMENTNewComponent },
  { path: ':ID', component: COMPANYCOMMENTDetailComponent,
    data: {
      oPermission: {
        permissionId: 'COMPANYCOMMENT-detail-permissions'
      }
    }
  }
];

export const COMPANYCOMMENT_MODULE_DECLARATIONS = [
    COMPANYCOMMENTHomeComponent,
    COMPANYCOMMENTNewComponent,
    COMPANYCOMMENTDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class COMPANYCOMMENTRoutingModule { }