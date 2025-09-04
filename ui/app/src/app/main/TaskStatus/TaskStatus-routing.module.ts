import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TaskStatusHomeComponent } from './home/TaskStatus-home.component';
import { TaskStatusNewComponent } from './new/TaskStatus-new.component';
import { TaskStatusDetailComponent } from './detail/TaskStatus-detail.component';

const routes: Routes = [
  {path: '', component: TaskStatusHomeComponent},
  { path: 'new', component: TaskStatusNewComponent },
  { path: ':StatusCode', component: TaskStatusDetailComponent,
    data: {
      oPermission: {
        permissionId: 'TaskStatus-detail-permissions'
      }
    }
  },{
    path: ':Status/TaskInstance', loadChildren: () => import('../TaskInstance/TaskInstance.module').then(m => m.TaskInstanceModule),
    data: {
        oPermission: {
            permissionId: 'TaskInstance-detail-permissions'
        }
    }
}
];

export const TASKSTATUS_MODULE_DECLARATIONS = [
    TaskStatusHomeComponent,
    TaskStatusNewComponent,
    TaskStatusDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TaskStatusRoutingModule { }