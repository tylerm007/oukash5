import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COMPANYFEECOMMENT_MODULE_DECLARATIONS, COMPANYFEECOMMENTRoutingModule} from  './COMPANYFEECOMMENT-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    COMPANYFEECOMMENTRoutingModule
  ],
  declarations: COMPANYFEECOMMENT_MODULE_DECLARATIONS,
  exports: COMPANYFEECOMMENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class COMPANYFEECOMMENTModule { }