import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProcessInstanceHomeComponent } from './home/ProcessInstance-home.component';
import { ProcessInstanceNewComponent } from './new/ProcessInstance-new.component';
import { ProcessInstanceDetailComponent } from './detail/ProcessInstance-detail.component';

const routes: Routes = [
  {path: '', component: ProcessInstanceHomeComponent},
  { path: 'new', component: ProcessInstanceNewComponent },
  { path: ':InstanceId', component: ProcessInstanceDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ProcessInstance-detail-permissions'
      }
    }
  },{
    path: ':InstanceId/ProcessMessage', loadChildren: () => import('../ProcessMessage/ProcessMessage.module').then(m => m.ProcessMessageModule),
    data: {
        oPermission: {
            permissionId: 'ProcessMessage-detail-permissions'
        }
    }
},{
    path: ':ProcessInstanceId/StageInstance', loadChildren: () => import('../StageInstance/StageInstance.module').then(m => m.StageInstanceModule),
    data: {
        oPermission: {
            permissionId: 'StageInstance-detail-permissions'
        }
    }
},{
    path: ':InstanceId/WorkflowHistory', loadChildren: () => import('../WorkflowHistory/WorkflowHistory.module').then(m => m.WorkflowHistoryModule),
    data: {
        oPermission: {
            permissionId: 'WorkflowHistory-detail-permissions'
        }
    }
}
];

export const PROCESSINSTANCE_MODULE_DECLARATIONS = [
    ProcessInstanceHomeComponent,
    ProcessInstanceNewComponent,
    ProcessInstanceDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProcessInstanceRoutingModule { }