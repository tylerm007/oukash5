import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {STRIPECUSTOMER_MODULE_DECLARATIONS, StripeCustomerRoutingModule} from  './StripeCustomer-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    StripeCustomerRoutingModule
  ],
  declarations: STRIPECUSTOMER_MODULE_DECLARATIONS,
  exports: STRIPECUSTOMER_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class StripeCustomerModule { }