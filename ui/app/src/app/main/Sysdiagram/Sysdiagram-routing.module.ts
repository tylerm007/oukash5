import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SysdiagramHomeComponent } from './home/Sysdiagram-home.component';
import { SysdiagramNewComponent } from './new/Sysdiagram-new.component';
import { SysdiagramDetailComponent } from './detail/Sysdiagram-detail.component';

const routes: Routes = [
  {path: '', component: SysdiagramHomeComponent},
  { path: 'new', component: SysdiagramNewComponent },
  { path: ':diagram_id', component: SysdiagramDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Sysdiagram-detail-permissions'
      }
    }
  }
];

export const SYSDIAGRAM_MODULE_DECLARATIONS = [
    SysdiagramHomeComponent,
    SysdiagramNewComponent,
    SysdiagramDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SysdiagramRoutingModule { }