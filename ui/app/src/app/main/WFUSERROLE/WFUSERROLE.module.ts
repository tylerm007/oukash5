import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFUSERROLE_MODULE_DECLARATIONS, WFUSERROLERoutingModule} from  './WFUSERROLE-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFUSERROLERoutingModule
  ],
  declarations: WFUSERROLE_MODULE_DECLARATIONS,
  exports: WFUSERROLE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFUSERROLEModule { }