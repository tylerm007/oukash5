import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {FORMULACOMPONENT_MODULE_DECLARATIONS, FormulaComponentRoutingModule} from  './FormulaComponent-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    FormulaComponentRoutingModule
  ],
  declarations: FORMULACOMPONENT_MODULE_DECLARATIONS,
  exports: FORMULACOMPONENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class FormulaComponentModule { }