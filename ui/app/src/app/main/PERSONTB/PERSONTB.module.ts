import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PERSONTB_MODULE_DECLARATIONS, PERSONTBRoutingModule} from  './PERSONTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PERSONTBRoutingModule
  ],
  declarations: PERSONTB_MODULE_DECLARATIONS,
  exports: PERSONTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PERSONTBModule { }