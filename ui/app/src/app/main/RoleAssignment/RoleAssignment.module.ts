import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {ROLEASSIGNMENT_MODULE_DECLARATIONS, RoleAssignmentRoutingModule} from  './RoleAssignment-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    RoleAssignmentRoutingModule
  ],
  declarations: ROLEASSIGNMENT_MODULE_DECLARATIONS,
  exports: ROLEASSIGNMENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class RoleAssignmentModule { }