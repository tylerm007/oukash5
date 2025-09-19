import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {TASKINSTANCE_MODULE_DECLARATIONS, TaskInstanceRoutingModule} from  './TaskInstance-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    TaskInstanceRoutingModule
  ],
  declarations: TASKINSTANCE_MODULE_DECLARATIONS,
  exports: TASKINSTANCE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class TaskInstanceModule { }