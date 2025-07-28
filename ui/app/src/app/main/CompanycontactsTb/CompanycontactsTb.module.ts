import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {COMPANYCONTACTSTB_MODULE_DECLARATIONS, CompanycontactsTbRoutingModule} from  './CompanycontactsTb-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    CompanycontactsTbRoutingModule
  ],
  declarations: COMPANYCONTACTSTB_MODULE_DECLARATIONS,
  exports: COMPANYCONTACTSTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class CompanycontactsTbModule { }