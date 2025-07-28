import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PLANTADDRESSTBHomeComponent } from './home/PLANTADDRESSTB-home.component';
import { PLANTADDRESSTBNewComponent } from './new/PLANTADDRESSTB-new.component';
import { PLANTADDRESSTBDetailComponent } from './detail/PLANTADDRESSTB-detail.component';

const routes: Routes = [
  {path: '', component: PLANTADDRESSTBHomeComponent},
  { path: 'new', component: PLANTADDRESSTBNewComponent },
  { path: ':ID', component: PLANTADDRESSTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PLANTADDRESSTB-detail-permissions'
      }
    }
  }
];

export const PLANTADDRESSTB_MODULE_DECLARATIONS = [
    PLANTADDRESSTBHomeComponent,
    PLANTADDRESSTBNewComponent,
    PLANTADDRESSTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PLANTADDRESSTBRoutingModule { }