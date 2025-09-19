import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PROCESSPRIORITY_MODULE_DECLARATIONS, ProcessPriorityRoutingModule} from  './ProcessPriority-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    ProcessPriorityRoutingModule
  ],
  declarations: PROCESSPRIORITY_MODULE_DECLARATIONS,
  exports: PROCESSPRIORITY_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ProcessPriorityModule { }