import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ASSIGNEDMASHGIACHTBHomeComponent } from './home/ASSIGNEDMASHGIACHTB-home.component';
import { ASSIGNEDMASHGIACHTBNewComponent } from './new/ASSIGNEDMASHGIACHTB-new.component';
import { ASSIGNEDMASHGIACHTBDetailComponent } from './detail/ASSIGNEDMASHGIACHTB-detail.component';

const routes: Routes = [
  {path: '', component: ASSIGNEDMASHGIACHTBHomeComponent},
  { path: 'new', component: ASSIGNEDMASHGIACHTBNewComponent },
  { path: ':ID', component: ASSIGNEDMASHGIACHTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ASSIGNEDMASHGIACHTB-detail-permissions'
      }
    }
  }
];

export const ASSIGNEDMASHGIACHTB_MODULE_DECLARATIONS = [
    ASSIGNEDMASHGIACHTBHomeComponent,
    ASSIGNEDMASHGIACHTBNewComponent,
    ASSIGNEDMASHGIACHTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ASSIGNEDMASHGIACHTBRoutingModule { }