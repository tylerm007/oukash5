import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {STAGEINSTANCE_MODULE_DECLARATIONS, StageInstanceRoutingModule} from  './StageInstance-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    StageInstanceRoutingModule
  ],
  declarations: STAGEINSTANCE_MODULE_DECLARATIONS,
  exports: STAGEINSTANCE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class StageInstanceModule { }