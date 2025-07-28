import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LabelCommentHomeComponent } from './home/LabelComment-home.component';
import { LabelCommentNewComponent } from './new/LabelComment-new.component';
import { LabelCommentDetailComponent } from './detail/LabelComment-detail.component';

const routes: Routes = [
  {path: '', component: LabelCommentHomeComponent},
  { path: 'new', component: LabelCommentNewComponent },
  { path: ':CommentID', component: LabelCommentDetailComponent,
    data: {
      oPermission: {
        permissionId: 'LabelComment-detail-permissions'
      }
    }
  }
];

export const LABELCOMMENT_MODULE_DECLARATIONS = [
    LabelCommentHomeComponent,
    LabelCommentNewComponent,
    LabelCommentDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LabelCommentRoutingModule { }