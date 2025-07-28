import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CompanycontactsTbHomeComponent } from './home/CompanycontactsTb-home.component';
import { CompanycontactsTbNewComponent } from './new/CompanycontactsTb-new.component';
import { CompanycontactsTbDetailComponent } from './detail/CompanycontactsTb-detail.component';

const routes: Routes = [
  {path: '', component: CompanycontactsTbHomeComponent},
  { path: 'new', component: CompanycontactsTbNewComponent },
  { path: ':ccID', component: CompanycontactsTbDetailComponent,
    data: {
      oPermission: {
        permissionId: 'CompanycontactsTb-detail-permissions'
      }
    }
  }
];

export const COMPANYCONTACTSTB_MODULE_DECLARATIONS = [
    CompanycontactsTbHomeComponent,
    CompanycontactsTbNewComponent,
    CompanycontactsTbDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CompanycontactsTbRoutingModule { }