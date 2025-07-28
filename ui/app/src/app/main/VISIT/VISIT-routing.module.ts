import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { VISITHomeComponent } from './home/VISIT-home.component';
import { VISITNewComponent } from './new/VISIT-new.component';
import { VISITDetailComponent } from './detail/VISIT-detail.component';

const routes: Routes = [
  {path: '', component: VISITHomeComponent},
  { path: 'new', component: VISITNewComponent },
  { path: ':VISIT_ID', component: VISITDetailComponent,
    data: {
      oPermission: {
        permissionId: 'VISIT-detail-permissions'
      }
    }
  },{
    path: ':MainVisit/VISIT', loadChildren: () => import('../VISIT/VISIT.module').then(m => m.VISITModule),
    data: {
        oPermission: {
            permissionId: 'VISIT-detail-permissions'
        }
    }
}
];

export const VISIT_MODULE_DECLARATIONS = [
    VISITHomeComponent,
    VISITNewComponent,
    VISITDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class VISITRoutingModule { }