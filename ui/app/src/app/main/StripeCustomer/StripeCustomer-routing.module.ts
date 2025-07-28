import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StripeCustomerHomeComponent } from './home/StripeCustomer-home.component';
import { StripeCustomerNewComponent } from './new/StripeCustomer-new.component';
import { StripeCustomerDetailComponent } from './detail/StripeCustomer-detail.component';

const routes: Routes = [
  {path: '', component: StripeCustomerHomeComponent},
  { path: 'new', component: StripeCustomerNewComponent },
  { path: ':Id', component: StripeCustomerDetailComponent,
    data: {
      oPermission: {
        permissionId: 'StripeCustomer-detail-permissions'
      }
    }
  }
];

export const STRIPECUSTOMER_MODULE_DECLARATIONS = [
    StripeCustomerHomeComponent,
    StripeCustomerNewComponent,
    StripeCustomerDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StripeCustomerRoutingModule { }