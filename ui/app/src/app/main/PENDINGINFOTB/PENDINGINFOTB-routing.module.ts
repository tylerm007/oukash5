import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PENDINGINFOTBHomeComponent } from './home/PENDINGINFOTB-home.component';
import { PENDINGINFOTBNewComponent } from './new/PENDINGINFOTB-new.component';
import { PENDINGINFOTBDetailComponent } from './detail/PENDINGINFOTB-detail.component';

const routes: Routes = [
  {path: '', component: PENDINGINFOTBHomeComponent},
  { path: 'new', component: PENDINGINFOTBNewComponent },
  { path: ':ID', component: PENDINGINFOTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PENDINGINFOTB-detail-permissions'
      }
    }
  }
];

export const PENDINGINFOTB_MODULE_DECLARATIONS = [
    PENDINGINFOTBHomeComponent,
    PENDINGINFOTBNewComponent,
    PENDINGINFOTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PENDINGINFOTBRoutingModule { }