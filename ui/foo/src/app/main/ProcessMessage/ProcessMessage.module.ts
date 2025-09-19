import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PROCESSMESSAGE_MODULE_DECLARATIONS, ProcessMessageRoutingModule} from  './ProcessMessage-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    ProcessMessageRoutingModule
  ],
  declarations: PROCESSMESSAGE_MODULE_DECLARATIONS,
  exports: PROCESSMESSAGE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ProcessMessageModule { }