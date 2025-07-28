import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {ACHPLAIDLAMBDARESPONSE_MODULE_DECLARATIONS, AchPlaidLambdaResponseRoutingModule} from  './AchPlaidLambdaResponse-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    AchPlaidLambdaResponseRoutingModule
  ],
  declarations: ACHPLAIDLAMBDARESPONSE_MODULE_DECLARATIONS,
  exports: ACHPLAIDLAMBDARESPONSE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AchPlaidLambdaResponseModule { }