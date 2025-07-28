import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BillingHomeComponent } from './home/Billing-home.component';
import { BillingNewComponent } from './new/Billing-new.component';
import { BillingDetailComponent } from './detail/Billing-detail.component';

const routes: Routes = [
  {path: '', component: BillingHomeComponent},
  { path: 'new', component: BillingNewComponent },
  { path: ':Id', component: BillingDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Billing-detail-permissions'
      }
    }
  }
];

export const BILLING_MODULE_DECLARATIONS = [
    BillingHomeComponent,
    BillingNewComponent,
    BillingDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class BillingRoutingModule { }