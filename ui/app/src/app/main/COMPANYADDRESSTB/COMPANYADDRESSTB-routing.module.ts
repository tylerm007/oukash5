import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { COMPANYADDRESSTBHomeComponent } from './home/COMPANYADDRESSTB-home.component';
import { COMPANYADDRESSTBNewComponent } from './new/COMPANYADDRESSTB-new.component';
import { COMPANYADDRESSTBDetailComponent } from './detail/COMPANYADDRESSTB-detail.component';

const routes: Routes = [
  {path: '', component: COMPANYADDRESSTBHomeComponent},
  { path: 'new', component: COMPANYADDRESSTBNewComponent },
  { path: ':ID', component: COMPANYADDRESSTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'COMPANYADDRESSTB-detail-permissions'
      }
    }
  }
];

export const COMPANYADDRESSTB_MODULE_DECLARATIONS = [
    COMPANYADDRESSTBHomeComponent,
    COMPANYADDRESSTBNewComponent,
    COMPANYADDRESSTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class COMPANYADDRESSTBRoutingModule { }