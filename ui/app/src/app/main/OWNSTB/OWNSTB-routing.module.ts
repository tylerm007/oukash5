import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OWNSTBHomeComponent } from './home/OWNSTB-home.component';
import { OWNSTBNewComponent } from './new/OWNSTB-new.component';
import { OWNSTBDetailComponent } from './detail/OWNSTB-detail.component';

const routes: Routes = [
  {path: '', component: OWNSTBHomeComponent},
  { path: 'new', component: OWNSTBNewComponent },
  { path: ':ID', component: OWNSTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'OWNSTB-detail-permissions'
      }
    }
  },{
    path: ':OWNS_ID/Billing', loadChildren: () => import('../Billing/Billing.module').then(m => m.BillingModule),
    data: {
        oPermission: {
            permissionId: 'Billing-detail-permissions'
        }
    }
},{
    path: ':OwnsID/CompanyPlantOption', loadChildren: () => import('../CompanyPlantOption/CompanyPlantOption.module').then(m => m.CompanyPlantOptionModule),
    data: {
        oPermission: {
            permissionId: 'CompanyPlantOption-detail-permissions'
        }
    }
},{
    path: ':OwnsID/PLANTFEESTRUCTURE', loadChildren: () => import('../PLANTFEESTRUCTURE/PLANTFEESTRUCTURE.module').then(m => m.PLANTFEESTRUCTUREModule),
    data: {
        oPermission: {
            permissionId: 'PLANTFEESTRUCTURE-detail-permissions'
        }
    }
},{
    path: ':OwnsID/PLANTHOLDTB', loadChildren: () => import('../PLANTHOLDTB/PLANTHOLDTB.module').then(m => m.PLANTHOLDTBModule),
    data: {
        oPermission: {
            permissionId: 'PLANTHOLDTB-detail-permissions'
        }
    }
},{
    path: ':OWNS_ID/ProducedIn1Tb', loadChildren: () => import('../ProducedIn1Tb/ProducedIn1Tb.module').then(m => m.ProducedIn1TbModule),
    data: {
        oPermission: {
            permissionId: 'ProducedIn1Tb-detail-permissions'
        }
    }
},{
    path: ':ownsID/ProductJobLineItem', loadChildren: () => import('../ProductJobLineItem/ProductJobLineItem.module').then(m => m.ProductJobLineItemModule),
    data: {
        oPermission: {
            permissionId: 'ProductJobLineItem-detail-permissions'
        }
    }
},{
    path: ':OWNS_ID/PurchaseOrder', loadChildren: () => import('../PurchaseOrder/PurchaseOrder.module').then(m => m.PurchaseOrderModule),
    data: {
        oPermission: {
            permissionId: 'PurchaseOrder-detail-permissions'
        }
    }
},{
    path: ':OWNS_ID/ThirdPartyBillingCompany', loadChildren: () => import('../ThirdPartyBillingCompany/ThirdPartyBillingCompany.module').then(m => m.ThirdPartyBillingCompanyModule),
    data: {
        oPermission: {
            permissionId: 'ThirdPartyBillingCompany-detail-permissions'
        }
    }
},{
    path: ':OWNS_ID/USEDIN1TB', loadChildren: () => import('../USEDIN1TB/USEDIN1TB.module').then(m => m.USEDIN1TBModule),
    data: {
        oPermission: {
            permissionId: 'USEDIN1TB-detail-permissions'
        }
    }
}
];

export const OWNSTB_MODULE_DECLARATIONS = [
    OWNSTBHomeComponent,
    OWNSTBNewComponent,
    OWNSTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OWNSTBRoutingModule { }