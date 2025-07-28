import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {ACHSTRIPEPAYMENTDETAIL_MODULE_DECLARATIONS, AchStripePaymentDetailRoutingModule} from  './AchStripePaymentDetail-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    AchStripePaymentDetailRoutingModule
  ],
  declarations: ACHSTRIPEPAYMENTDETAIL_MODULE_DECLARATIONS,
  exports: ACHSTRIPEPAYMENTDETAIL_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AchStripePaymentDetailModule { }