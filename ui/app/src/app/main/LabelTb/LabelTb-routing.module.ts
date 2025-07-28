import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LabelTbHomeComponent } from './home/LabelTb-home.component';
import { LabelTbNewComponent } from './new/LabelTb-new.component';
import { LabelTbDetailComponent } from './detail/LabelTb-detail.component';

const routes: Routes = [
  {path: '', component: LabelTbHomeComponent},
  { path: 'new', component: LabelTbNewComponent },
  { path: ':ID', component: LabelTbDetailComponent,
    data: {
      oPermission: {
        permissionId: 'LabelTb-detail-permissions'
      }
    }
  },{
    path: ':ComponentLabelID/FormulaComponent', loadChildren: () => import('../FormulaComponent/FormulaComponent.module').then(m => m.FormulaComponentModule),
    data: {
        oPermission: {
            permissionId: 'FormulaComponent-detail-permissions'
        }
    }
},{
    path: ':ComponentLabelID/FormulaSubmissionComponent', loadChildren: () => import('../FormulaSubmissionComponent/FormulaSubmissionComponent.module').then(m => m.FormulaSubmissionComponentModule),
    data: {
        oPermission: {
            permissionId: 'FormulaSubmissionComponent-detail-permissions'
        }
    }
},{
    path: ':labelId/LabelBarcode', loadChildren: () => import('../LabelBarcode/LabelBarcode.module').then(m => m.LabelBarcodeModule),
    data: {
        oPermission: {
            permissionId: 'LabelBarcode-detail-permissions'
        }
    }
},{
    path: ':LabelId/LabelComment', loadChildren: () => import('../LabelComment/LabelComment.module').then(m => m.LabelCommentModule),
    data: {
        oPermission: {
            permissionId: 'LabelComment-detail-permissions'
        }
    }
},{
    path: ':LabelID/LabelOption', loadChildren: () => import('../LabelOption/LabelOption.module').then(m => m.LabelOptionModule),
    data: {
        oPermission: {
            permissionId: 'LabelOption-detail-permissions'
        }
    }
},{
    path: ':LabelID/LabelOption', loadChildren: () => import('../LabelOption/LabelOption.module').then(m => m.LabelOptionModule),
    data: {
        oPermission: {
            permissionId: 'LabelOption-detail-permissions'
        }
    }
},{
    path: ':LabelID/ProducedIn1Tb', loadChildren: () => import('../ProducedIn1Tb/ProducedIn1Tb.module').then(m => m.ProducedIn1TbModule),
    data: {
        oPermission: {
            permissionId: 'ProducedIn1Tb-detail-permissions'
        }
    }
},{
    path: ':LabelID/USEDIN1TB', loadChildren: () => import('../USEDIN1TB/USEDIN1TB.module').then(m => m.USEDIN1TBModule),
    data: {
        oPermission: {
            permissionId: 'USEDIN1TB-detail-permissions'
        }
    }
}
];

export const LABELTB_MODULE_DECLARATIONS = [
    LabelTbHomeComponent,
    LabelTbNewComponent,
    LabelTbDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LabelTbRoutingModule { }