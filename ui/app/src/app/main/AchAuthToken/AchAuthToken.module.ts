import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {ACHAUTHTOKEN_MODULE_DECLARATIONS, AchAuthTokenRoutingModule} from  './AchAuthToken-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    AchAuthTokenRoutingModule
  ],
  declarations: ACHAUTHTOKEN_MODULE_DECLARATIONS,
  exports: ACHAUTHTOKEN_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AchAuthTokenModule { }