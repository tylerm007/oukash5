import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PLANTSTATUSTB_MODULE_DECLARATIONS, PLANTSTATUSTBRoutingModule} from  './PLANTSTATUSTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PLANTSTATUSTBRoutingModule
  ],
  declarations: PLANTSTATUSTB_MODULE_DECLARATIONS,
  exports: PLANTSTATUSTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PLANTSTATUSTBModule { }