import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AchStripePaymentDetailHomeComponent } from './home/AchStripePaymentDetail-home.component';
import { AchStripePaymentDetailNewComponent } from './new/AchStripePaymentDetail-new.component';
import { AchStripePaymentDetailDetailComponent } from './detail/AchStripePaymentDetail-detail.component';

const routes: Routes = [
  {path: '', component: AchStripePaymentDetailHomeComponent},
  { path: 'new', component: AchStripePaymentDetailNewComponent },
  { path: ':Id', component: AchStripePaymentDetailDetailComponent,
    data: {
      oPermission: {
        permissionId: 'AchStripePaymentDetail-detail-permissions'
      }
    }
  }
];

export const ACHSTRIPEPAYMENTDETAIL_MODULE_DECLARATIONS = [
    AchStripePaymentDetailHomeComponent,
    AchStripePaymentDetailNewComponent,
    AchStripePaymentDetailDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AchStripePaymentDetailRoutingModule { }