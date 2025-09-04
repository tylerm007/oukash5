import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFPRIORITY_MODULE_DECLARATIONS, WFPriorityRoutingModule} from  './WFPriority-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFPriorityRoutingModule
  ],
  declarations: WFPRIORITY_MODULE_DECLARATIONS,
  exports: WFPRIORITY_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFPriorityModule { }