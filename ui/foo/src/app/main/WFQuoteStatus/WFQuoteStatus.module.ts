import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFQUOTESTATUS_MODULE_DECLARATIONS, WFQuoteStatusRoutingModule} from  './WFQuoteStatus-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFQuoteStatusRoutingModule
  ],
  declarations: WFQUOTESTATUS_MODULE_DECLARATIONS,
  exports: WFQUOTESTATUS_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFQuoteStatusModule { }