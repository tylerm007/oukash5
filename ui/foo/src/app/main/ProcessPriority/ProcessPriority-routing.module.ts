import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProcessPriorityHomeComponent } from './home/ProcessPriority-home.component';
import { ProcessPriorityNewComponent } from './new/ProcessPriority-new.component';
import { ProcessPriorityDetailComponent } from './detail/ProcessPriority-detail.component';

const routes: Routes = [
  {path: '', component: ProcessPriorityHomeComponent},
  { path: 'new', component: ProcessPriorityNewComponent },
  { path: ':PriorityCode', component: ProcessPriorityDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ProcessPriority-detail-permissions'
      }
    }
  },{
    path: ':Priority/ProcessInstance', loadChildren: () => import('../ProcessInstance/ProcessInstance.module').then(m => m.ProcessInstanceModule),
    data: {
        oPermission: {
            permissionId: 'ProcessInstance-detail-permissions'
        }
    }
}
];

export const PROCESSPRIORITY_MODULE_DECLARATIONS = [
    ProcessPriorityHomeComponent,
    ProcessPriorityNewComponent,
    ProcessPriorityDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProcessPriorityRoutingModule { }