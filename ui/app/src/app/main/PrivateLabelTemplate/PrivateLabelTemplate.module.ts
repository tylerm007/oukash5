import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PRIVATELABELTEMPLATE_MODULE_DECLARATIONS, PrivateLabelTemplateRoutingModule} from  './PrivateLabelTemplate-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PrivateLabelTemplateRoutingModule
  ],
  declarations: PRIVATELABELTEMPLATE_MODULE_DECLARATIONS,
  exports: PRIVATELABELTEMPLATE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PrivateLabelTemplateModule { }