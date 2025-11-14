import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFUSERADMIN_MODULE_DECLARATIONS, WFUserAdminRoutingModule} from  './WFUserAdmin-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFUserAdminRoutingModule
  ],
  declarations: WFUSERADMIN_MODULE_DECLARATIONS,
  exports: WFUSERADMIN_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFUserAdminModule { }