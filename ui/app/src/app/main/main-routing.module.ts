import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { MainComponent } from './main.component';

export const routes: Routes = [
  {
    path: '', component: MainComponent,
    children: [
        { path: '', redirectTo: 'home', pathMatch: 'full' },
        { path: 'about', loadChildren: () => import('./about/about.module').then(m => m.AboutModule) },
        { path: 'home', loadChildren: () => import('./home/home.module').then(m => m.HomeModule) },
        { path: 'settings', loadChildren: () => import('./settings/settings.module').then(m => m.SettingsModule) },
      
    
        { path: 'ASSIGNEDMASHGIACHTB', loadChildren: () => import('./ASSIGNEDMASHGIACHTB/ASSIGNEDMASHGIACHTB.module').then(m => m.ASSIGNEDMASHGIACHTBModule) },
    
        { path: 'AchAuthToken', loadChildren: () => import('./AchAuthToken/AchAuthToken.module').then(m => m.AchAuthTokenModule) },
    
        { path: 'AchPlaidLambdaResponse', loadChildren: () => import('./AchPlaidLambdaResponse/AchPlaidLambdaResponse.module').then(m => m.AchPlaidLambdaResponseModule) },
    
        { path: 'AchStripePayment', loadChildren: () => import('./AchStripePayment/AchStripePayment.module').then(m => m.AchStripePaymentModule) },
    
        { path: 'AchStripePaymentDetail', loadChildren: () => import('./AchStripePaymentDetail/AchStripePaymentDetail.module').then(m => m.AchStripePaymentDetailModule) },
    
        { path: 'BarCode', loadChildren: () => import('./BarCode/BarCode.module').then(m => m.BarCodeModule) },
    
        { path: 'Billing', loadChildren: () => import('./Billing/Billing.module').then(m => m.BillingModule) },
    
        { path: 'CODETB', loadChildren: () => import('./CODETB/CODETB.module').then(m => m.CODETBModule) },
    
        { path: 'COMPANYADDRESSTB', loadChildren: () => import('./COMPANYADDRESSTB/COMPANYADDRESSTB.module').then(m => m.COMPANYADDRESSTBModule) },
    
        { path: 'COMPANYCERTDETAIL', loadChildren: () => import('./COMPANYCERTDETAIL/COMPANYCERTDETAIL.module').then(m => m.COMPANYCERTDETAILModule) },
    
        { path: 'COMPANYCOMMENT', loadChildren: () => import('./COMPANYCOMMENT/COMPANYCOMMENT.module').then(m => m.COMPANYCOMMENTModule) },
    
        { path: 'COMPANYFEECOMMENT', loadChildren: () => import('./COMPANYFEECOMMENT/COMPANYFEECOMMENT.module').then(m => m.COMPANYFEECOMMENTModule) },
    
        { path: 'COMPANYFEESTRUCTURE', loadChildren: () => import('./COMPANYFEESTRUCTURE/COMPANYFEESTRUCTURE.module').then(m => m.COMPANYFEESTRUCTUREModule) },
    
        { path: 'COMPANYHOLDTB', loadChildren: () => import('./COMPANYHOLDTB/COMPANYHOLDTB.module').then(m => m.COMPANYHOLDTBModule) },
    
        { path: 'COMPANYOTHERNAME', loadChildren: () => import('./COMPANYOTHERNAME/COMPANYOTHERNAME.module').then(m => m.COMPANYOTHERNAMEModule) },
    
        { path: 'COMPANYSTATUSTB', loadChildren: () => import('./COMPANYSTATUSTB/COMPANYSTATUSTB.module').then(m => m.COMPANYSTATUSTBModule) },
    
        { path: 'COMPANYTB', loadChildren: () => import('./COMPANYTB/COMPANYTB.module').then(m => m.COMPANYTBModule) },
    
        { path: 'COPRIVATELABELFEEDETAIL', loadChildren: () => import('./COPRIVATELABELFEEDETAIL/COPRIVATELABELFEEDETAIL.module').then(m => m.COPRIVATELABELFEEDETAILModule) },
    
        { path: 'CoPackerFacilitiesCategory', loadChildren: () => import('./CoPackerFacilitiesCategory/CoPackerFacilitiesCategory.module').then(m => m.CoPackerFacilitiesCategoryModule) },
    
        { path: 'CoPackerFacilitiesLocation', loadChildren: () => import('./CoPackerFacilitiesLocation/CoPackerFacilitiesLocation.module').then(m => m.CoPackerFacilitiesLocationModule) },
    
        { path: 'CoPackerFacility', loadChildren: () => import('./CoPackerFacility/CoPackerFacility.module').then(m => m.CoPackerFacilityModule) },
    
        { path: 'CompanyPlantOption', loadChildren: () => import('./CompanyPlantOption/CompanyPlantOption.module').then(m => m.CompanyPlantOptionModule) },
    
        { path: 'CompanycontactsTb', loadChildren: () => import('./CompanycontactsTb/CompanycontactsTb.module').then(m => m.CompanycontactsTbModule) },
    
        { path: 'FormulaComponent', loadChildren: () => import('./FormulaComponent/FormulaComponent.module').then(m => m.FormulaComponentModule) },
    
        { path: 'FormulaProduct', loadChildren: () => import('./FormulaProduct/FormulaProduct.module').then(m => m.FormulaProductModule) },
    
        { path: 'FormulaSubmissionComponent', loadChildren: () => import('./FormulaSubmissionComponent/FormulaSubmissionComponent.module').then(m => m.FormulaSubmissionComponentModule) },
    
        { path: 'FormulaSubmissionPlant', loadChildren: () => import('./FormulaSubmissionPlant/FormulaSubmissionPlant.module').then(m => m.FormulaSubmissionPlantModule) },
    
        { path: 'INVOICEFEE', loadChildren: () => import('./INVOICEFEE/INVOICEFEE.module').then(m => m.INVOICEFEEModule) },
    
        { path: 'INVOICEFEESDETAIL', loadChildren: () => import('./INVOICEFEESDETAIL/INVOICEFEESDETAIL.module').then(m => m.INVOICEFEESDETAILModule) },
    
        { path: 'LabelBarcode', loadChildren: () => import('./LabelBarcode/LabelBarcode.module').then(m => m.LabelBarcodeModule) },
    
        { path: 'LabelComment', loadChildren: () => import('./LabelComment/LabelComment.module').then(m => m.LabelCommentModule) },
    
        { path: 'LabelOption', loadChildren: () => import('./LabelOption/LabelOption.module').then(m => m.LabelOptionModule) },
    
        { path: 'LabelTb', loadChildren: () => import('./LabelTb/LabelTb.module').then(m => m.LabelTbModule) },
    
        { path: 'MERCHCOMMENT', loadChildren: () => import('./MERCHCOMMENT/MERCHCOMMENT.module').then(m => m.MERCHCOMMENTModule) },
    
        { path: 'MERCHOTHERNAME', loadChildren: () => import('./MERCHOTHERNAME/MERCHOTHERNAME.module').then(m => m.MERCHOTHERNAMEModule) },
    
        { path: 'MERCHTB', loadChildren: () => import('./MERCHTB/MERCHTB.module').then(m => m.MERCHTBModule) },
    
        { path: 'MiniCRMAction', loadChildren: () => import('./MiniCRMAction/MiniCRMAction.module').then(m => m.MiniCRMActionModule) },
    
        { path: 'OWNSTB', loadChildren: () => import('./OWNSTB/OWNSTB.module').then(m => m.OWNSTBModule) },
    
        { path: 'PENDINGINFOTB', loadChildren: () => import('./PENDINGINFOTB/PENDINGINFOTB.module').then(m => m.PENDINGINFOTBModule) },
    
        { path: 'PERSONADDRESSTB', loadChildren: () => import('./PERSONADDRESSTB/PERSONADDRESSTB.module').then(m => m.PERSONADDRESSTBModule) },
    
        { path: 'PERSONJOBSTATUSTB', loadChildren: () => import('./PERSONJOBSTATUSTB/PERSONJOBSTATUSTB.module').then(m => m.PERSONJOBSTATUSTBModule) },
    
        { path: 'PERSONJOBTB', loadChildren: () => import('./PERSONJOBTB/PERSONJOBTB.module').then(m => m.PERSONJOBTBModule) },
    
        { path: 'PERSONTB', loadChildren: () => import('./PERSONTB/PERSONTB.module').then(m => m.PERSONTBModule) },
    
        { path: 'PLANTADDRESSTB', loadChildren: () => import('./PLANTADDRESSTB/PLANTADDRESSTB.module').then(m => m.PLANTADDRESSTBModule) },
    
        { path: 'PLANTCERTDETAIL', loadChildren: () => import('./PLANTCERTDETAIL/PLANTCERTDETAIL.module').then(m => m.PLANTCERTDETAILModule) },
    
        { path: 'PLANTCOMMENT', loadChildren: () => import('./PLANTCOMMENT/PLANTCOMMENT.module').then(m => m.PLANTCOMMENTModule) },
    
        { path: 'PLANTFEECOMMENT', loadChildren: () => import('./PLANTFEECOMMENT/PLANTFEECOMMENT.module').then(m => m.PLANTFEECOMMENTModule) },
    
        { path: 'PLANTFEESTRUCTURE', loadChildren: () => import('./PLANTFEESTRUCTURE/PLANTFEESTRUCTURE.module').then(m => m.PLANTFEESTRUCTUREModule) },
    
        { path: 'PLANTFEESTRUCTUREOUT', loadChildren: () => import('./PLANTFEESTRUCTUREOUT/PLANTFEESTRUCTUREOUT.module').then(m => m.PLANTFEESTRUCTUREOUTModule) },
    
        { path: 'PLANTHOLDTB', loadChildren: () => import('./PLANTHOLDTB/PLANTHOLDTB.module').then(m => m.PLANTHOLDTBModule) },
    
        { path: 'PLANTOTHERNAME', loadChildren: () => import('./PLANTOTHERNAME/PLANTOTHERNAME.module').then(m => m.PLANTOTHERNAMEModule) },
    
        { path: 'PLANTSTATUSTB', loadChildren: () => import('./PLANTSTATUSTB/PLANTSTATUSTB.module').then(m => m.PLANTSTATUSTBModule) },
    
        { path: 'PLANTTB', loadChildren: () => import('./PLANTTB/PLANTTB.module').then(m => m.PLANTTBModule) },
    
        { path: 'PRIVATELABELBILL', loadChildren: () => import('./PRIVATELABELBILL/PRIVATELABELBILL.module').then(m => m.PRIVATELABELBILLModule) },
    
        { path: 'PrivateLabelTemplate', loadChildren: () => import('./PrivateLabelTemplate/PrivateLabelTemplate.module').then(m => m.PrivateLabelTemplateModule) },
    
        { path: 'ProducedIn1Tb', loadChildren: () => import('./ProducedIn1Tb/ProducedIn1Tb.module').then(m => m.ProducedIn1TbModule) },
    
        { path: 'ProductJob', loadChildren: () => import('./ProductJob/ProductJob.module').then(m => m.ProductJobModule) },
    
        { path: 'ProductJobLineItem', loadChildren: () => import('./ProductJobLineItem/ProductJobLineItem.module').then(m => m.ProductJobLineItemModule) },
    
        { path: 'PurchaseOrder', loadChildren: () => import('./PurchaseOrder/PurchaseOrder.module').then(m => m.PurchaseOrderModule) },
    
        { path: 'RCTB', loadChildren: () => import('./RCTB/RCTB.module').then(m => m.RCTBModule) },
    
        { path: 'StripeCustomer', loadChildren: () => import('./StripeCustomer/StripeCustomer.module').then(m => m.StripeCustomerModule) },
    
        { path: 'ThirdPartyBillingCompany', loadChildren: () => import('./ThirdPartyBillingCompany/ThirdPartyBillingCompany.module').then(m => m.ThirdPartyBillingCompanyModule) },
    
        { path: 'USEDIN1TB', loadChildren: () => import('./USEDIN1TB/USEDIN1TB.module').then(m => m.USEDIN1TBModule) },
    
        { path: 'VISIT', loadChildren: () => import('./VISIT/VISIT.module').then(m => m.VISITModule) },
    
        { path: 'VISITSCOMMENT', loadChildren: () => import('./VISITSCOMMENT/VISITSCOMMENT.module').then(m => m.VISITSCOMMENTModule) },
    
        { path: 'YoshonInfo', loadChildren: () => import('./YoshonInfo/YoshonInfo.module').then(m => m.YoshonInfoModule) },
    
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainRoutingModule { }