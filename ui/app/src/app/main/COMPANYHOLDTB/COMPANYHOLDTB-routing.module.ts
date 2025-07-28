import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { COMPANYHOLDTBHomeComponent } from './home/COMPANYHOLDTB-home.component';
import { COMPANYHOLDTBNewComponent } from './new/COMPANYHOLDTB-new.component';
import { COMPANYHOLDTBDetailComponent } from './detail/COMPANYHOLDTB-detail.component';

const routes: Routes = [
  {path: '', component: COMPANYHOLDTBHomeComponent},
  { path: 'new', component: COMPANYHOLDTBNewComponent },
  { path: ':ID', component: COMPANYHOLDTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'COMPANYHOLDTB-detail-permissions'
      }
    }
  }
];

export const COMPANYHOLDTB_MODULE_DECLARATIONS = [
    COMPANYHOLDTBHomeComponent,
    COMPANYHOLDTBNewComponent,
    COMPANYHOLDTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class COMPANYHOLDTBRoutingModule { }