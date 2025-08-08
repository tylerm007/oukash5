import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PLANTOTHERNAME_MODULE_DECLARATIONS, PLANTOTHERNAMERoutingModule} from  './PLANTOTHERNAME-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PLANTOTHERNAMERoutingModule
  ],
  declarations: PLANTOTHERNAME_MODULE_DECLARATIONS,
  exports: PLANTOTHERNAME_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PLANTOTHERNAMEModule { }