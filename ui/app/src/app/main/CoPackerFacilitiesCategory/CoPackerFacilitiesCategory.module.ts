import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COPACKERFACILITIESCATEGORY_MODULE_DECLARATIONS, CoPackerFacilitiesCategoryRoutingModule} from  './CoPackerFacilitiesCategory-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    CoPackerFacilitiesCategoryRoutingModule
  ],
  declarations: COPACKERFACILITIESCATEGORY_MODULE_DECLARATIONS,
  exports: COPACKERFACILITIESCATEGORY_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class CoPackerFacilitiesCategoryModule { }