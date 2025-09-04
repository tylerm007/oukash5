import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {TASKCATEGORY_MODULE_DECLARATIONS, TaskCategoryRoutingModule} from  './TaskCategory-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    TaskCategoryRoutingModule
  ],
  declarations: TASKCATEGORY_MODULE_DECLARATIONS,
  exports: TASKCATEGORY_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class TaskCategoryModule { }