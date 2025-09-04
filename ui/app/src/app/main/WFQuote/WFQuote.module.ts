import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFQUOTE_MODULE_DECLARATIONS, WFQuoteRoutingModule} from  './WFQuote-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFQuoteRoutingModule
  ],
  declarations: WFQUOTE_MODULE_DECLARATIONS,
  exports: WFQUOTE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFQuoteModule { }