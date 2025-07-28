import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ThirdPartyBillingCompanyHomeComponent } from './home/ThirdPartyBillingCompany-home.component';
import { ThirdPartyBillingCompanyNewComponent } from './new/ThirdPartyBillingCompany-new.component';
import { ThirdPartyBillingCompanyDetailComponent } from './detail/ThirdPartyBillingCompany-detail.component';

const routes: Routes = [
  {path: '', component: ThirdPartyBillingCompanyHomeComponent},
  { path: 'new', component: ThirdPartyBillingCompanyNewComponent },
  { path: ':ID', component: ThirdPartyBillingCompanyDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ThirdPartyBillingCompany-detail-permissions'
      }
    }
  }
];

export const THIRDPARTYBILLINGCOMPANY_MODULE_DECLARATIONS = [
    ThirdPartyBillingCompanyHomeComponent,
    ThirdPartyBillingCompanyNewComponent,
    ThirdPartyBillingCompanyDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ThirdPartyBillingCompanyRoutingModule { }