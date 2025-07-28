import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PERSONJOBTBHomeComponent } from './home/PERSONJOBTB-home.component';
import { PERSONJOBTBNewComponent } from './new/PERSONJOBTB-new.component';
import { PERSONJOBTBDetailComponent } from './detail/PERSONJOBTB-detail.component';

const routes: Routes = [
  {path: '', component: PERSONJOBTBHomeComponent},
  { path: 'new', component: PERSONJOBTBNewComponent },
  { path: ':PERSON_JOB_ID', component: PERSONJOBTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PERSONJOBTB-detail-permissions'
      }
    }
  },{
    path: ':Setup_By/OWNSTB', loadChildren: () => import('../OWNSTB/OWNSTB.module').then(m => m.OWNSTBModule),
    data: {
        oPermission: {
            permissionId: 'OWNSTB-detail-permissions'
        }
    }
},{
    path: ':AdministrativeAssistant/PERSONTB', loadChildren: () => import('../PERSONTB/PERSONTB.module').then(m => m.PERSONTBModule),
    data: {
        oPermission: {
            permissionId: 'PERSONTB-detail-permissions'
        }
    }
},{
    path: ':DesignatedRFR/PLANTTB', loadChildren: () => import('../PLANTTB/PLANTTB.module').then(m => m.PLANTTBModule),
    data: {
        oPermission: {
            permissionId: 'PLANTTB-detail-permissions'
        }
    }
},{
    path: ':DesignatedRFR/PLANTTB', loadChildren: () => import('../PLANTTB/PLANTTB.module').then(m => m.PLANTTBModule),
    data: {
        oPermission: {
            permissionId: 'PLANTTB-detail-permissions'
        }
    }
},{
    path: ':AssignedTo/ProductJobLineItem', loadChildren: () => import('../ProductJobLineItem/ProductJobLineItem.module').then(m => m.ProductJobLineItemModule),
    data: {
        oPermission: {
            permissionId: 'ProductJobLineItem-detail-permissions'
        }
    }
},{
    path: ':PERSON_JOB_ID/RCTB', loadChildren: () => import('../RCTB/RCTB.module').then(m => m.RCTBModule),
    data: {
        oPermission: {
            permissionId: 'RCTB-detail-permissions'
        }
    }
},{
    path: ':ACTUAL_PERSON_JOB_ID/VISIT', loadChildren: () => import('../VISIT/VISIT.module').then(m => m.VISITModule),
    data: {
        oPermission: {
            permissionId: 'VISIT-detail-permissions'
        }
    }
},{
    path: ':ASSIGNED_PERSON_JOB_ID/VISIT', loadChildren: () => import('../VISIT/VISIT.module').then(m => m.VISITModule),
    data: {
        oPermission: {
            permissionId: 'VISIT-detail-permissions'
        }
    }
}
];

export const PERSONJOBTB_MODULE_DECLARATIONS = [
    PERSONJOBTBHomeComponent,
    PERSONJOBTBNewComponent,
    PERSONJOBTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PERSONJOBTBRoutingModule { }