import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFCONTACT_MODULE_DECLARATIONS, WFContactRoutingModule} from  './WFContact-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFContactRoutingModule
  ],
  declarations: WFCONTACT_MODULE_DECLARATIONS,
  exports: WFCONTACT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFContactModule { }