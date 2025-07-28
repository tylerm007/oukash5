import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COMPANYCERTDETAIL_MODULE_DECLARATIONS, COMPANYCERTDETAILRoutingModule} from  './COMPANYCERTDETAIL-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    COMPANYCERTDETAILRoutingModule
  ],
  declarations: COMPANYCERTDETAIL_MODULE_DECLARATIONS,
  exports: COMPANYCERTDETAIL_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class COMPANYCERTDETAILModule { }