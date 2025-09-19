import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {TASKDEFINITION_MODULE_DECLARATIONS, TaskDefinitionRoutingModule} from  './TaskDefinition-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    TaskDefinitionRoutingModule
  ],
  declarations: TASKDEFINITION_MODULE_DECLARATIONS,
  exports: TASKDEFINITION_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class TaskDefinitionModule { }