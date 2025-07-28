import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PLANTCOMMENT_MODULE_DECLARATIONS, PLANTCOMMENTRoutingModule} from  './PLANTCOMMENT-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PLANTCOMMENTRoutingModule
  ],
  declarations: PLANTCOMMENT_MODULE_DECLARATIONS,
  exports: PLANTCOMMENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PLANTCOMMENTModule { }