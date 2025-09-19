import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {TASKSTATUS_MODULE_DECLARATIONS, TaskStatusRoutingModule} from  './TaskStatus-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    TaskStatusRoutingModule
  ],
  declarations: TASKSTATUS_MODULE_DECLARATIONS,
  exports: TASKSTATUS_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class TaskStatusModule { }