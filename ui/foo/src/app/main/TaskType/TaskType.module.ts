import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {TASKTYPE_MODULE_DECLARATIONS, TaskTypeRoutingModule} from  './TaskType-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    TaskTypeRoutingModule
  ],
  declarations: TASKTYPE_MODULE_DECLARATIONS,
  exports: TASKTYPE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class TaskTypeModule { }