import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {STAGESTATUS_MODULE_DECLARATIONS, StageStatusRoutingModule} from  './StageStatus-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    StageStatusRoutingModule
  ],
  declarations: STAGESTATUS_MODULE_DECLARATIONS,
  exports: STAGESTATUS_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class StageStatusModule { }