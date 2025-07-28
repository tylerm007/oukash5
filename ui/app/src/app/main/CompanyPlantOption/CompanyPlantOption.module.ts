import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COMPANYPLANTOPTION_MODULE_DECLARATIONS, CompanyPlantOptionRoutingModule} from  './CompanyPlantOption-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    CompanyPlantOptionRoutingModule
  ],
  declarations: COMPANYPLANTOPTION_MODULE_DECLARATIONS,
  exports: COMPANYPLANTOPTION_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class CompanyPlantOptionModule { }