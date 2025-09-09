import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TaskInstanceHomeComponent } from './home/TaskInstance-home.component';
import { TaskInstanceNewComponent } from './new/TaskInstance-new.component';
import { TaskInstanceDetailComponent } from './detail/TaskInstance-detail.component';

const routes: Routes = [
  {path: '', component: TaskInstanceHomeComponent},
  { path: 'new', component: TaskInstanceNewComponent },
  { path: ':TaskInstanceId', component: TaskInstanceDetailComponent,
    data: {
      oPermission: {
        permissionId: 'TaskInstance-detail-permissions'
      }
    }
  },{
    path: ':TaskInstanceId/TaskComment', loadChildren: () => import('../TaskComment/TaskComment.module').then(m => m.TaskCommentModule),
    data: {
        oPermission: {
            permissionId: 'TaskComment-detail-permissions'
        }
    }
},{
    path: ':ParentInstanceId/TaskInstance', loadChildren: () => import('../TaskInstance/TaskInstance.module').then(m => m.TaskInstanceModule),
    data: {
        oPermission: {
            permissionId: 'TaskInstance-detail-permissions'
        }
    }
},{
    path: ':TaskInstanceId/WorkflowHistory', loadChildren: () => import('../WorkflowHistory/WorkflowHistory.module').then(m => m.WorkflowHistoryModule),
    data: {
        oPermission: {
            permissionId: 'WorkflowHistory-detail-permissions'
        }
    }
}
];

export const TASKINSTANCE_MODULE_DECLARATIONS = [
    TaskInstanceHomeComponent,
    TaskInstanceNewComponent,
    TaskInstanceDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TaskInstanceRoutingModule { }