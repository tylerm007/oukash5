import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PROCESSMESSAGETYPE_MODULE_DECLARATIONS, ProcessMessageTypeRoutingModule} from  './ProcessMessageType-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    ProcessMessageTypeRoutingModule
  ],
  declarations: PROCESSMESSAGETYPE_MODULE_DECLARATIONS,
  exports: PROCESSMESSAGETYPE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ProcessMessageTypeModule { }