import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PERSONADDRESSTBHomeComponent } from './home/PERSONADDRESSTB-home.component';
import { PERSONADDRESSTBNewComponent } from './new/PERSONADDRESSTB-new.component';
import { PERSONADDRESSTBDetailComponent } from './detail/PERSONADDRESSTB-detail.component';

const routes: Routes = [
  {path: '', component: PERSONADDRESSTBHomeComponent},
  { path: 'new', component: PERSONADDRESSTBNewComponent },
  { path: ':ID', component: PERSONADDRESSTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PERSONADDRESSTB-detail-permissions'
      }
    }
  }
];

export const PERSONADDRESSTB_MODULE_DECLARATIONS = [
    PERSONADDRESSTBHomeComponent,
    PERSONADDRESSTBNewComponent,
    PERSONADDRESSTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PERSONADDRESSTBRoutingModule { }