import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COMPANYTB_MODULE_DECLARATIONS, COMPANYTBRoutingModule} from  './COMPANYTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    COMPANYTBRoutingModule
  ],
  declarations: COMPANYTB_MODULE_DECLARATIONS,
  exports: COMPANYTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class COMPANYTBModule { }