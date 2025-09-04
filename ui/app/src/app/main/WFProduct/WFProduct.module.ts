import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFPRODUCT_MODULE_DECLARATIONS, WFProductRoutingModule} from  './WFProduct-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFProductRoutingModule
  ],
  declarations: WFPRODUCT_MODULE_DECLARATIONS,
  exports: WFPRODUCT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFProductModule { }