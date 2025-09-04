import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {SYSDIAGRAM_MODULE_DECLARATIONS, SysdiagramRoutingModule} from  './Sysdiagram-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    SysdiagramRoutingModule
  ],
  declarations: SYSDIAGRAM_MODULE_DECLARATIONS,
  exports: SYSDIAGRAM_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class SysdiagramModule { }