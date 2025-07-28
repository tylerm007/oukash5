import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COMPANYSTATUSTB_MODULE_DECLARATIONS, COMPANYSTATUSTBRoutingModule} from  './COMPANYSTATUSTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    COMPANYSTATUSTBRoutingModule
  ],
  declarations: COMPANYSTATUSTB_MODULE_DECLARATIONS,
  exports: COMPANYSTATUSTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class COMPANYSTATUSTBModule { }