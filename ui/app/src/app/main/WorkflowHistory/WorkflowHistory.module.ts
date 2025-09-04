import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WORKFLOWHISTORY_MODULE_DECLARATIONS, WorkflowHistoryRoutingModule} from  './WorkflowHistory-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WorkflowHistoryRoutingModule
  ],
  declarations: WORKFLOWHISTORY_MODULE_DECLARATIONS,
  exports: WORKFLOWHISTORY_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WorkflowHistoryModule { }