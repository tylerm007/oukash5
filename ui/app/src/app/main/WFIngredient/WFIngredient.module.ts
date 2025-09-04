import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFINGREDIENT_MODULE_DECLARATIONS, WFIngredientRoutingModule} from  './WFIngredient-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFIngredientRoutingModule
  ],
  declarations: WFINGREDIENT_MODULE_DECLARATIONS,
  exports: WFINGREDIENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFIngredientModule { }