import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AchStripePaymentHomeComponent } from './home/AchStripePayment-home.component';
import { AchStripePaymentNewComponent } from './new/AchStripePayment-new.component';
import { AchStripePaymentDetailComponent } from './detail/AchStripePayment-detail.component';

const routes: Routes = [
  {path: '', component: AchStripePaymentHomeComponent},
  { path: 'new', component: AchStripePaymentNewComponent },
  { path: ':Id', component: AchStripePaymentDetailComponent,
    data: {
      oPermission: {
        permissionId: 'AchStripePayment-detail-permissions'
      }
    }
  },{
    path: ':AchStripePaymentId/AchStripePaymentDetail', loadChildren: () => import('../AchStripePaymentDetail/AchStripePaymentDetail.module').then(m => m.AchStripePaymentDetailModule),
    data: {
        oPermission: {
            permissionId: 'AchStripePaymentDetail-detail-permissions'
        }
    }
}
];

export const ACHSTRIPEPAYMENT_MODULE_DECLARATIONS = [
    AchStripePaymentHomeComponent,
    AchStripePaymentNewComponent,
    AchStripePaymentDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AchStripePaymentRoutingModule { }