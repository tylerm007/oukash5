import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFUserAdminHomeComponent } from './home/WFUserAdmin-home.component';
import { WFUserAdminNewComponent } from './new/WFUserAdmin-new.component';
import { WFUserAdminDetailComponent } from './detail/WFUserAdmin-detail.component';

const routes: Routes = [
  {path: '', component: WFUserAdminHomeComponent},
  { path: 'new', component: WFUserAdminNewComponent },
  { path: ':UserName/:AdminUserName', component: WFUserAdminDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFUserAdmin-detail-permissions'
      }
    }
  }
];

export const WFUSERADMIN_MODULE_DECLARATIONS = [
    WFUserAdminHomeComponent,
    WFUserAdminNewComponent,
    WFUserAdminDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFUserAdminRoutingModule { }