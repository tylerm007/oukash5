import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COMPANYHOLDTB_MODULE_DECLARATIONS, COMPANYHOLDTBRoutingModule} from  './COMPANYHOLDTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    COMPANYHOLDTBRoutingModule
  ],
  declarations: COMPANYHOLDTB_MODULE_DECLARATIONS,
  exports: COMPANYHOLDTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class COMPANYHOLDTBModule { }