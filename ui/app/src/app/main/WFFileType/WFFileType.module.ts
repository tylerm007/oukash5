import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFFILETYPE_MODULE_DECLARATIONS, WFFileTypeRoutingModule} from  './WFFileType-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFFileTypeRoutingModule
  ],
  declarations: WFFILETYPE_MODULE_DECLARATIONS,
  exports: WFFILETYPE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFFileTypeModule { }