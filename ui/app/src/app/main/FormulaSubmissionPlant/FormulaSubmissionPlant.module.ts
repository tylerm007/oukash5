import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {FORMULASUBMISSIONPLANT_MODULE_DECLARATIONS, FormulaSubmissionPlantRoutingModule} from  './FormulaSubmissionPlant-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    FormulaSubmissionPlantRoutingModule
  ],
  declarations: FORMULASUBMISSIONPLANT_MODULE_DECLARATIONS,
  exports: FORMULASUBMISSIONPLANT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class FormulaSubmissionPlantModule { }