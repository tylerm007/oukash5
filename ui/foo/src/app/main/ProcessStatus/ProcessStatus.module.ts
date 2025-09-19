import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PROCESSSTATUS_MODULE_DECLARATIONS, ProcessStatusRoutingModule} from  './ProcessStatus-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    ProcessStatusRoutingModule
  ],
  declarations: PROCESSSTATUS_MODULE_DECLARATIONS,
  exports: PROCESSSTATUS_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ProcessStatusModule { }