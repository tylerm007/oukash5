import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {TASKCOMMENT_MODULE_DECLARATIONS, TaskCommentRoutingModule} from  './TaskComment-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    TaskCommentRoutingModule
  ],
  declarations: TASKCOMMENT_MODULE_DECLARATIONS,
  exports: TASKCOMMENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class TaskCommentModule { }