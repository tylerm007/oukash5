import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFDASHBOARD_MODULE_DECLARATIONS, WFDashboardRoutingModule} from  './WFDashboard-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFDashboardRoutingModule
  ],
  declarations: WFDASHBOARD_MODULE_DECLARATIONS,
  exports: WFDASHBOARD_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFDashboardModule { }