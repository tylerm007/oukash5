import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFCompanyHomeComponent } from './home/WFCompany-home.component';
import { WFCompanyNewComponent } from './new/WFCompany-new.component';
import { WFCompanyDetailComponent } from './detail/WFCompany-detail.component';

const routes: Routes = [
  {path: '', component: WFCompanyHomeComponent},
  { path: 'new', component: WFCompanyNewComponent },
  { path: ':CompanyID', component: WFCompanyDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFCompany-detail-permissions'
      }
    }
  }
];

export const WFCOMPANY_MODULE_DECLARATIONS = [
    WFCompanyHomeComponent,
    WFCompanyNewComponent,
    WFCompanyDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFCompanyRoutingModule { }