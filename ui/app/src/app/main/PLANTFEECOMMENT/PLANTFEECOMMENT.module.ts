import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PLANTFEECOMMENT_MODULE_DECLARATIONS, PLANTFEECOMMENTRoutingModule} from  './PLANTFEECOMMENT-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PLANTFEECOMMENTRoutingModule
  ],
  declarations: PLANTFEECOMMENT_MODULE_DECLARATIONS,
  exports: PLANTFEECOMMENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PLANTFEECOMMENTModule { }