import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RoleAssigmentHomeComponent } from './home/RoleAssigment-home.component';
import { RoleAssigmentNewComponent } from './new/RoleAssigment-new.component';
import { RoleAssigmentDetailComponent } from './detail/RoleAssigment-detail.component';

const routes: Routes = [
  {path: '', component: RoleAssigmentHomeComponent},
  { path: 'new', component: RoleAssigmentNewComponent },
  { path: ':RoleAssigmentID', component: RoleAssigmentDetailComponent,
    data: {
      oPermission: {
        permissionId: 'RoleAssigment-detail-permissions'
      }
    }
  }
];

export const ROLEASSIGMENT_MODULE_DECLARATIONS = [
    RoleAssigmentHomeComponent,
    RoleAssigmentNewComponent,
    RoleAssigmentDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RoleAssigmentRoutingModule { }