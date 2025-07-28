import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COPACKERFACILITIESLOCATION_MODULE_DECLARATIONS, CoPackerFacilitiesLocationRoutingModule} from  './CoPackerFacilitiesLocation-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    CoPackerFacilitiesLocationRoutingModule
  ],
  declarations: COPACKERFACILITIESLOCATION_MODULE_DECLARATIONS,
  exports: COPACKERFACILITIESLOCATION_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class CoPackerFacilitiesLocationModule { }