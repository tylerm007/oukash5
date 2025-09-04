import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TaskCommentTypeHomeComponent } from './home/TaskCommentType-home.component';
import { TaskCommentTypeNewComponent } from './new/TaskCommentType-new.component';
import { TaskCommentTypeDetailComponent } from './detail/TaskCommentType-detail.component';

const routes: Routes = [
  {path: '', component: TaskCommentTypeHomeComponent},
  { path: 'new', component: TaskCommentTypeNewComponent },
  { path: ':CommentTypeCode', component: TaskCommentTypeDetailComponent,
    data: {
      oPermission: {
        permissionId: 'TaskCommentType-detail-permissions'
      }
    }
  }
];

export const TASKCOMMENTTYPE_MODULE_DECLARATIONS = [
    TaskCommentTypeHomeComponent,
    TaskCommentTypeNewComponent,
    TaskCommentTypeDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TaskCommentTypeRoutingModule { }