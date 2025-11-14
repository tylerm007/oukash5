import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RoleAssignmentHomeComponent } from './home/RoleAssignment-home.component';
import { RoleAssignmentNewComponent } from './new/RoleAssignment-new.component';
import { RoleAssignmentDetailComponent } from './detail/RoleAssignment-detail.component';

const routes: Routes = [
  {path: '', component: RoleAssignmentHomeComponent},
  { path: 'new', component: RoleAssignmentNewComponent },
  { path: ':RoleAssignmentID', component: RoleAssignmentDetailComponent,
    data: {
      oPermission: {
        permissionId: 'RoleAssignment-detail-permissions'
      }
    }
  }
];

export const ROLEASSIGNMENT_MODULE_DECLARATIONS = [
    RoleAssignmentHomeComponent,
    RoleAssignmentNewComponent,
    RoleAssignmentDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RoleAssignmentRoutingModule { }