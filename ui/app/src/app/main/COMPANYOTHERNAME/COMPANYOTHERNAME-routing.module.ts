import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { COMPANYOTHERNAMEHomeComponent } from './home/COMPANYOTHERNAME-home.component';
import { COMPANYOTHERNAMENewComponent } from './new/COMPANYOTHERNAME-new.component';
import { COMPANYOTHERNAMEDetailComponent } from './detail/COMPANYOTHERNAME-detail.component';

const routes: Routes = [
  {path: '', component: COMPANYOTHERNAMEHomeComponent},
  { path: 'new', component: COMPANYOTHERNAMENewComponent },
  { path: ':ID', component: COMPANYOTHERNAMEDetailComponent,
    data: {
      oPermission: {
        permissionId: 'COMPANYOTHERNAME-detail-permissions'
      }
    }
  }
];

export const COMPANYOTHERNAME_MODULE_DECLARATIONS = [
    COMPANYOTHERNAMEHomeComponent,
    COMPANYOTHERNAMENewComponent,
    COMPANYOTHERNAMEDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class COMPANYOTHERNAMERoutingModule { }