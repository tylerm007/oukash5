import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {FORMULAPRODUCT_MODULE_DECLARATIONS, FormulaProductRoutingModule} from  './FormulaProduct-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    FormulaProductRoutingModule
  ],
  declarations: FORMULAPRODUCT_MODULE_DECLARATIONS,
  exports: FORMULAPRODUCT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class FormulaProductModule { }