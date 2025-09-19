import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFAPPLICATIONSTATUS_MODULE_DECLARATIONS, WFApplicationStatusRoutingModule} from  './WFApplicationStatus-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFApplicationStatusRoutingModule
  ],
  declarations: WFAPPLICATIONSTATUS_MODULE_DECLARATIONS,
  exports: WFAPPLICATIONSTATUS_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFApplicationStatusModule { }