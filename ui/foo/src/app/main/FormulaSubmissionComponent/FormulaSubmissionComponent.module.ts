import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {FORMULASUBMISSIONCOMPONENT_MODULE_DECLARATIONS, FormulaSubmissionComponentRoutingModule} from  './FormulaSubmissionComponent-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    FormulaSubmissionComponentRoutingModule
  ],
  declarations: FORMULASUBMISSIONCOMPONENT_MODULE_DECLARATIONS,
  exports: FORMULASUBMISSIONCOMPONENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class FormulaSubmissionComponentModule { }