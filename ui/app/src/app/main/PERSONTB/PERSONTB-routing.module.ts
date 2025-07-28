import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PERSONTBHomeComponent } from './home/PERSONTB-home.component';
import { PERSONTBNewComponent } from './new/PERSONTB-new.component';
import { PERSONTBDetailComponent } from './detail/PERSONTB-detail.component';

const routes: Routes = [
  {path: '', component: PERSONTBHomeComponent},
  { path: 'new', component: PERSONTBNewComponent },
  { path: ':PERSON_ID', component: PERSONTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PERSONTB-detail-permissions'
      }
    }
  },{
    path: ':PERSON_ID/PERSONADDRESSTB', loadChildren: () => import('../PERSONADDRESSTB/PERSONADDRESSTB.module').then(m => m.PERSONADDRESSTBModule),
    data: {
        oPermission: {
            permissionId: 'PERSONADDRESSTB-detail-permissions'
        }
    }
},{
    path: ':PERSON_ID/PERSONJOBTB', loadChildren: () => import('../PERSONJOBTB/PERSONJOBTB.module').then(m => m.PERSONJOBTBModule),
    data: {
        oPermission: {
            permissionId: 'PERSONJOBTB-detail-permissions'
        }
    }
}
];

export const PERSONTB_MODULE_DECLARATIONS = [
    PERSONTBHomeComponent,
    PERSONTBNewComponent,
    PERSONTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PERSONTBRoutingModule { }