import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TaskFlowHomeComponent } from './home/TaskFlow-home.component';
import { TaskFlowNewComponent } from './new/TaskFlow-new.component';
import { TaskFlowDetailComponent } from './detail/TaskFlow-detail.component';

const routes: Routes = [
  {path: '', component: TaskFlowHomeComponent},
  { path: 'new', component: TaskFlowNewComponent },
  { path: ':FlowId', component: TaskFlowDetailComponent,
    data: {
      oPermission: {
        permissionId: 'TaskFlow-detail-permissions'
      }
    }
  }
];

export const TASKFLOW_MODULE_DECLARATIONS = [
    TaskFlowHomeComponent,
    TaskFlowNewComponent,
    TaskFlowDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TaskFlowRoutingModule { }