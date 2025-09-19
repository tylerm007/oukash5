import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PLANTADDRESSTB_MODULE_DECLARATIONS, PLANTADDRESSTBRoutingModule} from  './PLANTADDRESSTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PLANTADDRESSTBRoutingModule
  ],
  declarations: PLANTADDRESSTB_MODULE_DECLARATIONS,
  exports: PLANTADDRESSTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PLANTADDRESSTBModule { }