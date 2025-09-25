import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFUSERADMINHomeComponent } from './home/WFUSERADMIN-home.component';
import { WFUSERADMINNewComponent } from './new/WFUSERADMIN-new.component';
import { WFUSERADMINDetailComponent } from './detail/WFUSERADMIN-detail.component';

const routes: Routes = [
  {path: '', component: WFUSERADMINHomeComponent},
  { path: 'new', component: WFUSERADMINNewComponent },
  { path: ':UserName/:AdminUserName', component: WFUSERADMINDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFUSERADMIN-detail-permissions'
      }
    }
  }
];

export const WFUSERADMIN_MODULE_DECLARATIONS = [
    WFUSERADMINHomeComponent,
    WFUSERADMINNewComponent,
    WFUSERADMINDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFUSERADMINRoutingModule { }