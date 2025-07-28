import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PERSONADDRESSTB_MODULE_DECLARATIONS, PERSONADDRESSTBRoutingModule} from  './PERSONADDRESSTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PERSONADDRESSTBRoutingModule
  ],
  declarations: PERSONADDRESSTB_MODULE_DECLARATIONS,
  exports: PERSONADDRESSTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PERSONADDRESSTBModule { }