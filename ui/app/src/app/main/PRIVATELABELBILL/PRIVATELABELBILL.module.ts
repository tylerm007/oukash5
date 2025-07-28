import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PRIVATELABELBILL_MODULE_DECLARATIONS, PRIVATELABELBILLRoutingModule} from  './PRIVATELABELBILL-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PRIVATELABELBILLRoutingModule
  ],
  declarations: PRIVATELABELBILL_MODULE_DECLARATIONS,
  exports: PRIVATELABELBILL_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PRIVATELABELBILLModule { }