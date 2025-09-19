import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFApplicationCommentHomeComponent } from './home/WFApplicationComment-home.component';
import { WFApplicationCommentNewComponent } from './new/WFApplicationComment-new.component';
import { WFApplicationCommentDetailComponent } from './detail/WFApplicationComment-detail.component';

const routes: Routes = [
  {path: '', component: WFApplicationCommentHomeComponent},
  { path: 'new', component: WFApplicationCommentNewComponent },
  { path: ':CommentID', component: WFApplicationCommentDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFApplicationComment-detail-permissions'
      }
    }
  }
];

export const WFAPPLICATIONCOMMENT_MODULE_DECLARATIONS = [
    WFApplicationCommentHomeComponent,
    WFApplicationCommentNewComponent,
    WFApplicationCommentDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFApplicationCommentRoutingModule { }