import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFCOMPANY_MODULE_DECLARATIONS, WFCompanyRoutingModule} from  './WFCompany-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFCompanyRoutingModule
  ],
  declarations: WFCOMPANY_MODULE_DECLARATIONS,
  exports: WFCOMPANY_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFCompanyModule { }