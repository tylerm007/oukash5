import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TaskDefinitionHomeComponent } from './home/TaskDefinition-home.component';
import { TaskDefinitionNewComponent } from './new/TaskDefinition-new.component';
import { TaskDefinitionDetailComponent } from './detail/TaskDefinition-detail.component';

const routes: Routes = [
  {path: '', component: TaskDefinitionHomeComponent},
  { path: 'new', component: TaskDefinitionNewComponent },
  { path: ':TaskId', component: TaskDefinitionDetailComponent,
    data: {
      oPermission: {
        permissionId: 'TaskDefinition-detail-permissions'
      }
    }
  },{
    path: ':CurrentTaskId/ProcessInstance', loadChildren: () => import('../ProcessInstance/ProcessInstance.module').then(m => m.ProcessInstanceModule),
    data: {
        oPermission: {
            permissionId: 'ProcessInstance-detail-permissions'
        }
    }
},{
    path: ':FromTaskId/TaskFlow', loadChildren: () => import('../TaskFlow/TaskFlow.module').then(m => m.TaskFlowModule),
    data: {
        oPermission: {
            permissionId: 'TaskFlow-detail-permissions'
        }
    }
},{
    path: ':ToTaskId/TaskFlow', loadChildren: () => import('../TaskFlow/TaskFlow.module').then(m => m.TaskFlowModule),
    data: {
        oPermission: {
            permissionId: 'TaskFlow-detail-permissions'
        }
    }
},{
    path: ':TaskId/TaskInstance', loadChildren: () => import('../TaskInstance/TaskInstance.module').then(m => m.TaskInstanceModule),
    data: {
        oPermission: {
            permissionId: 'TaskInstance-detail-permissions'
        }
    }
}
];

export const TASKDEFINITION_MODULE_DECLARATIONS = [
    TaskDefinitionHomeComponent,
    TaskDefinitionNewComponent,
    TaskDefinitionDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TaskDefinitionRoutingModule { }