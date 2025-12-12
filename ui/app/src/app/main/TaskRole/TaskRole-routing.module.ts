import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TaskRoleHomeComponent } from './home/TaskRole-home.component';
import { TaskRoleNewComponent } from './new/TaskRole-new.component';
import { TaskRoleDetailComponent } from './detail/TaskRole-detail.component';

const routes: Routes = [
  {path: '', component: TaskRoleHomeComponent},
  { path: 'new', component: TaskRoleNewComponent },
  { path: ':RoleCode', component: TaskRoleDetailComponent,
    data: {
      oPermission: {
        permissionId: 'TaskRole-detail-permissions'
      }
    }
  }
];

export const TASKROLE_MODULE_DECLARATIONS = [
    TaskRoleHomeComponent,
    TaskRoleNewComponent,
    TaskRoleDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TaskRoleRoutingModule { }