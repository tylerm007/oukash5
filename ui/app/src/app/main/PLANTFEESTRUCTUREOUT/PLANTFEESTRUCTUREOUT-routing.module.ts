import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PLANTFEESTRUCTUREOUTHomeComponent } from './home/PLANTFEESTRUCTUREOUT-home.component';
import { PLANTFEESTRUCTUREOUTNewComponent } from './new/PLANTFEESTRUCTUREOUT-new.component';
import { PLANTFEESTRUCTUREOUTDetailComponent } from './detail/PLANTFEESTRUCTUREOUT-detail.component';

const routes: Routes = [
  {path: '', component: PLANTFEESTRUCTUREOUTHomeComponent},
  { path: 'new', component: PLANTFEESTRUCTUREOUTNewComponent },
  { path: ':ID', component: PLANTFEESTRUCTUREOUTDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PLANTFEESTRUCTUREOUT-detail-permissions'
      }
    }
  },{
    path: ':PFSO_ID/Billing', loadChildren: () => import('../Billing/Billing.module').then(m => m.BillingModule),
    data: {
        oPermission: {
            permissionId: 'Billing-detail-permissions'
        }
    }
}
];

export const PLANTFEESTRUCTUREOUT_MODULE_DECLARATIONS = [
    PLANTFEESTRUCTUREOUTHomeComponent,
    PLANTFEESTRUCTUREOUTNewComponent,
    PLANTFEESTRUCTUREOUTDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PLANTFEESTRUCTUREOUTRoutingModule { }