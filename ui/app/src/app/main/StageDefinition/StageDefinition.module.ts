import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {STAGEDEFINITION_MODULE_DECLARATIONS, StageDefinitionRoutingModule} from  './StageDefinition-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    StageDefinitionRoutingModule
  ],
  declarations: STAGEDEFINITION_MODULE_DECLARATIONS,
  exports: STAGEDEFINITION_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class StageDefinitionModule { }