import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFUserRoleHomeComponent } from './home/WFUserRole-home.component';
import { WFUserRoleNewComponent } from './new/WFUserRole-new.component';
import { WFUserRoleDetailComponent } from './detail/WFUserRole-detail.component';

const routes: Routes = [
  {path: '', component: WFUserRoleHomeComponent},
  { path: 'new', component: WFUserRoleNewComponent },
  { path: ':UserName/:UserRole', component: WFUserRoleDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFUserRole-detail-permissions'
      }
    }
  }
];

export const WFUSERROLE_MODULE_DECLARATIONS = [
    WFUserRoleHomeComponent,
    WFUserRoleNewComponent,
    WFUserRoleDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFUserRoleRoutingModule { }