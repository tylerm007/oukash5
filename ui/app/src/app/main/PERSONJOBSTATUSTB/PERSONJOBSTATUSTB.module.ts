import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PERSONJOBSTATUSTB_MODULE_DECLARATIONS, PERSONJOBSTATUSTBRoutingModule} from  './PERSONJOBSTATUSTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PERSONJOBSTATUSTBRoutingModule
  ],
  declarations: PERSONJOBSTATUSTB_MODULE_DECLARATIONS,
  exports: PERSONJOBSTATUSTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PERSONJOBSTATUSTBModule { }