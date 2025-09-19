import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PROCESSINSTANCE_MODULE_DECLARATIONS, ProcessInstanceRoutingModule} from  './ProcessInstance-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    ProcessInstanceRoutingModule
  ],
  declarations: PROCESSINSTANCE_MODULE_DECLARATIONS,
  exports: PROCESSINSTANCE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ProcessInstanceModule { }