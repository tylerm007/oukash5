import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFUSERROLEHomeComponent } from './home/WFUSERROLE-home.component';
import { WFUSERROLENewComponent } from './new/WFUSERROLE-new.component';
import { WFUSERROLEDetailComponent } from './detail/WFUSERROLE-detail.component';

const routes: Routes = [
  {path: '', component: WFUSERROLEHomeComponent},
  { path: 'new', component: WFUSERROLENewComponent },
  { path: ':UserName/:UserRole', component: WFUSERROLEDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFUSERROLE-detail-permissions'
      }
    }
  }
];

export const WFUSERROLE_MODULE_DECLARATIONS = [
    WFUSERROLEHomeComponent,
    WFUSERROLENewComponent,
    WFUSERROLEDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFUSERROLERoutingModule { }