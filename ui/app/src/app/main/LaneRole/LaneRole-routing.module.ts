import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LaneRoleHomeComponent } from './home/LaneRole-home.component';
import { LaneRoleNewComponent } from './new/LaneRole-new.component';
import { LaneRoleDetailComponent } from './detail/LaneRole-detail.component';

const routes: Routes = [
  {path: '', component: LaneRoleHomeComponent},
  { path: 'new', component: LaneRoleNewComponent },
  { path: ':RoleCode', component: LaneRoleDetailComponent,
    data: {
      oPermission: {
        permissionId: 'LaneRole-detail-permissions'
      }
    }
  },{
    path: ':LaneRole/LaneDefinition', loadChildren: () => import('../LaneDefinition/LaneDefinition.module').then(m => m.LaneDefinitionModule),
    data: {
        oPermission: {
            permissionId: 'LaneDefinition-detail-permissions'
        }
    }
}
];

export const LANEROLE_MODULE_DECLARATIONS = [
    LaneRoleHomeComponent,
    LaneRoleNewComponent,
    LaneRoleDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LaneRoleRoutingModule { }