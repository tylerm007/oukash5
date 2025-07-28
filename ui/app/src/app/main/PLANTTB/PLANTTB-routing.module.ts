import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PLANTTBHomeComponent } from './home/PLANTTB-home.component';
import { PLANTTBNewComponent } from './new/PLANTTB-new.component';
import { PLANTTBDetailComponent } from './detail/PLANTTB-detail.component';

const routes: Routes = [
  {path: '', component: PLANTTBHomeComponent},
  { path: 'new', component: PLANTTBNewComponent },
  { path: ':PLANT_ID', component: PLANTTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PLANTTB-detail-permissions'
      }
    }
  },{
    path: ':Plant_id/CompanyPlantOption', loadChildren: () => import('../CompanyPlantOption/CompanyPlantOption.module').then(m => m.CompanyPlantOptionModule),
    data: {
        oPermission: {
            permissionId: 'CompanyPlantOption-detail-permissions'
        }
    }
},{
    path: ':BILL_TO_PLANT_ID/INVOICEFEE', loadChildren: () => import('../INVOICEFEE/INVOICEFEE.module').then(m => m.INVOICEFEEModule),
    data: {
        oPermission: {
            permissionId: 'INVOICEFEE-detail-permissions'
        }
    }
},{
    path: ':PLANT_ID/OWNSTB', loadChildren: () => import('../OWNSTB/OWNSTB.module').then(m => m.OWNSTBModule),
    data: {
        oPermission: {
            permissionId: 'OWNSTB-detail-permissions'
        }
    }
},{
    path: ':PLANT_ID/PENDINGINFOTB', loadChildren: () => import('../PENDINGINFOTB/PENDINGINFOTB.module').then(m => m.PENDINGINFOTBModule),
    data: {
        oPermission: {
            permissionId: 'PENDINGINFOTB-detail-permissions'
        }
    }
},{
    path: ':PLANT_ID/PLANTADDRESSTB', loadChildren: () => import('../PLANTADDRESSTB/PLANTADDRESSTB.module').then(m => m.PLANTADDRESSTBModule),
    data: {
        oPermission: {
            permissionId: 'PLANTADDRESSTB-detail-permissions'
        }
    }
},{
    path: ':PLANT_ID/PLANTCERTDETAIL', loadChildren: () => import('../PLANTCERTDETAIL/PLANTCERTDETAIL.module').then(m => m.PLANTCERTDETAILModule),
    data: {
        oPermission: {
            permissionId: 'PLANTCERTDETAIL-detail-permissions'
        }
    }
},{
    path: ':PLANT_ID/PLANTCOMMENT', loadChildren: () => import('../PLANTCOMMENT/PLANTCOMMENT.module').then(m => m.PLANTCOMMENTModule),
    data: {
        oPermission: {
            permissionId: 'PLANTCOMMENT-detail-permissions'
        }
    }
},{
    path: ':PLANT_ID/PLANTFEECOMMENT', loadChildren: () => import('../PLANTFEECOMMENT/PLANTFEECOMMENT.module').then(m => m.PLANTFEECOMMENTModule),
    data: {
        oPermission: {
            permissionId: 'PLANTFEECOMMENT-detail-permissions'
        }
    }
},{
    path: ':PLANT_ID/PLANTFEESTRUCTUREOUT', loadChildren: () => import('../PLANTFEESTRUCTUREOUT/PLANTFEESTRUCTUREOUT.module').then(m => m.PLANTFEESTRUCTUREOUTModule),
    data: {
        oPermission: {
            permissionId: 'PLANTFEESTRUCTUREOUT-detail-permissions'
        }
    }
},{
    path: ':PLANT_ID/PLANTHOLDTB', loadChildren: () => import('../PLANTHOLDTB/PLANTHOLDTB.module').then(m => m.PLANTHOLDTBModule),
    data: {
        oPermission: {
            permissionId: 'PLANTHOLDTB-detail-permissions'
        }
    }
},{
    path: ':BILL_TO_PLANT_ID/PRIVATELABELBILL', loadChildren: () => import('../PRIVATELABELBILL/PRIVATELABELBILL.module').then(m => m.PRIVATELABELBILLModule),
    data: {
        oPermission: {
            permissionId: 'PRIVATELABELBILL-detail-permissions'
        }
    }
},{
    path: ':DESTINATION_ID/VISIT', loadChildren: () => import('../VISIT/VISIT.module').then(m => m.VISITModule),
    data: {
        oPermission: {
            permissionId: 'VISIT-detail-permissions'
        }
    }
}
];

export const PLANTTB_MODULE_DECLARATIONS = [
    PLANTTBHomeComponent,
    PLANTTBNewComponent,
    PLANTTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PLANTTBRoutingModule { }