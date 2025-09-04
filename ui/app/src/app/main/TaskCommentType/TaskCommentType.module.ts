import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {TASKCOMMENTTYPE_MODULE_DECLARATIONS, TaskCommentTypeRoutingModule} from  './TaskCommentType-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    TaskCommentTypeRoutingModule
  ],
  declarations: TASKCOMMENTTYPE_MODULE_DECLARATIONS,
  exports: TASKCOMMENTTYPE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class TaskCommentTypeModule { }