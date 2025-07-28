import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PENDINGINFOTB_MODULE_DECLARATIONS, PENDINGINFOTBRoutingModule} from  './PENDINGINFOTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PENDINGINFOTBRoutingModule
  ],
  declarations: PENDINGINFOTB_MODULE_DECLARATIONS,
  exports: PENDINGINFOTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PENDINGINFOTBModule { }