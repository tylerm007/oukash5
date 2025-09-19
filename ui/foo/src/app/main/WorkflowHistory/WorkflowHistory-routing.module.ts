import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WorkflowHistoryHomeComponent } from './home/WorkflowHistory-home.component';
import { WorkflowHistoryNewComponent } from './new/WorkflowHistory-new.component';
import { WorkflowHistoryDetailComponent } from './detail/WorkflowHistory-detail.component';

const routes: Routes = [
  {path: '', component: WorkflowHistoryHomeComponent},
  { path: 'new', component: WorkflowHistoryNewComponent },
  { path: ':HistoryId', component: WorkflowHistoryDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WorkflowHistory-detail-permissions'
      }
    }
  }
];

export const WORKFLOWHISTORY_MODULE_DECLARATIONS = [
    WorkflowHistoryHomeComponent,
    WorkflowHistoryNewComponent,
    WorkflowHistoryDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WorkflowHistoryRoutingModule { }