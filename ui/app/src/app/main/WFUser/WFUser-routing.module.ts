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
    path: ':Assignee/RoleAssignment', loadChildren: () => import('../RoleAssignment/RoleAssignment.module').then(m => m.RoleAssignmentModule),
    data: {
        oPermission: {
            permissionId: 'RoleAssignment-detail-permissions'
        }
    }
},{
    path: ':FromUser/WFApplicationMessage', loadChildren: () => import('../WFApplicationMessage/WFApplicationMessage.module').then(m => m.WFApplicationMessageModule),
    data: {
        oPermission: {
            permissionId: 'WFApplicationMessage-detail-permissions'
        }
    }
},{
    path: ':ToUser/WFApplicationMessage', loadChildren: () => import('../WFApplicationMessage/WFApplicationMessage.module').then(m => m.WFApplicationMessageModule),
    data: {
        oPermission: {
            permissionId: 'WFApplicationMessage-detail-permissions'
        }
    }
},{
    path: ':AdminUserName/WFUserAdmin', loadChildren: () => import('../WFUserAdmin/WFUserAdmin.module').then(m => m.WFUserAdminModule),
    data: {
        oPermission: {
            permissionId: 'WFUserAdmin-detail-permissions'
        }
    }
},{
    path: ':UserName/WFUserAdmin', loadChildren: () => import('../WFUserAdmin/WFUserAdmin.module').then(m => m.WFUserAdminModule),
    data: {
        oPermission: {
            permissionId: 'WFUserAdmin-detail-permissions'
        }
    }
},{
    path: ':UserName/WFUserRole', loadChildren: () => import('../WFUserRole/WFUserRole.module').then(m => m.WFUserRoleModule),
    data: {
        oPermission: {
            permissionId: 'WFUserRole-detail-permissions'
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