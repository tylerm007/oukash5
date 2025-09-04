import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFRoleHomeComponent } from './home/WFRole-home.component';
import { WFRoleNewComponent } from './new/WFRole-new.component';
import { WFRoleDetailComponent } from './detail/WFRole-detail.component';

const routes: Routes = [
  {path: '', component: WFRoleHomeComponent},
  { path: 'new', component: WFRoleNewComponent },
  { path: ':UserRole', component: WFRoleDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFRole-detail-permissions'
      }
    }
  },{
    path: ':Role/WFUser', loadChildren: () => import('../WFUser/WFUser.module').then(m => m.WFUserModule),
    data: {
        oPermission: {
            permissionId: 'WFUser-detail-permissions'
        }
    }
}
];

export const WFROLE_MODULE_DECLARATIONS = [
    WFRoleHomeComponent,
    WFRoleNewComponent,
    WFRoleDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFRoleRoutingModule { }