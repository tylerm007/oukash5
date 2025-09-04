import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {LANEROLE_MODULE_DECLARATIONS, LaneRoleRoutingModule} from  './LaneRole-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    LaneRoleRoutingModule
  ],
  declarations: LANEROLE_MODULE_DECLARATIONS,
  exports: LANEROLE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class LaneRoleModule { }