import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COMPANYAPPLICATION_MODULE_DECLARATIONS, CompanyApplicationRoutingModule} from  './CompanyApplication-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    CompanyApplicationRoutingModule
  ],
  declarations: COMPANYAPPLICATION_MODULE_DECLARATIONS,
  exports: COMPANYAPPLICATION_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class CompanyApplicationModule { }