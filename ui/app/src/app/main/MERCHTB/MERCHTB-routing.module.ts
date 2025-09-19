import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MERCHTBHomeComponent } from './home/MERCHTB-home.component';
import { MERCHTBNewComponent } from './new/MERCHTB-new.component';
import { MERCHTBDetailComponent } from './detail/MERCHTB-detail.component';

const routes: Routes = [
  {path: '', component: MERCHTBHomeComponent},
  { path: 'new', component: MERCHTBNewComponent },
  { path: ':MERCHANDISE_ID', component: MERCHTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'MERCHTB-detail-permissions'
      }
    }
  },{
    path: ':ComponentMerchID/FormulaSubmissionComponent', loadChildren: () => import('../FormulaSubmissionComponent/FormulaSubmissionComponent.module').then(m => m.FormulaSubmissionComponentModule),
    data: {
        oPermission: {
            permissionId: 'FormulaSubmissionComponent-detail-permissions'
        }
    }
}
];

export const MERCHTB_MODULE_DECLARATIONS = [
    MERCHTBHomeComponent,
    MERCHTBNewComponent,
    MERCHTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MERCHTBRoutingModule { }