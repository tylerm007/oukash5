import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { COMPANYTBHomeComponent } from './home/COMPANYTB-home.component';
import { COMPANYTBNewComponent } from './new/COMPANYTB-new.component';
import { COMPANYTBDetailComponent } from './detail/COMPANYTB-detail.component';

const routes: Routes = [
  {path: '', component: COMPANYTBHomeComponent},
  { path: 'new', component: COMPANYTBNewComponent },
  { path: ':COMPANY_ID', component: COMPANYTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'COMPANYTB-detail-permissions'
      }
    }
  },{
    path: ':company_id/AchAuthToken', loadChildren: () => import('../AchAuthToken/AchAuthToken.module').then(m => m.AchAuthTokenModule),
    data: {
        oPermission: {
            permissionId: 'AchAuthToken-detail-permissions'
        }
    }
},{
    path: ':company_id/AchPlaidLambdaResponse', loadChildren: () => import('../AchPlaidLambdaResponse/AchPlaidLambdaResponse.module').then(m => m.AchPlaidLambdaResponseModule),
    data: {
        oPermission: {
            permissionId: 'AchPlaidLambdaResponse-detail-permissions'
        }
    }
},{
    path: ':company_id/AchStripePayment', loadChildren: () => import('../AchStripePayment/AchStripePayment.module').then(m => m.AchStripePaymentModule),
    data: {
        oPermission: {
            permissionId: 'AchStripePayment-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/BarCode', loadChildren: () => import('../BarCode/BarCode.module').then(m => m.BarCodeModule),
    data: {
        oPermission: {
            permissionId: 'BarCode-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/Billing', loadChildren: () => import('../Billing/Billing.module').then(m => m.BillingModule),
    data: {
        oPermission: {
            permissionId: 'Billing-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/COMPANYADDRESSTB', loadChildren: () => import('../COMPANYADDRESSTB/COMPANYADDRESSTB.module').then(m => m.COMPANYADDRESSTBModule),
    data: {
        oPermission: {
            permissionId: 'COMPANYADDRESSTB-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/COMPANYCERTDETAIL', loadChildren: () => import('../COMPANYCERTDETAIL/COMPANYCERTDETAIL.module').then(m => m.COMPANYCERTDETAILModule),
    data: {
        oPermission: {
            permissionId: 'COMPANYCERTDETAIL-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/COMPANYCOMMENT', loadChildren: () => import('../COMPANYCOMMENT/COMPANYCOMMENT.module').then(m => m.COMPANYCOMMENTModule),
    data: {
        oPermission: {
            permissionId: 'COMPANYCOMMENT-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/COMPANYFEECOMMENT', loadChildren: () => import('../COMPANYFEECOMMENT/COMPANYFEECOMMENT.module').then(m => m.COMPANYFEECOMMENTModule),
    data: {
        oPermission: {
            permissionId: 'COMPANYFEECOMMENT-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/COMPANYFEESTRUCTURE', loadChildren: () => import('../COMPANYFEESTRUCTURE/COMPANYFEESTRUCTURE.module').then(m => m.COMPANYFEESTRUCTUREModule),
    data: {
        oPermission: {
            permissionId: 'COMPANYFEESTRUCTURE-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/COMPANYFEESTRUCTURE', loadChildren: () => import('../COMPANYFEESTRUCTURE/COMPANYFEESTRUCTURE.module').then(m => m.COMPANYFEESTRUCTUREModule),
    data: {
        oPermission: {
            permissionId: 'COMPANYFEESTRUCTURE-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/COMPANYHOLDTB', loadChildren: () => import('../COMPANYHOLDTB/COMPANYHOLDTB.module').then(m => m.COMPANYHOLDTBModule),
    data: {
        oPermission: {
            permissionId: 'COMPANYHOLDTB-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/COMPANYHOLDTB', loadChildren: () => import('../COMPANYHOLDTB/COMPANYHOLDTB.module').then(m => m.COMPANYHOLDTBModule),
    data: {
        oPermission: {
            permissionId: 'COMPANYHOLDTB-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/COMPANYOTHERNAME', loadChildren: () => import('../COMPANYOTHERNAME/COMPANYOTHERNAME.module').then(m => m.COMPANYOTHERNAMEModule),
    data: {
        oPermission: {
            permissionId: 'COMPANYOTHERNAME-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/COMPANYSTATUSTB', loadChildren: () => import('../COMPANYSTATUSTB/COMPANYSTATUSTB.module').then(m => m.COMPANYSTATUSTBModule),
    data: {
        oPermission: {
            permissionId: 'COMPANYSTATUSTB-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/COMPANYSTATUSTB', loadChildren: () => import('../COMPANYSTATUSTB/COMPANYSTATUSTB.module').then(m => m.COMPANYSTATUSTBModule),
    data: {
        oPermission: {
            permissionId: 'COMPANYSTATUSTB-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/COPRIVATELABELFEEDETAIL', loadChildren: () => import('../COPRIVATELABELFEEDETAIL/COPRIVATELABELFEEDETAIL.module').then(m => m.COPRIVATELABELFEEDETAILModule),
    data: {
        oPermission: {
            permissionId: 'COPRIVATELABELFEEDETAIL-detail-permissions'
        }
    }
},{
    path: ':CompanyId/CoPackerFacility', loadChildren: () => import('../CoPackerFacility/CoPackerFacility.module').then(m => m.CoPackerFacilityModule),
    data: {
        oPermission: {
            permissionId: 'CoPackerFacility-detail-permissions'
        }
    }
},{
    path: ':Company_ID/CompanyPlantOption', loadChildren: () => import('../CompanyPlantOption/CompanyPlantOption.module').then(m => m.CompanyPlantOptionModule),
    data: {
        oPermission: {
            permissionId: 'CompanyPlantOption-detail-permissions'
        }
    }
},{
    path: ':Company_ID/CompanycontactsTb', loadChildren: () => import('../CompanycontactsTb/CompanycontactsTb.module').then(m => m.CompanycontactsTbModule),
    data: {
        oPermission: {
            permissionId: 'CompanycontactsTb-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/INVOICEFEE', loadChildren: () => import('../INVOICEFEE/INVOICEFEE.module').then(m => m.INVOICEFEEModule),
    data: {
        oPermission: {
            permissionId: 'INVOICEFEE-detail-permissions'
        }
    }
},{
    path: ':SRC_MAR_ID/LabelTb', loadChildren: () => import('../LabelTb/LabelTb.module').then(m => m.LabelTbModule),
    data: {
        oPermission: {
            permissionId: 'LabelTb-detail-permissions'
        }
    }
},{
    path: ':SRC_MAR_ID/LabelTb', loadChildren: () => import('../LabelTb/LabelTb.module').then(m => m.LabelTbModule),
    data: {
        oPermission: {
            permissionId: 'LabelTb-detail-permissions'
        }
    }
},{
    path: ':CompanyId/MiniCRMAction', loadChildren: () => import('../MiniCRMAction/MiniCRMAction.module').then(m => m.MiniCRMActionModule),
    data: {
        oPermission: {
            permissionId: 'MiniCRMAction-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/OWNSTB', loadChildren: () => import('../OWNSTB/OWNSTB.module').then(m => m.OWNSTBModule),
    data: {
        oPermission: {
            permissionId: 'OWNSTB-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/PENDINGINFOTB', loadChildren: () => import('../PENDINGINFOTB/PENDINGINFOTB.module').then(m => m.PENDINGINFOTBModule),
    data: {
        oPermission: {
            permissionId: 'PENDINGINFOTB-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/PLANTADDRESSTB', loadChildren: () => import('../PLANTADDRESSTB/PLANTADDRESSTB.module').then(m => m.PLANTADDRESSTBModule),
    data: {
        oPermission: {
            permissionId: 'PLANTADDRESSTB-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/PLANTCERTDETAIL', loadChildren: () => import('../PLANTCERTDETAIL/PLANTCERTDETAIL.module').then(m => m.PLANTCERTDETAILModule),
    data: {
        oPermission: {
            permissionId: 'PLANTCERTDETAIL-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/PLANTCOMMENT', loadChildren: () => import('../PLANTCOMMENT/PLANTCOMMENT.module').then(m => m.PLANTCOMMENTModule),
    data: {
        oPermission: {
            permissionId: 'PLANTCOMMENT-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/PLANTFEECOMMENT', loadChildren: () => import('../PLANTFEECOMMENT/PLANTFEECOMMENT.module').then(m => m.PLANTFEECOMMENTModule),
    data: {
        oPermission: {
            permissionId: 'PLANTFEECOMMENT-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/PLANTFEESTRUCTURE', loadChildren: () => import('../PLANTFEESTRUCTURE/PLANTFEESTRUCTURE.module').then(m => m.PLANTFEESTRUCTUREModule),
    data: {
        oPermission: {
            permissionId: 'PLANTFEESTRUCTURE-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/PLANTFEESTRUCTUREOUT', loadChildren: () => import('../PLANTFEESTRUCTUREOUT/PLANTFEESTRUCTUREOUT.module').then(m => m.PLANTFEESTRUCTUREOUTModule),
    data: {
        oPermission: {
            permissionId: 'PLANTFEESTRUCTUREOUT-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/PLANTHOLDTB', loadChildren: () => import('../PLANTHOLDTB/PLANTHOLDTB.module').then(m => m.PLANTHOLDTBModule),
    data: {
        oPermission: {
            permissionId: 'PLANTHOLDTB-detail-permissions'
        }
    }
},{
    path: ':PrimaryCompany/PLANTTB', loadChildren: () => import('../PLANTTB/PLANTTB.module').then(m => m.PLANTTBModule),
    data: {
        oPermission: {
            permissionId: 'PLANTTB-detail-permissions'
        }
    }
},{
    path: ':BILL_TO_CO_ID/PRIVATELABELBILL', loadChildren: () => import('../PRIVATELABELBILL/PRIVATELABELBILL.module').then(m => m.PRIVATELABELBILLModule),
    data: {
        oPermission: {
            permissionId: 'PRIVATELABELBILL-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/PRIVATELABELBILL', loadChildren: () => import('../PRIVATELABELBILL/PRIVATELABELBILL.module').then(m => m.PRIVATELABELBILLModule),
    data: {
        oPermission: {
            permissionId: 'PRIVATELABELBILL-detail-permissions'
        }
    }
},{
    path: ':SRC_MAR_ID/PRIVATELABELBILL', loadChildren: () => import('../PRIVATELABELBILL/PRIVATELABELBILL.module').then(m => m.PRIVATELABELBILLModule),
    data: {
        oPermission: {
            permissionId: 'PRIVATELABELBILL-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/PrivateLabelTemplate', loadChildren: () => import('../PrivateLabelTemplate/PrivateLabelTemplate.module').then(m => m.PrivateLabelTemplateModule),
    data: {
        oPermission: {
            permissionId: 'PrivateLabelTemplate-detail-permissions'
        }
    }
},{
    path: ':company_id/ProductJob', loadChildren: () => import('../ProductJob/ProductJob.module').then(m => m.ProductJobModule),
    data: {
        oPermission: {
            permissionId: 'ProductJob-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/PurchaseOrder', loadChildren: () => import('../PurchaseOrder/PurchaseOrder.module').then(m => m.PurchaseOrderModule),
    data: {
        oPermission: {
            permissionId: 'PurchaseOrder-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/RCTB', loadChildren: () => import('../RCTB/RCTB.module').then(m => m.RCTBModule),
    data: {
        oPermission: {
            permissionId: 'RCTB-detail-permissions'
        }
    }
},{
    path: ':company_id/StripeCustomer', loadChildren: () => import('../StripeCustomer/StripeCustomer.module').then(m => m.StripeCustomerModule),
    data: {
        oPermission: {
            permissionId: 'StripeCustomer-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/ThirdPartyBillingCompany', loadChildren: () => import('../ThirdPartyBillingCompany/ThirdPartyBillingCompany.module').then(m => m.ThirdPartyBillingCompanyModule),
    data: {
        oPermission: {
            permissionId: 'ThirdPartyBillingCompany-detail-permissions'
        }
    }
},{
    path: ':BrokerID/USEDIN1TB', loadChildren: () => import('../USEDIN1TB/USEDIN1TB.module').then(m => m.USEDIN1TBModule),
    data: {
        oPermission: {
            permissionId: 'USEDIN1TB-detail-permissions'
        }
    }
},{
    path: ':VISIT_FOR_ID/VISIT', loadChildren: () => import('../VISIT/VISIT.module').then(m => m.VISITModule),
    data: {
        oPermission: {
            permissionId: 'VISIT-detail-permissions'
        }
    }
}
];

export const COMPANYTB_MODULE_DECLARATIONS = [
    COMPANYTBHomeComponent,
    COMPANYTBNewComponent,
    COMPANYTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class COMPANYTBRoutingModule { }