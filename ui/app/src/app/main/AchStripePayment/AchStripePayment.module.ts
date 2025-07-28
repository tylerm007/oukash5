import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {ACHSTRIPEPAYMENT_MODULE_DECLARATIONS, AchStripePaymentRoutingModule} from  './AchStripePayment-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    AchStripePaymentRoutingModule
  ],
  declarations: ACHSTRIPEPAYMENT_MODULE_DECLARATIONS,
  exports: ACHSTRIPEPAYMENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AchStripePaymentModule { }