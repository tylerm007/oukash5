import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TaskCommentHomeComponent } from './home/TaskComment-home.component';
import { TaskCommentNewComponent } from './new/TaskComment-new.component';
import { TaskCommentDetailComponent } from './detail/TaskComment-detail.component';

const routes: Routes = [
  {path: '', component: TaskCommentHomeComponent},
  { path: 'new', component: TaskCommentNewComponent },
  { path: ':CommentId', component: TaskCommentDetailComponent,
    data: {
      oPermission: {
        permissionId: 'TaskComment-detail-permissions'
      }
    }
  }
];

export const TASKCOMMENT_MODULE_DECLARATIONS = [
    TaskCommentHomeComponent,
    TaskCommentNewComponent,
    TaskCommentDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TaskCommentRoutingModule { }