import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {THIRDPARTYBILLINGCOMPANY_MODULE_DECLARATIONS, ThirdPartyBillingCompanyRoutingModule} from  './ThirdPartyBillingCompany-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    ThirdPartyBillingCompanyRoutingModule
  ],
  declarations: THIRDPARTYBILLINGCOMPANY_MODULE_DECLARATIONS,
  exports: THIRDPARTYBILLINGCOMPANY_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ThirdPartyBillingCompanyModule { }