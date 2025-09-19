import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {ROLEASSIGMENT_MODULE_DECLARATIONS, RoleAssigmentRoutingModule} from  './RoleAssigment-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    RoleAssigmentRoutingModule
  ],
  declarations: ROLEASSIGMENT_MODULE_DECLARATIONS,
  exports: ROLEASSIGMENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class RoleAssigmentModule { }