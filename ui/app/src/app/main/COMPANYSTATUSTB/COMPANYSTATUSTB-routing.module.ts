import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { COMPANYSTATUSTBHomeComponent } from './home/COMPANYSTATUSTB-home.component';
import { COMPANYSTATUSTBNewComponent } from './new/COMPANYSTATUSTB-new.component';
import { COMPANYSTATUSTBDetailComponent } from './detail/COMPANYSTATUSTB-detail.component';

const routes: Routes = [
  {path: '', component: COMPANYSTATUSTBHomeComponent},
  { path: 'new', component: COMPANYSTATUSTBNewComponent },
  { path: ':ID', component: COMPANYSTATUSTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'COMPANYSTATUSTB-detail-permissions'
      }
    }
  }
];

export const COMPANYSTATUSTB_MODULE_DECLARATIONS = [
    COMPANYSTATUSTBHomeComponent,
    COMPANYSTATUSTBNewComponent,
    COMPANYSTATUSTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class COMPANYSTATUSTBRoutingModule { }