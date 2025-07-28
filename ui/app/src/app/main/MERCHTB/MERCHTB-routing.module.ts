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
    path: ':ComponentMerchID/FormulaComponent', loadChildren: () => import('../FormulaComponent/FormulaComponent.module').then(m => m.FormulaComponentModule),
    data: {
        oPermission: {
            permissionId: 'FormulaComponent-detail-permissions'
        }
    }
},{
    path: ':Merchandise_ID/FormulaProduct', loadChildren: () => import('../FormulaProduct/FormulaProduct.module').then(m => m.FormulaProductModule),
    data: {
        oPermission: {
            permissionId: 'FormulaProduct-detail-permissions'
        }
    }
},{
    path: ':ComponentMerchID/FormulaSubmissionComponent', loadChildren: () => import('../FormulaSubmissionComponent/FormulaSubmissionComponent.module').then(m => m.FormulaSubmissionComponentModule),
    data: {
        oPermission: {
            permissionId: 'FormulaSubmissionComponent-detail-permissions'
        }
    }
},{
    path: ':MERCHANDISE_ID/LabelTb', loadChildren: () => import('../LabelTb/LabelTb.module').then(m => m.LabelTbModule),
    data: {
        oPermission: {
            permissionId: 'LabelTb-detail-permissions'
        }
    }
},{
    path: ':MERCHANDISE_ID/MERCHOTHERNAME', loadChildren: () => import('../MERCHOTHERNAME/MERCHOTHERNAME.module').then(m => m.MERCHOTHERNAMEModule),
    data: {
        oPermission: {
            permissionId: 'MERCHOTHERNAME-detail-permissions'
        }
    }
},{
    path: ':MerchId/YoshonInfo', loadChildren: () => import('../YoshonInfo/YoshonInfo.module').then(m => m.YoshonInfoModule),
    data: {
        oPermission: {
            permissionId: 'YoshonInfo-detail-permissions'
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