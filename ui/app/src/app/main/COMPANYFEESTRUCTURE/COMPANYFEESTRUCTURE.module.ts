import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COMPANYFEESTRUCTURE_MODULE_DECLARATIONS, COMPANYFEESTRUCTURERoutingModule} from  './COMPANYFEESTRUCTURE-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    COMPANYFEESTRUCTURERoutingModule
  ],
  declarations: COMPANYFEESTRUCTURE_MODULE_DECLARATIONS,
  exports: COMPANYFEESTRUCTURE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class COMPANYFEESTRUCTUREModule { }