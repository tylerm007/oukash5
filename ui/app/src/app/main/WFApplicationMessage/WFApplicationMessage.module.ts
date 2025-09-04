import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFAPPLICATIONMESSAGE_MODULE_DECLARATIONS, WFApplicationMessageRoutingModule} from  './WFApplicationMessage-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFApplicationMessageRoutingModule
  ],
  declarations: WFAPPLICATIONMESSAGE_MODULE_DECLARATIONS,
  exports: WFAPPLICATIONMESSAGE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFApplicationMessageModule { }