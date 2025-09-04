import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {VALIDATIONRESULT_MODULE_DECLARATIONS, ValidationResultRoutingModule} from  './ValidationResult-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    ValidationResultRoutingModule
  ],
  declarations: VALIDATIONRESULT_MODULE_DECLARATIONS,
  exports: VALIDATIONRESULT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ValidationResultModule { }