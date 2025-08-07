import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {ASSIGNEDMASHGIACHTB_MODULE_DECLARATIONS, ASSIGNEDMASHGIACHTBRoutingModule} from  './ASSIGNEDMASHGIACHTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    ASSIGNEDMASHGIACHTBRoutingModule
  ],
  declarations: ASSIGNEDMASHGIACHTB_MODULE_DECLARATIONS,
  exports: ASSIGNEDMASHGIACHTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ASSIGNEDMASHGIACHTBModule { }