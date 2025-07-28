import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COPACKERFACILITY_MODULE_DECLARATIONS, CoPackerFacilityRoutingModule} from  './CoPackerFacility-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    CoPackerFacilityRoutingModule
  ],
  declarations: COPACKERFACILITY_MODULE_DECLARATIONS,
  exports: COPACKERFACILITY_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class CoPackerFacilityModule { }