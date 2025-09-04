import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFACTIVITYLOG_MODULE_DECLARATIONS, WFActivityLogRoutingModule} from  './WFActivityLog-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFActivityLogRoutingModule
  ],
  declarations: WFACTIVITYLOG_MODULE_DECLARATIONS,
  exports: WFACTIVITYLOG_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFActivityLogModule { }