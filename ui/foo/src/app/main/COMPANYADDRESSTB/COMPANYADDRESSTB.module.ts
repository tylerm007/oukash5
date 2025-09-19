import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COMPANYADDRESSTB_MODULE_DECLARATIONS, COMPANYADDRESSTBRoutingModule} from  './COMPANYADDRESSTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    COMPANYADDRESSTBRoutingModule
  ],
  declarations: COMPANYADDRESSTB_MODULE_DECLARATIONS,
  exports: COMPANYADDRESSTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class COMPANYADDRESSTBModule { }