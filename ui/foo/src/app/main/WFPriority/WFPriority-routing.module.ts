import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFPriorityHomeComponent } from './home/WFPriority-home.component';
import { WFPriorityNewComponent } from './new/WFPriority-new.component';
import { WFPriorityDetailComponent } from './detail/WFPriority-detail.component';

const routes: Routes = [
  {path: '', component: WFPriorityHomeComponent},
  { path: 'new', component: WFPriorityNewComponent },
  { path: ':PriorityCode', component: WFPriorityDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFPriority-detail-permissions'
      }
    }
  },{
    path: ':Priority/WFApplication', loadChildren: () => import('../WFApplication/WFApplication.module').then(m => m.WFApplicationModule),
    data: {
        oPermission: {
            permissionId: 'WFApplication-detail-permissions'
        }
    }
}
];

export const WFPRIORITY_MODULE_DECLARATIONS = [
    WFPriorityHomeComponent,
    WFPriorityNewComponent,
    WFPriorityDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFPriorityRoutingModule { }