import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TaskTypeHomeComponent } from './home/TaskType-home.component';
import { TaskTypeNewComponent } from './new/TaskType-new.component';
import { TaskTypeDetailComponent } from './detail/TaskType-detail.component';

const routes: Routes = [
  {path: '', component: TaskTypeHomeComponent},
  { path: 'new', component: TaskTypeNewComponent },
  { path: ':TaskTypeCode', component: TaskTypeDetailComponent,
    data: {
      oPermission: {
        permissionId: 'TaskType-detail-permissions'
      }
    }
  },{
    path: ':TaskType/TaskDefinition', loadChildren: () => import('../TaskDefinition/TaskDefinition.module').then(m => m.TaskDefinitionModule),
    data: {
        oPermission: {
            permissionId: 'TaskDefinition-detail-permissions'
        }
    }
}
];

export const TASKTYPE_MODULE_DECLARATIONS = [
    TaskTypeHomeComponent,
    TaskTypeNewComponent,
    TaskTypeDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TaskTypeRoutingModule { }