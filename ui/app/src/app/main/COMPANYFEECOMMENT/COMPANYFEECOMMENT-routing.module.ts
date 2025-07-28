import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { COMPANYFEECOMMENTHomeComponent } from './home/COMPANYFEECOMMENT-home.component';
import { COMPANYFEECOMMENTNewComponent } from './new/COMPANYFEECOMMENT-new.component';
import { COMPANYFEECOMMENTDetailComponent } from './detail/COMPANYFEECOMMENT-detail.component';

const routes: Routes = [
  {path: '', component: COMPANYFEECOMMENTHomeComponent},
  { path: 'new', component: COMPANYFEECOMMENTNewComponent },
  { path: ':ID', component: COMPANYFEECOMMENTDetailComponent,
    data: {
      oPermission: {
        permissionId: 'COMPANYFEECOMMENT-detail-permissions'
      }
    }
  }
];

export const COMPANYFEECOMMENT_MODULE_DECLARATIONS = [
    COMPANYFEECOMMENTHomeComponent,
    COMPANYFEECOMMENTNewComponent,
    COMPANYFEECOMMENTDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class COMPANYFEECOMMENTRoutingModule { }