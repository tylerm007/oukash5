import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import { HttpClientModule } from '@angular/common/http';
import  {WFFILE_MODULE_DECLARATIONS, WFFileRoutingModule} from  './WFFile-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    HttpClientModule,
    WFFileRoutingModule
  ],
  declarations: WFFILE_MODULE_DECLARATIONS,
  exports: WFFILE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFFileModule { }