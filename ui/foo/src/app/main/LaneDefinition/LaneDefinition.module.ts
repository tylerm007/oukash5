import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {LANEDEFINITION_MODULE_DECLARATIONS, LaneDefinitionRoutingModule} from  './LaneDefinition-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    LaneDefinitionRoutingModule
  ],
  declarations: LANEDEFINITION_MODULE_DECLARATIONS,
  exports: LANEDEFINITION_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class LaneDefinitionModule { }