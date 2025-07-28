import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COPRIVATELABELFEEDETAIL_MODULE_DECLARATIONS, COPRIVATELABELFEEDETAILRoutingModule} from  './COPRIVATELABELFEEDETAIL-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    COPRIVATELABELFEEDETAILRoutingModule
  ],
  declarations: COPRIVATELABELFEEDETAIL_MODULE_DECLARATIONS,
  exports: COPRIVATELABELFEEDETAIL_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class COPRIVATELABELFEEDETAILModule { }