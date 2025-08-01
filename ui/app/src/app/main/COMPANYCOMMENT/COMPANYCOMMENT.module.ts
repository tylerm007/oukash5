import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COMPANYCOMMENT_MODULE_DECLARATIONS, COMPANYCOMMENTRoutingModule} from  './COMPANYCOMMENT-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    COMPANYCOMMENTRoutingModule
  ],
  declarations: COMPANYCOMMENT_MODULE_DECLARATIONS,
  exports: COMPANYCOMMENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class COMPANYCOMMENTModule { }