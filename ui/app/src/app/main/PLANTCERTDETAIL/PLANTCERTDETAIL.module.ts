import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PLANTCERTDETAIL_MODULE_DECLARATIONS, PLANTCERTDETAILRoutingModule} from  './PLANTCERTDETAIL-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PLANTCERTDETAILRoutingModule
  ],
  declarations: PLANTCERTDETAIL_MODULE_DECLARATIONS,
  exports: PLANTCERTDETAIL_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PLANTCERTDETAILModule { }