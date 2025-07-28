import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PERSONJOBTB_MODULE_DECLARATIONS, PERSONJOBTBRoutingModule} from  './PERSONJOBTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PERSONJOBTBRoutingModule
  ],
  declarations: PERSONJOBTB_MODULE_DECLARATIONS,
  exports: PERSONJOBTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PERSONJOBTBModule { }