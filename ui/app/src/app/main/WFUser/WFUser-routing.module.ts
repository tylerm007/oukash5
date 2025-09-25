import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFUserHomeComponent } from './home/WFUser-home.component';
import { WFUserNewComponent } from './new/WFUser-new.component';
import { WFUserDetailComponent } from './detail/WFUser-detail.component';

const routes: Routes = [
  {path: '', component: WFUserHomeComponent},
  { path: 'new', component: WFUserNewComponent },
  { path: ':Username', component: WFUserDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFUser-detail-permissions'
      }
    }
  },{
    path: ':Assignee/RoleAssigment', loadChildren: () => import('../RoleAssigment/RoleAssigment.module').then(m => m.RoleAssigmentModule),
    data: {
        oPermission: {
            permissionId: 'RoleAssigment-detail-permissions'
        }
    }
},{
    path: ':AdminUserName/WFUSERADMIN', loadChildren: () => import('../WFUSERADMIN/WFUSERADMIN.module').then(m => m.WFUSERADMINModule),
    data: {
        oPermission: {
            permissionId: 'WFUSERADMIN-detail-permissions'
        }
    }
},{
    path: ':UserName/WFUSERADMIN', loadChildren: () => import('../WFUSERADMIN/WFUSERADMIN.module').then(m => m.WFUSERADMINModule),
    data: {
        oPermission: {
            permissionId: 'WFUSERADMIN-detail-permissions'
        }
    }
},{
    path: ':UserName/WFUSERROLE', loadChildren: () => import('../WFUSERROLE/WFUSERROLE.module').then(m => m.WFUSERROLEModule),
    data: {
        oPermission: {
            permissionId: 'WFUSERROLE-detail-permissions'
        }
    }
}
];

export const WFUSER_MODULE_DECLARATIONS = [
    WFUserHomeComponent,
    WFUserNewComponent,
    WFUserDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFUserRoutingModule { }