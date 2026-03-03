import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { HttpClientModule } from '@angular/common/http';
import { SharedModule } from '../../shared/shared.module';
import  {WFAPPLICATION_MODULE_DECLARATIONS, WFApplicationRoutingModule} from  './WFApplication-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    HttpClientModule,
    WFApplicationRoutingModule
  ],
  declarations: WFAPPLICATION_MODULE_DECLARATIONS,
  exports: WFAPPLICATION_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFApplicationModule { }